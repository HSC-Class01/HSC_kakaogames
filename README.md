[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C_%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-2563eb?style=for-the-badge)](https://hsc-class01.github.io/HSC_kakaogames/)

# 카카오게임즈 DART Financial Intelligence

대상 저장소: https://github.com/HSC-Class01/HSC_kakaogames

대시보드: https://hsc-class01.github.io/HSC_kakaogames/ (배포 후 활성화)

## 가장 중요한 업로드 방법 (숨김 폴더 없는 ZIP)

이 ZIP에는 숨김 파일/폴더가 **없습니다**. `workflows/update.yml`과 `workflows/pages.yml`은 GitHub Actions에서 바로 실행되지 않습니다. GitHub 저장소의 웹 UI에서 `Add file → Create new file`을 눌러 **`.github/workflows/update.yml`**, **`.github/workflows/pages.yml`**이라는 이름으로 각각 만들고, ZIP 안 `workflows` 파일 내용을 복사해 저장하세요. GitHub는 경로에 `.github`가 반드시 있어야 합니다.

나머지 `scripts`, `docs`, `requirements.txt`, `README.md`는 저장소 최상위에 업로드합니다.

## API 키 등록

1. https://opendart.fss.or.kr/ 에서 API 인증키를 발급받습니다.
2. 저장소 `Settings → Secrets and variables → Actions → New repository secret`으로 이동합니다.
3. 이름은 **DART_API_KEY**, 값은 발급받은 API 인증키로 입력합니다. 코드를 수정하거나 키를 커밋하지 마세요.
4. `Settings → Actions → General → Workflow permissions`에서 **Read and write permissions**을 허용합니다(조직 정책에 따라 관리자 권한 필요).
5. `Settings → Pages → Build and deployment → Source`를 **GitHub Actions**로 선택합니다.
6. `Actions → Update DART financial data → Run workflow`를 실행합니다. 수집 완료 후 `Deploy dashboard to GitHub Pages`가 자동 실행되며, 필요하면 수동 실행할 수 있습니다.
7. 저장소 오른쪽 **About → 톱니바퀴 → Website**에 `https://hsc-class01.github.io/HSC_kakaogames/`를 입력하고 저장합니다. 이는 저장소 관리자 권한이 필요합니다.

## 자동 갱신

매월 1일 UTC 00:15 (한국시간 오전 9:15) GitHub Actions가 공시 API를 조회합니다. GitHub 예약 작업은 지연되거나 상황에 따라 누락될 수 있으므로 Actions 실행 이력을 확인하세요. 2010년부터 연간(11011), 반기(11012), 1분기(11013), 3분기(11014) 보고서의 재무제표를 조회하며, 실제로 제공되지 않는 연도는 비워둡니다.

## 분석 가이드 적용 및 주의

첨부된 「재무제표 및 재무비율 실무 가이드」를 함께 포함했습니다. 재무상태표, 손익계산서, 현금흐름표의 원천 수치를 추출하고 수익성·유동성·안정성·성장성 비율을 계산합니다. 연결(CFS)을 우선 사용하고 없으면 별도(OFS)를 사용합니다. 서로 다른 회계 범위는 시계열 비교하지 않습니다. Q1/H1/Q3 손익·현금흐름 수치는 **누적**입니다. ROA/ROE/회전율의 중간기간 수치는 단순 연환산 참고치이며 정확한 기간 평균잔액 방식과 차이가 있습니다. DPO·CCC·EBITDA·ROIC·PER·PBR·EV/EBITDA 등 충분한 원천 데이터가 없는 지표는 임의로 만들지 않고 `—`로 표시합니다. 차입금은 공시 계정 중 단기·장기차입금으로 확인되는 범위만 합산하므로 회사의 모든 이자부부채를 포괄하지 않을 수 있습니다.

### 국내 비교기업 (Peer Firms)

| 회사 | 종목코드 | 비교 분야 |
|---|---|---|
| 크래프톤 | 259960 | 게임 개발 및 퍼블리싱 |
| 넷마블 | 251270 | 모바일 게임 |
| 엔씨소프트 | 036570 | MMORPG |
| 펄어비스 | 263750 | PC·콘솔 게임 |
| 위메이드 | 112040 | MMORPG·IP |
| 네오위즈 | 095660 | PC·콘솔 게임 |
| 컴투스 | 078340 | 모바일 게임 |

Peer Firms 표는 비교대상 목록이며 동종기업 재무수치 수집까지 포함하는 것은 아닙니다.

## 로컬 실행

`pip install -r requirements.txt` 실행 후 `DART_API_KEY` 환경변수를 설정하고 `python scripts/update.py`를 실행합니다. API 인증키가 없는 경우 데이터가 생성되지 않습니다.
