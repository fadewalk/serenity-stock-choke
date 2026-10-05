#!/usr/bin/env python3
"""
Serenity A股/港美股框架 · 独立数据查询脚本（零依赖，多源冗余）

不依赖任何智能体平台（WorkBuddy/Claude Code/Codex 均可调用），无需 API Key，
仅用 Python 标准库 + 公开财经接口；akshare 为可选增强（筹码/大宗）。

数据源（按稳定性排序，自动降级）：
  行情快照   东方财富 push2 → 腾讯 qt.gtimg.cn（A股/港股/美股均支持）
  板块K线    东方财富 push2his（仅A股板块；不可用时提示改用网络检索）
  名称联想   东方财富 searchapi（自动识别 A股/港股/美股）
  券商研报   东方财富 reportapi（仅A股）
  融资融券   东方财富 datacenter-web（仅A股）
  筹码/大宗  akshare（可选安装，仅A股）

用法（结果均为 JSON，可直接被智能体解析）:
  python3 scripts/a_stock_query.py stock 贵州茅台     # A股快照: 价格/涨跌幅/PE/PB/市值/主力净流入
  python3 scripts/a_stock_query.py stock 00700        # 港股: 腾讯控股(HKD)
  python3 scripts/a_stock_query.py stock AAPL         # 美股: 苹果(USD)
  python3 scripts/a_stock_query.py search 英伟达       # 名称联想（A股+港股+美股+板块）
  python3 scripts/a_stock_query.py sector 电力 [--days 5]   # A股板块近N日K线+区间涨跌幅
  python3 scripts/a_stock_query.py reports 600519     # A股券商研报: 评级/机构/盈利预测
  python3 scripts/a_stock_query.py margin 600519      # A股融资融券余额近5日
  python3 scripts/a_stock_query.py chip 600519        # A股筹码分布（需 akshare）
  python3 scripts/a_stock_query.py block 600519       # A股大宗交易（需 akshare）
"""

import argparse
import datetime
import json
import subprocess
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
TIMEOUT = 15

# ---------------- 数据源端点 ----------------
SUGGEST_URL = ("https://searchapi.eastmoney.com/api/suggest/get"
               "?input={kw}&type=14&token=D43BF722C8E33BDC906FB84D85E326E8")
EM_STOCK = ("https://push2.eastmoney.com/api/qt/stock/get"
            "?secid={secid}&fltt=2&invt=2&fields=f43,f57,f58,f169,f170,f162,f167,f116,f117,f62")
EM_KLINE = ("https://push2his.eastmoney.com/api/qt/stock/kline/get"
            "?secid={secid}&klt=101&fqt=1&lmt={lmt}&end=20500101"
            "&fields1=f1,f2,f3&fields2=f51,f53,f56,f57")
TX_QUOTE = "https://qt.gtimg.cn/q={symbol}"
REPORT_URL = ("https://reportapi.eastmoney.com/report/list"
              "?pageSize={n}&pageNo=1&code={code}&industryCode=*&industry=*"
              "&rating=*&ratingchange=*&beginTime={begin}&endTime={end}&qType=0")
MARGIN_URL = ("https://datacenter-web.eastmoney.com/api/data/v1/get"
              "?reportName=RPTA_WEB_RZRQ_GGMX&columns=ALL"
              "&filter=(scode%3D%22{code}%22)&sortColumns=DATE&sortTypes=-1"
              "&pageSize={n}&pageNumber=1")

NET_HINT = ("数据源暂不可达（可能为网络/地域限制或临时限流）。"
            "请改用：1) 智能体自带的财经 MCP 工具；2) 网络检索该关键词（见 SKILL.md 三级数据策略）。")


