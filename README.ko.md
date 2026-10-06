# Serenity Stock Choke · A주식/홍콩주/미국주 공급망 병목(초크포인트) 투자 프레임워크

<p align="center"><a href="README.md">简体中文</a> · <a href="README.en.md">English</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b></p>

> "**공급망을 상류로 거슬러 올라가 '그곳이 끊기면 조 단위 산업이 멈추는' 핵심 노드를 찾아라 — 그 노드에 앉아 있는 소형주가 다음 대박의 기회다.**"

이 스킬은 Reddit의 전설적인 트레이더 **Serenity(@aleabitoreddit)** 의 공급망 병목 이론을 **A주식·홍콩주·미국주** 3개 시장에 적용한 범용 산업 분석 프레임워크입니다. Serenity의 원조 전적은 미국주(AXTI, AAOI)이며, A주식 버전은 그 현지화입니다.

---

## 핵심 방법론

### "호르무즈 해협" 아날로지

> "호르무즈 해협은 세계 석유의 목구멍이다. 봉쇄되면 모두가 영향을 받는다. 하지만 호르무즈 해협 자체에 주식을 갖고 있다면, 가격 결정권을 쥐게 된다."

**투자로의 번역**: 어떤 거대 트랙의 "호르무즈"는 어느 노드인가 — 그것을 지배하는 상장사(A주/홍콩주/미국주)는 어디인가?

### 3단계 핵심 로직

```
① AI 폭발 / 정책 드라이브 / 기술 도약
    ↓
② 상류 하드웨어·소재 수요 폭증, 공급망 일부가 따라가지 못함
    ↓
③ 병목 노드가 가격 결정권 확보 → 그곳의 소형주 변동성(상승 탄력)이 최대
```

### Serenity의 실적 (미국주 · 참고)

| 종목 | 티커 | 초크포인트 포지셔닝 |
|------|------|-------------------|
| AXT Inc | AXTI.US | InP 기판 글로벌 톱3 제조사 중 하나 |
| Applied Optoelectronics | AAOI.US | CPO 레이저 주요 공급사 |
| Sivers Semiconductors | SIVE.SE | CPO 레이저 + 실리콘 포토닉스 |
| X-FAB | XFAB.EU | 특수공정 파운드리 |

> ⚠️ 위 표는 **사후 관점의 생존 편향 샘플**로, 프레임워크 로직 설명용입니다. 프레임워크의 기대수익률을 대표하지 않습니다.

---

## 6단계 분석 파이프라인

| 단계 | 질문 | 산출물 |
|------|------|--------|
| 1️⃣ 사이클 단계 | 수요 폭발 / 기술 도약 / 공급 제약 중 무엇인가? | 섹터 단계 판정 |
| 2️⃣ 공급망 추적 | 어느 층이 병목인가? | 공급망 계층 지도 |
| 3️⃣ 상장사 발굴 | 그 노드에 앉은 기업은 누구인가? (A/홍콩/미) | 4요소 시그널 카드 |
| 4️⃣ 진위 스크리닝 | 진짜 병목인가, 테마 편승인가? | 7대 제외 규칙으로 판정 |
| 5️⃣ 양방향 확인 | 강세 시그널 vs 약세 시그널? | 시그널 대조표 |
| 6️⃣ 리포트 | 포지션 설계 + 리스크 | 구조화 리포트 (8섹션) |

---

## 지원 시장

| 시장 | 시세·밸류에이션 (`stock`/`search`) | 섹터 K라인 | 리서치/신용융자/칩 |
|------|:---:|:---:|:---:|
| **A주식** | ✅ 주력 자금유입 포함 | ✅ | ✅ |
| **홍콩주** | ✅ HKD 표기 | — | 웹 검색으로 대체 |
| **미국주** | ✅ USD 표기 · 중국어명 지원 | — | 웹 검색으로 대체 |

6단계 프레임워크 자체는 시장 비의존적입니다. 홍콩·미국 기관 시그널(13F, 공매도 잔고, 남향 자금, 공매도 비율)은 SKILL.md의 검색 템플릿을 사용하세요. **13F는 45일 지연(분기), 공매도 잔고는 격주 발표**임에 유의하세요.

---

## 빠른 시작

### 설치 (하나만 선택)

**방법 0 — AI 에이전트에 한마디 던지기 (가장 간단)**. 아래 문장을 Claude Code / Codex 등 명령 실행 가능한 에이전트에 붙여넣으면, 자동으로 클론·설치·검증까지 수행합니다:

