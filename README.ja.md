# Serenity Stock Choke · A株/香港株/米国株 ボトルネック（チョークポイント）投資フレームワーク

<p align="center"><a href="README.md">简体中文</a> · <a href="README.en.md">English</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a></p>

> "**サプライチェーンを上流に遡り、『そこが途絶えたら兆円産業が停止する』中核ノードを見つける——そのノードに座る小型株こそ、次の大打撃のチャンスだ。**"

本スキルは、Redditの伝説的トレーダー **Serenity（@aleabitoreddit）** のサプライチェーン・ボトルネック理論を、**A株・香港株・米国株**の3市場に展開する汎用フレームワークです。Serenityの元祖の戦例は米国株（AXTI・AAOI）であり、A株版はそのローカライズです。

---

## コアメソドロジー

### 「ホルムズ海峡」のアナロジー

> 「ホルムズ海峡は世界の石油の喉元だ。封鎖されれば皆が影響を受ける。しかし、ホルムズ海峡そのものに株式を持っていれば、価格決定権を握れる。」

**投資への翻訳**：ある巨大トラックの「ホルムズ」とはどのノードか——それを支配する上場企業（A株/香港株/米国株）はどこか？

### 3段階のコアロジック

```
① AI爆発 / 政策ドライブ / 技術の飛躍
    ↓
② 上流のハードウェア・素材需要が急増し、供給網の一部が追いつかない
    ↓
③ ボトルネック・ノードが価格決定権を獲得 → そこにある小型株の値動きが最大
```

### Serenityの実績（米国株・ 参考）

| 銘柄 | ティッカー | チョークポイントの位置づけ |
|------|-----------|--------------------------|
| AXT Inc | AXTI.US | InP基板の世界トップ3メーカーの一つ |
| Applied Optoelectronics | AAOI.US | CPOレーザーの主要サプライヤー |
| Sivers Semiconductors | SIVE.SE | CPOレーザー + シリコンフォトニクス |
| X-FAB | XFAB.EU | 特殊プロセスファウンドリ |

> ⚠️ 上表は**事後視点のサバイバーシップ（生存者）サンプル**であり、フレームワークのロジック説明用です。フレームワークの期待リターンを表すものではありません。

---

## 6ステップ分析パイプライン

| ステップ | 問い | アウトプット |
|---------|------|------------|
| 1️⃣ 循環段階 | 需要爆発 / 技術躍進 / 供給制約のどれか？ | セクターの段階判定 |
| 2️⃣ サプライチェーン追跡 | どの層がボトルネックか？ | 階層マップ |
| 3️⃣ 上場銘柄の特定 | そのノードに座るのは誰か？（A/香港/米） | 4要素シグナルカード |
| 4️⃣ 真贋スクリーニング | 本物のボトルネックか、テーマ便乗か？ | 7つの除外ルールで判定 |
| 5️⃣ 双方向確認 | 強気シグナル vs 弱気シグナル？ | シグナル対照表 |
| 6️⃣ レポート | ポジション設計 + リスク | 構造化レポート（8セクション） |

---

## 対応市場

| 市場 | 行情・評価（`stock`/`search`） | セクターK線 | レポート/信用/チップ |
|------|:---:|:---:|:---:|
| **A株** | ✅ 主力資金流込み | ✅ | ✅ |
| **香港株** | ✅ HKD建て | — | Web検索で補完 |
| **米国株** | ✅ USD建て・中国語名対応 | — | Web検索で補完 |

6ステップのフレームワーク自体は市場非依存です。香港株・米国株の機関シグナル（13F、空売り残高、南向き資金、空売り比率）はSKILL.mdの検索テンプレートを使用。**13Fは45日遅延（四半期）、空売り残高は半月频**である点に注意。

---

## クイックスタート

### インストール（いずれか一つ）

**方法0 — AIエージェントに一言投げる（最簡単）**。以下の文をClaude Code / Codex等のコマンド実行可能なエージェントに貼り付ければ、自動でクローン・インストール・検証まで行います：

