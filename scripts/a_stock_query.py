#!/usr/bin/env python3
"""
Serenity A股框架 · 通用查询脚本
用法: python a_stock_query.py --query "查询内容" --type [sector|stock|policy|fund]
"""

import argparse
import json
import subprocess
import sys
import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SKILL_DIR, ".token_cache")

def load_token():
    """加载已缓存的 token"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return f.read().strip()
    return None

def save_token(token):
    """缓存 token"""
    with open(CACHE_FILE, "w") as f:
        f.write(token)

def query_neodata(query: str, data_type: str = "api") -> dict:
    """通过 neodata-financial-search 查询"""
    script = os.path.join(
        os.path.dirname(SKILL_DIR),
        "neodata-financial-search/scripts/query.py"
    )
    cmd = [
        "/Users/fadewalk/.workbuddy/binaries/python/envs/default/bin/python3",
        script,
        "--query", query,
        "--data-type", data_type,
    ]
    token = load_token()
    if token:
        cmd.extend(["--save-token", token])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout[:2000]}

def query_sector(sector_name: str) -> dict:
    """查询板块行情+资金流向"""
    return query_neodata(f"{sector_name} 板块 行情 资金流向")

def query_stock(stock_name: str) -> dict:
    """查询个股行情"""
    return query_neodata(f"{stock_name} 股价 行情")

def query_supply_chain(material: str) -> dict:
    """查询供应链卡脖子情况"""
    return query_neodata(f"{material} 供需缺口 国产替代 扩产周期")

def query_policy(sector: str) -> dict:
    """查询政策催化"""
    return query_neodata(f"{sector} 政府工作报告 政策 文件")

def query_report(stock_name: str) -> dict:
    """查询研报信号"""
    return query_neodata(f"{stock_name} 券商研报 评级 目标价")

def main():
    parser = argparse.ArgumentParser(description="Serenity A股框架通用查询")
    parser.add_argument("--query", "-q", required=True, help="查询内容")
    parser.add_argument("--type", "-t", default="stock",
                        choices=["sector", "stock", "supply", "policy", "report"],
                        help="查询类型")
    args = parser.parse_args()

    query_map = {
        "sector": (query_sector, args.query),
        "stock": (query_stock, args.query),
        "supply": (query_supply_chain, args.query),
        "policy": (query_policy, args.query),
        "report": (query_report, args.query),
    }

    handler, q = query_map[args.type]
    print(f"[查询] {q}", file=sys.stderr)
    result = handler(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