```
https://github.com/fadewalk/serenity-stock-choke 스킬을 설치해줘:
이 에이전트의 스킬 디렉터리(Claude Code: ~/.claude/skills/,
기타: .agents/skills/, 불확실하면 저장소 README 참조)에 클론하고,
python3 <skill-dir>/scripts/a_stock_query.py stock 600519 로 동작 확인 후,
이 스킬 사용법과 할 수 있는 일을 알려줘.
```

**방법 1 — Claude Code 플러그인 마켓:**

```
/plugin marketplace add fadewalk/serenity-stock-choke
/plugin install serenity-stock-choke@serenity-stock-choke
```

**방법 2 — skills.sh 설치기:**

```bash
npx skills add fadewalk/serenity-stock-choke
```

**방법 3 — 수동 클론:**

```bash
git clone https://github.com/fadewalk/serenity-stock-choke.git ~/.claude/skills/serenity-stock-choke
```

번들 쿼리 스크립트는 Python 표준 라이브러리만 사용 — 의존성 없음, API 키 불필요 (`akshare` 선택: `pip install akshare`).

### 트리거 방법

```
serenity-stock-choke 로 [섹터] 분석해줘
예: serenity-stock-choke 로 미국 AI 컴퓨트 공급망 분석해줘
[산업] 의 병목 지점을 찾아줘
```

### 데이터 접근 (3단계 폴백, 어느 환경에서든 동작)

1. **에이전트 내장 금융 도구** (MCP 시세·리서치 도구) — 있으면 최우선
2. **번들 스크립트** (`scripts/a_stock_query.py`, 제로 의존성·멀티소스 자동 전환):
   ```bash
   python3 scripts/a_stock_query.py stock 600519     # A주 스냅샷: 가격/PER/PB/시총/자금유입
   python3 scripts/a_stock_query.py stock 00700      # 홍콩주: 텐센트 (HKD)
   python3 scripts/a_stock_query.py stock AAPL       # 미국주: 애플 (USD)
   python3 scripts/a_stock_query.py valuation 600519 # A주 PER/PB 역사 백분위
   python3 scripts/a_stock_query.py kline 300308     # 모멘텀/연율 변동성/최대 낙폭
   python3 scripts/a_stock_query.py business 600519  # A주 매출 구성 (테마 편승 체크)
   python3 scripts/a_stock_query.py sector 电力       # A주 섹터 K라인
   python3 scripts/a_stock_query.py reports 600519   # A주 증권사 리서치
   python3 scripts/a_stock_query.py margin 600519    # A주 신용융자 잔고
   ```
3. **웹 검색 폴백**: 공급 갭·정책·칩 분포·13F·공매도 등은 SKILL.md 템플릿 사용

## 파일 구조

```
serenity-stock-choke/
├── SKILL.md                    # 메인 프롬프트 (6단계 + 3단계 데이터 전략)
├── README.md                   # 简体中文版
├── README.en.md                # English
├── README.ja.md                # 日本語版
├── README.ko.md                # 이 파일
├── .claude-plugin/             # Claude Code 플러그인 (원클릭 설치)
├── scripts/
│   └── a_stock_query.py        # 독립 데이터 스크립트 (제로 의존성·A/홍콩/미 지원)
└── references/
    └── user_guide.md          # 사용 가이드 (중국어)
```

---

## 리스크 고지

1. 연구 참고용이며 투자 자문이 아닙니다.
2. 소형주는 하루에 20~30% 움직일 수 있습니다.
3. A주식은 정책 영향이 매우 크므로 규제 동향에 주의하세요.
4. 공급망 정보는 노이즈가 많아 독자적 검증이 필수입니다.
5. 로직 검증에는 1~3년이 걸릴 수 있습니다.

---

## 참고 자료

- [yan-labs/serenity-aleabitoreddit](https://github.com/yan-labs/serenity-aleabitoreddit) — Serenity 트윗 코퍼스 증류 (2025-07→2026-09: 6,592개 트윗 + 4편 아티클, 방법론·전적 타임라인)
- [Serenity 오리지널 Skill (영어)](https://github.com/leslieyeo/aleabitoreddit-skill)
- [semiconstocks.com 트래커](https://semiconstocks.com/zh)
- [Singularity Research Fund](https://singularityresearchfund.substack.com)