# ---------------- 传输层：urllib → curl 自动降级 + 重试 ----------------
def _fetch_once(url: str, decode: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Referer": "https://quote.eastmoney.com/"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode(decode, "ignore")
    except Exception as e:  # noqa: BLE001
        print(f"[warn] urllib: {e}，降级 curl", file=sys.stderr)
    try:
        out = subprocess.run(["curl", "-s", "--max-time", str(TIMEOUT), "-A", UA, url],
                             capture_output=True, timeout=TIMEOUT + 5)
        if out.returncode == 0 and out.stdout:
            return out.stdout.decode(decode, "ignore")
    except Exception as e:  # noqa: BLE001
        print(f"[warn] curl: {e}", file=sys.stderr)
    return None


def _fetch(url: str, decode="utf-8", retries=3):
    """GET 并按指定编码解码文本。urllib 失败（TLS拦截等）自动降级系统 curl，
    并对间歇性网络失败做最多 retries 次重试（1s 退避）。"""
    import time
    for i in range(retries):
        text = _fetch_once(url, decode)
        if text:
            return text
        if i < retries - 1:
            time.sleep(1)
    return None


def _get_json(url: str):
    text = _fetch(url)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _fail(result=None):
    print(json.dumps(result or {"error": NET_HINT}, ensure_ascii=False))
    sys.exit(2)


def _fmt_amount(v):
    if v is None:
        return None
    v = float(v)
    if abs(v) >= 1e8:
        return f"{v / 1e8:.2f}亿"
    if abs(v) >= 1e4:
        return f"{v / 1e4:.2f}万"
    return f"{v:.0f}"


# ---------------- 名称/代码解析 ----------------
def _market_of(quote_id: str) -> str:
    """东财 QuoteID 前缀 → 市场标识"""
    prefix = quote_id.split(".")[0] if "." in quote_id else ""
    return {"1": "cn", "0": "cn", "116": "hk",
            "105": "us", "106": "us", "107": "us"}.get(prefix, "cn" if prefix else "cn")


def _guess_secid(code: str):
    """联想接口不可用时的纯规则兜底（仅A股/港股代码可推断）"""
    if code.isdigit() and len(code) == 6:
        mkt = "sh" if code.startswith(("6", "9")) else "sz"
        prefix = "1" if mkt == "sh" else "0"
        return {"code": code, "name": None, "quote_id": f"{prefix}.{code}",
                "is_board": False, "market": "cn", "tx_symbol": f"{mkt}{code}"}
    if code.isdigit() and 4 <= len(code) <= 5:
        c = code.zfill(5)
        return {"code": c, "name": None, "quote_id": f"116.{c}",
                "is_board": False, "market": "hk", "tx_symbol": f"hk{c}"}
    return None


def _tx_symbol_of(t: dict) -> str:
    """统一标识 → 腾讯行情 symbol（A股 sh/sz、港股 hk、美股 us）"""
    if t.get("tx_symbol"):
        return t["tx_symbol"]
    market, qid = t.get("market"), t.get("quote_id", "")
    code = t.get("code", "")
    if market == "hk":
        return f"hk{code}"
    if market == "us":
        return f"us{code}"
    return ("sh" if qid.startswith("1.") else "sz") + code


def resolve(keyword: str):
    """名称/代码/拼音 → 统一标识 {code,name,quote_id,is_board,market,tx_symbol}"""
    d = _get_json(SUGGEST_URL.format(kw=urllib.parse.quote(keyword)))
    rows = (d or {}).get("QuotationCodeTable", {}).get("Data") or []
    hit = None
    for r in rows:                      # 优先精确代码命中
        if r.get("Code") == keyword:
            hit = r
            break
    hit = hit or (rows[0] if rows else None)
    if hit:
        qid = hit.get("QuoteID", "")
        t = {"code": hit.get("Code"), "name": hit.get("Name"), "quote_id": qid,
             "is_board": qid.startswith("90."), "market": _market_of(qid)}
        t["tx_symbol"] = _tx_symbol_of(t)
        return t
    return _guess_secid(keyword) if keyword.replace(".", "").isalnum() else None


# ---------------- 命令实现 ----------------
def _tx_parse_hk_us(f: list, market: str, t: dict):
    """腾讯港/美股字段映射：[3]现价 [31]涨跌 [32]涨跌幅% [39]PE [44/45]市值亿 [46]英文名 [48/49]52周"""
    if len(f) < 50 or not f[3]:
        return None
    currency = "HKD" if market == "hk" else "USD"
    mv = f[45] if market == "us" and f[45] else f[44]
    return {"source": "tencent", "market": market, "code": t["code"],
            "name": f[1], "name_en": f[46] if len(f) > 46 and f[46] else None,
            "currency": currency,
            "price": float(f[3]), "pct_change": float(f[32]),
            "pe_ttm": float(f[39]) if f[39] else None,
            "pb": None,
            "total_mv": f"{mv}亿{currency}" if mv else None,
            "week52_high": float(f[48]) if f[48] else None,
            "week52_low": float(f[49]) if f[49] else None,
            "note": "港美股公开接口不提供PB与主力资金流；"
                    "估值与资金信号请用第三级网络检索（13F/沽空比率/南向资金等）"}


def cmd_stock(keyword: str):
    t = resolve(keyword)
    if not t or t["is_board"]:
        _fail({"error": f"未找到个股: {keyword}，请先用 search 命令确认代码"})

    # 主源：东方财富（A股含主力净流入；港美股同样支持 secid 查询）
    d = (_get_json(EM_STOCK.format(secid=t["quote_id"])) or {}).get("data")
    if d and d.get("f43") is not None:
        out = {"source": "eastmoney", "market": t["market"], "code": d.get("f57"),
               "name": d.get("f58"), "price": d.get("f43"), "pct_change": d.get("f170"),
               "pe_ttm": d.get("f162"), "pb": d.get("f167"),
               "total_mv": _fmt_amount(d.get("f116")),
               "float_mv": _fmt_amount(d.get("f117"))}
        if t["market"] == "cn":
            out["main_inflow_today"] = _fmt_amount(d.get("f62"))
        else:
            out["currency"] = "HKD" if t["market"] == "hk" else "USD"
            out["note"] = "港美股公开接口不提供主力资金流；信号获取见 SKILL.md 跨市场章节"
        return out

    # 降级源：腾讯行情（A股/港股/美股）
    text = _fetch(TX_QUOTE.format(symbol=t["tx_symbol"]), decode="gbk")
    if text and "~" in text:
        f = text.split('"')[1].split("~")
        if t["market"] == "cn":
            if len(f) > 53 and f[3]:
                return {"source": "tencent", "market": "cn", "code": t["code"],
                        "name": f[1], "price": float(f[3]), "pct_change": float(f[32]),
                        "pe_ttm": float(f[39]), "pb": float(f[46]),
                        "total_mv": f"{f[45]}亿", "float_mv": f"{f[44]}亿",
                        "turnover_pct": float(f[38]), "volume_hand": float(f[36]),
                        "main_inflow_today": None,
                        "note": "主力净流入本源不提供，可用 margin 命令或网络检索补充"}
        else:
            out = _tx_parse_hk_us(f, t["market"], t)
            if out:
                return out
    _fail()


def cmd_sector(keyword: str, days: int = 5):
    t = resolve(keyword)
    if not t:
        _fail({"error": f"未找到板块: {keyword}，请先用 search 命令确认"})
    if not t["is_board"]:
        t = {"quote_id": t["quote_id"], "code": t["code"], "name": t["name"]}  # 个股也照查K线
    d = (_get_json(EM_KLINE.format(secid=t["quote_id"], lmt=days)) or {}).get("data")
    klines = []
    if d and d.get("klines"):
        for line in d["klines"]:
            dt, close, vol, amt = line.split(",")
            klines.append({"date": dt, "close": float(close), "volume_hand": int(vol),
                           "amount": _fmt_amount(float(amt))})
    if not klines:
        _fail({"error": "板块K线数据源（东财 push2his）暂不可达。"
                        "请改用智能体财经工具或网络检索『{kw} 板块 行情 资金流向』".format(kw=keyword)})
    pct = round((klines[-1]["close"] / klines[0]["close"] - 1) * 100, 2) if len(klines) >= 2 else None
    return {"code": d.get("code"), "name": d.get("name"), "window_days": days,
            "range_pct": pct, "klines": klines,
            "note": "range_pct 为区间涨跌幅；板块实时资金流请配合网络检索"}


def _require_cn_stock(keyword: str):
    t = resolve(keyword)
    if not t or t["is_board"]:
        _fail({"error": f"未找到个股: {keyword}，请先用 search 命令确认代码"})
    if t["market"] != "cn":
        _fail({"error": f"{t.get('name') or keyword} 属于{'港股' if t['market'] == 'hk' else '美股'}，"
                        "本命令仅支持A股。港美股对应数据请用第三级网络检索："
                        "美股『TICKER 13F holdings short interest』；港股『代码 南向资金 沽空比率』"})
    return t


def cmd_reports(keyword: str, n: int = 8):
    t = _require_cn_stock(keyword)
    end = datetime.date.today()
    begin = end - datetime.timedelta(days=180)
    d = _get_json(REPORT_URL.format(code=t["code"], n=n, begin=begin, end=end))
    rows = [{"date": (r.get("publishDate") or "")[:10], "title": r.get("title"),
             "org": r.get("orgSName"),
             "rating": r.get("emRatingName") or r.get("sRatingName"),
             "eps_forecast": r.get("predictThisYearEps"),
             "pe_forecast": r.get("predictThisYearPe")}
            for r in (d or {}).get("data") or []]
    if not rows:
        _fail({"error": "研报数据暂不可达，请网络检索『公司名 券商研报 评级 目标价』"})
    return {"code": t["code"], "name": t["name"], "count": len(rows), "reports": rows,
            "note": "研报开始覆盖 = 机构关注度信号（六步法第五步做多信号）"}


def cmd_margin(keyword: str, n: int = 5):
    t = _require_cn_stock(keyword)
    d = _get_json(MARGIN_URL.format(code=t["code"], n=n))
    rows = [{"date": (r.get("DATE") or "")[:10],
             "margin_balance": _fmt_amount(r.get("RZYE")),
             "margin_net_buy": _fmt_amount(r.get("RZJME")),
             "rzrq_total": _fmt_amount(r.get("RZRQYE"))}
            for r in ((d or {}).get("result") or {}).get("data") or []]
    if not rows:
        _fail({"error": "两融数据暂不可达，请网络检索『代码 融资余额』"})
    return {"code": t["code"], "name": t["name"], "count": len(rows), "rows": rows,
            "note": "融资余额连续上升 = 杠杆资金看多；连续下降需警惕"}


def cmd_search(keyword: str):
    d = _get_json(SUGGEST_URL.format(kw=urllib.parse.quote(keyword)))
    rows = []
    for r in ((d or {}).get("QuotationCodeTable") or {}).get("Data") or []:
        qid = r.get("QuoteID", "")
        if qid.startswith("90."):
            mtype = "板块"
        else:
            mtype = {"cn": "A股", "hk": "港股", "us": "美股"}[_market_of(qid)]
        rows.append({"code": r.get("Code"), "name": r.get("Name"),
                     "type": mtype, "quote_id": qid})
    if not rows:
        _fail({"error": f"无匹配或接口不可达: {keyword}。"
                        "可能是俗称/概念叫法与东财板块库不一致，建议：1) 换近义关键词重试"
                        "（如 光模块→CPO、光通信）；2) 用网络检索『{kw} 板块 行情』兜底".format(kw=keyword)})
    return {"keyword": keyword, "matches": rows}


# ---------------- akshare 可选增强 ----------------
def _ak_available():
    try:
        import akshare  # noqa: F401
        return True
    except ImportError:
        return False


def cmd_chip(keyword: str):
    if not _ak_available():
        _fail({"error": "筹码分布需可选依赖 akshare：pip install akshare；"
                        "或网络检索『代码 筹码分布 股东人数』"})
    import akshare as ak
    t = _require_cn_stock(keyword)
    df = ak.stock_cyq_em(symbol=t["code"], adjust="")
    return {"code": t["code"], "name": t["name"],
            "chip_distribution": json.loads(df.to_json(orient="records", force_ascii=False)),
            "note": "获利盘比例升高+筹码集中 = 主力控盘信号"}


def cmd_block(keyword: str):
    if not _ak_available():
        _fail({"error": "大宗交易需可选依赖 akshare：pip install akshare；"
                        "或网络检索『代码 大宗交易 折价率』"})
    import akshare as ak
    t = _require_cn_stock(keyword)
    df = ak.stock_dzjy_mrmx(symbol=t["code"])
    return {"code": t["code"], "name": t["name"],
            "block_trades": json.loads(df.tail(20).to_json(orient="records", force_ascii=False)),
            "note": "机构专用席位接货+低折价 = 建仓信号"}


def main():
    parser = argparse.ArgumentParser(description="Serenity A股框架 · 独立数据查询（零依赖多源冗余）")
    sub = parser.add_subparsers(dest="command", required=True)
    specs = [("stock", cmd_stock, "个股名称/代码/拼音"),
             ("sector", cmd_sector, "板块或个股名称"),
             ("reports", cmd_reports, "个股名称/代码"),
             ("margin", cmd_margin, "个股名称/代码"),
             ("search", cmd_search, "任意关键词"),
             ("chip", cmd_chip, "个股代码"),
             ("block", cmd_block, "个股代码")]
    for name, _, help_ in specs:
        sub.add_parser(name).add_argument("target", help=help_)
    sub.choices["sector"].add_argument("--days", type=int, default=5, help="K线天数，默认5")
    args = parser.parse_args()

    handlers = {name: fn for name, fn, _ in specs}
    kwargs = {"days": args.days} if args.command == "sector" else {}
    print(f"[查询] {args.command} {args.target}", file=sys.stderr)
    print(json.dumps(handlers[args.command](args.target, **kwargs), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