```
https://github.com/fadewalk/serenity-stock-choke のスキルをインストールして：
このエージェントのスキルディレクトリ（Claude Code: ~/.claude/skills/、
その他: .agents/skills/、不明ならリポジトリのREADME参照）にクローンし、
python3 <skill-dir>/scripts/a_stock_query.py stock 600519 で動作確認、
その後このスキルの使い方とできることを教えて。
```

**方法1 — Claude Codeプラグインマーケット：**

```
/plugin marketplace add fadewalk/serenity-stock-choke
/plugin install serenity-stock-choke@serenity-stock-choke
```

**方法2 — skills.shインストーラ：**

```bash
npx skills add fadewalk/serenity-stock-choke
```

**方法3 — 手動クローン：**

```bash
git clone https://github.com/fadewalk/serenity-stock-choke.git ~/.claude/skills/serenity-stock-choke
```

同梱のクエリスクリプトはPython標準ライブラリのみ使用——依存関係なし・APIキー不要（`akshare`はオプション：`pip install akshare`）。

### トリガー方法

```
serenity-stock-choke で [セクター] を分析して
例：serenity-stock-choke で米国AIコンピュート・サプライチェーンを分析して
[業界] のボトルネックを見つけて
```

### データアクセス（3段階フォールバック、どの環境でも動作）

1. **エージェント内蔵の金融ツール**（MCP市況・レポートツール）——あれば最優先
2. **同梱スクリプト**（`scripts/a_stock_query.py`、ゼロ依存・マルチソース自動切替）：
   ```bash
   python3 scripts/a_stock_query.py stock 600519     # A株スナップショット：価格/PER/PB/時価総額/資金流
   python3 scripts/a_stock_query.py stock 00700      # 香港株：テンセント（HKD）
   python3 scripts/a_stock_query.py stock AAPL       # 米国株：アップル（USD）
   python3 scripts/a_stock_query.py valuation 600519 # A株 PER/PB の歴史パーセンタイル
   python3 scripts/a_stock_query.py kline 300308     # モメンタム/年率ボラ/最大ドローダウン
   python3 scripts/a_stock_query.py business 600519  # A株 売上構成（テーマ便乗チェック）
   python3 scripts/a_stock_query.py sector 电力       # A株 セクターK線
   python3 scripts/a_stock_query.py reports 600519   # A株 券商レポート
   python3 scripts/a_stock_query.py margin 600519    # A株 信用残高
   ```
3. **Web検索フォールバック**：供給ギャップ・政策・チップ分布・13F・空売り等はSKILL.mdのテンプレートで

## ファイル構成

```
serenity-stock-choke/
├── SKILL.md                    # メインプロンプト（6ステップ + 3段階データ戦略）
├── README.md                   # 简体中文版
├── README.en.md                # English
├── README.ja.md                # このファイル
├── README.ko.md                # 한국어版
├── .claude-plugin/             # Claude Codeプラグイン（ワンクリック導入）
├── scripts/
│   └── a_stock_query.py        # 独立データスクリプト（ゼロ依存・A/香港/米対応）
└── references/
    └── user_guide.md          # 使用ガイド（中国語）
```

---

## リスク開示

1. 研究参考用であり、投資助言ではありません。
2. 小型株は1日で20〜30%動くことがあります。
3. A株は政策影響が極めて大きく、規制動向に要注意。
4. サプライチェーン情報はノイズが多く、独自検証が必須。
5. ロジックの検証には1〜3年かかる場合があります。

---

## 参考文献

- [yan-labs/serenity-aleabitoreddit](https://github.com/yan-labs/serenity-aleabitoreddit) — Serenityツイートのコーパス蒸留（2025-07→2026-09：6,592ツイート＋4記事、メソドロジーと戦績タイムライン）
- [SerenityオリジナルSkill（英語）](https://github.com/leslieyeo/aleabitoreddit-skill)
- [semiconstocks.com トラッカー](https://semiconstocks.com/zh)
- [Singularity Research Fund](https://singularityresearchfund.substack.com)
