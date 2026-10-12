[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗_대시보드_바로가기-2563eb?style=for-the-badge)](https://hsc-class01.github.io/HSC_kakaogames/)

# 카카오게임즈 DART Financial Intelligence

카카오게임즈(293490)의 OpenDART 공시 재무제표를 수집하고 주요 재무수치와 재무비율을 분석하는 프로젝트입니다.

- **🔗 대시보드:** https://hsc-class01.github.io/HSC_kakaogames/
- **저장소:** https://github.com/HSC-Class01/HSC_kakaogames
- **대상 기간:** 2010년부터 현재까지 조회 시도
- **보고서:** 사업보고서(FY), 반기보고서(H1), 1분기(Q1), 3분기(Q3)
- **자동 업데이트:** 매월 1일 00:15 UTC (한국시간 오전 9:15), 또는 GitHub Actions에서 수동 실행

## 대시보드 구성

상단에는 연간 매출액·영업이익 및 영업이익률·순이익률 추세와 최신 연간 주요 KPI를 표시합니다. 하단에는 **Annual, Half-year, Quarterly** 세 구분별로 재무상태표, 손익계산서, 현금흐름, 수익성·효율, 안정성·성장성, 시장가치 지표를 표로 제공합니다. 넓은 표는 가로 스크롤할 수 있습니다.

주요 수집 항목에는 매출액, 매출원가, 매출총이익, 판매비와관리비, 영업이익, 세전이익, 순이익, 지배주주순이익, 총자산, 유동자산, 현금, 매출채권, 재고자산, 유형자산, 총부채, 자본, 차입금, 영업·투자·재무 현금흐름 및 CAPEX/FCF가 포함됩니다. 계산 가능한 범위에서 매출총이익률, 영업이익률, 순이익률, 유동비율, 당좌비율, 부채비율, 자기자본비율, 차입금의존도, 이자보상배율, ROA, ROE, 자산회전율, 매출증가율 등을 산출합니다.

## OpenDART API 키 등록

1. [OpenDART](https://opendart.fss.or.kr/)에서 API 인증키를 발급받습니다.
2. GitHub 저장소의 **Settings → Secrets and variables → Actions → New repository secret**으로 이동합니다.
3. Secret 이름을 정확히 `DART_API_KEY`로 입력하고, 값에 발급받은 인증키를 붙여넣은 뒤 저장합니다.
4. 인증키를 코드, README, CSV/JSON 또는 공개 파일에 입력하지 마세요.
5. **Actions → Kakao Games DART update and GitHub Pages deploy → Run workflow**를 실행해 최초 데이터를 수집합니다.
6. **Settings → Pages → Build and deployment → Source**가 **GitHub Actions**인지 확인합니다.
7. 실행이 끝나면 [대시보드](https://hsc-class01.github.io/HSC_kakaogames/)를 확인합니다. 최초 수집에는 시간이 걸릴 수 있습니다.

조직 정책상 Actions 실행 권한이나 저장소 쓰기 권한이 제한되어 있으면 저장소 관리자가 권한을 확인해야 합니다.

## 자동화 및 데이터 저장

- `scripts/update.py`: OpenDART 기업코드 조회, 재무제표 수집, 지표 계산
- `data/raw/`: 보고서별 API 응답 원자료(JSON)
- `data/processed/financials.json`: 대시보드에서 사용하는 정리된 재무 데이터
- `.github/workflows/monthly_update.yml`: 월간 실행, 검증, 데이터 커밋 및 GitHub Pages 배포

워크플로는 매월 1일 UTC 00:15에 실행됩니다(한국시간 오전 9:15). 예약 실행은 GitHub 사정에 따라 지연될 수 있습니다. **Actions** 탭에서 실행 결과와 오류 로그를 확인할 수 있습니다.

## 기간 및 회계 데이터 해석 시 주의사항

- OpenDART 구조화 재무 API는 통상 2015년 이후 데이터가 중심입니다. 2010~2014년은 API가 반환하지 않는 재무수치를 임의로 채우지 않으며, 데이터가 없는 기간은 공란으로 남습니다.
- 연결재무제표(CFS)를 우선 조회하고 사용할 수 없으면 별도재무제표(OFS)를 대체 사용합니다. 회계 범위가 다른 관측치는 직접 비교할 때 주의해야 하며, 각 행에 CFS/OFS 구분을 표시합니다.
- Q1, H1, Q3의 손익 및 현금흐름 항목은 각각 3개월·6개월·9개월 누적 금액이지 단독 분기 금액이 아닙니다. 연간은 FY로 표시합니다.
- ROA, ROE 및 자산회전율은 공시 가능한 전년 말 잔액과 당기 잔액을 사용한 참고치이며, 중간기간 수치는 연환산합니다.
- CAPEX는 확인 가능한 유형자산·무형자산 취득액을 사용합니다. 원천 계정이 불충분한 지표는 추정해 채우지 않고 결측으로 둡니다. 차입금도 공시 계정으로 확인되는 단기·장기 차입금 범위이므로 모든 이자부부채를 포괄하지 않을 수 있습니다.
- PER, PBR, EV/EBITDA, EBITDA, ROIC, DPO, CCC 등은 필요한 시장가격 또는 충분한 원천 계정이 없는 경우 대시(—)로 표시합니다. 이는 0을 의미하지 않습니다.
- 금액은 대시보드에서 억원 단위로 표시합니다. 비율의 정의와 분모를 확인한 뒤 다른 데이터베이스 수치와 비교하세요.

## 국내 Peer Firms

| 기업 | 종목코드 | 비교 분야 |
|---|---:|---|
| 크래프톤 | 259960 | 글로벌 게임 개발·퍼블리싱 |
| 넷마블 | 251270 | 모바일 게임 퍼블리싱 |
| 엔씨소프트 | 036570 | MMORPG 개발·서비스 |
| 펄어비스 | 263750 | PC·콘솔 게임 개발 |
| 위메이드 | 112040 | MMORPG·게임 IP |
| 네오위즈 | 095660 | PC·콘솔·모바일 게임 |
| 컴투스 | 078340 | 모바일 게임 개발·퍼블리싱 |

Peer Firms 표는 비교 대상 목록이며, 현재 자동 수집되는 재무 데이터는 카카오게임즈 기준입니다. 동종기업의 재무수치 자동수집 및 동시 비교는 포함하지 않습니다.

## ZIP 패키지 및 숨김 파일

에이전트 ZIP을 별도로 배포할 때는 `.github` 같은 숨김 경로를 ZIP 내부에 포함하지 않고, 워크플로 파일은 GitHub 웹에서 `.github/workflows/monthly_update.yml` 경로로 생성하는 절차를 안내합니다. 다만 **GitHub Actions가 실행될 때는 워크플로 파일이 저장소의 해당 경로에 반드시 있어야 합니다.**

## 로컬 실행

```bash
python -m pip install -r requirements.txt
# macOS/Linux
export DART_API_KEY="발급받은_API_키"
# Windows PowerShell
$env:DART_API_KEY="발급받은_API_키"
python scripts/update.py
```

데이터는 OpenDART API 응답에 따라 달라질 수 있으며, 이 프로젝트는 회계·투자 자문이 아닌 공시 기반 분석 도구입니다.
