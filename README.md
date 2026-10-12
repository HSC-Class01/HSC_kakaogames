[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97-%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C_%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-2463eb?style=for-the-badge)](https://ghkdtpcks00-ux.github.io/townboy/)

> **업로드:** ZIP 안의 `.github` 폴더는 GitHub Actions가 반드시 요구하는 경로입니다. 압축파일에는 숨김 속성 파일이 없지만, 이름이 점으로 시작하는 `.github` 디렉터리는 필수입니다. 웹 업로드에서 폴더가 누락된다면 GitHub 웹 편집기로 `.github/workflows/update.yml`과 `pages.yml`을 각각 생성하세요.

[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97-%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C_%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-2563eb?style=for-the-badge)](https://ghkdtpcks00-ux.github.io/townboy/)

# 카카오게임즈 OpenDART 재무분석 Agent

**대시보드:** https://ghkdtpcks00-ux.github.io/townboy/

## 설치 및 배포
1. ZIP을 압축 해제한 뒤 **내부 파일과 폴더**를 GitHub 저장소 `ghkdtpcks00-ux/townboy`의 `main` 브랜치 루트에 업로드합니다.
2. ZIP의 `github/workflows` 디렉터리를 GitHub 웹사이트에서 **`.github/workflows`**로 이동하거나 이름을 바꾸세요. 숨김 파일 없는 ZIP 요청 때문에 워크플로우는 `github/workflows`에 제공됩니다. GitHub Actions 실행에는 반드시 `.github/workflows` 경로가 필요합니다.
3. GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret에서 이름 `DART_API_KEY`로 OpenDART API 키를 입력합니다. **코드나 README에 키를 넣지 마세요.**
4. Settings → Actions → General → Workflow permissions에서 **Read and write permissions**를 선택합니다. 조직 정책이 이를 막으면 별도 PAT 기반 인증 설정이 필요합니다.
5. Settings → Pages → Build and deployment → Source에서 **GitHub Actions**를 선택합니다.
6. Actions → Update DART financial data → Run workflow를 먼저 실행합니다. 데이터 수집이 완료되면 commit/push에 따라 Pages가 배포됩니다. 필요시 Deploy dashboard 워크플로우도 수동 실행합니다.
7. 저장소 오른쪽 **About → 톱니바퀴 → Website**에 `https://ghkdtpcks00-ux.github.io/townboy/`를 입력하고 저장합니다. 이는 저장소 관리자가 수동으로 설정해야 합니다.

## 업데이트
- 매월 1일 **09:15 KST** (00:15 UTC) GitHub Actions 실행. GitHub 스케줄은 혼잡 시 지연될 수 있습니다.
- 사업보고서 FY(11011), 반기 H1(11012), 1분기 Q1(11013), 3분기 Q3(11014) 수집.
- 연결(CFS) 우선, 없으면 별도(OFS). 2010년부터 조회하며 미공시 연도는 생략.
- 원본: `data/raw`, 정규화 결과: `data/processed/financials.json`.
- 손익은 누적 공시 금액입니다. Quarterly 표는 Q1/Q3 보고서 데이터이며 **Q2/Q4 단독분기 자료가 아닙니다.**
- 재무비율은 단순 산식이며 회계정책·업종 차이와 누적 기간에 주의하세요.

## 국내 Peer Firms
| 기업 | 종목코드 | 비교 사업 |
|---|---|---|
| 크래프톤 | 259960 | 글로벌 게임 개발·퍼블리싱 |
| 넷마블 | 251270 | 모바일 게임 퍼블리싱 |
| 엔씨소프트 | 036570 | MMORPG 개발·서비스 |
| 펄어비스 | 263750 | PC·콘솔 게임 개발 |
| 위메이드 | 112040 | MMORPG·IP 사업 |
| 네오위즈 | 095660 | PC·콘솔·모바일 게임 |
| 컴투스 | 078340 | 모바일 게임 개발·퍼블리싱 |

## 유의사항
- 이 ZIP은 **실행용 소스코드**이며 API 키가 없으므로 실제 공시 데이터는 아직 포함하지 않습니다.
- 첨부 재무비율 가이드와 배지 이미지는 이 대화에서 확인되지 않아 표준 지표 및 shields.io 배지로 구성했습니다.
- GitHub 저장소의 실제 설정 변경이나 배포 완료는 이 ZIP만으로 자동 수행되지 않습니다.


## 첨부 실무가이드 반영 내용
재무상태표·손익계산서·현금흐름표 핵심 수치, 수익성(매출총이익률/영업이익률/순이익률/ROA/ROE), 유동성·안정성(유동/당좌/부채/자기자본/차입금의존도/이자보상배율), 성장성·활동성(매출성장률/총자산회전율/DSO/DIO), FCF·순차입금을 포함합니다. 연간·반기·분기 각각 범주별 테이블을 제공합니다.

**자료 부족 시 결측:** EBITDA/EBITDA 마진/ROIC/순차입금 대비 EBITDA, DPO/CCC, PER/PBR/EV·EBITDA/FCF 수익률은 감가상각·외상매입액·주가/주식수 등 검증된 추가 자료가 없으면 계산하지 않습니다. 이자부차입금은 단기·장기차입금 부분합으로 리스부채/사채가 빠질 수 있습니다. CAPEX는 유형·무형자산 취득액이 모두 확인될 때만 산출합니다. ROE/ROA/회전율은 동일 연결/별도 기준의 전년말·당기말 평균 잔액을 사용하고 반기/분기는 연환산 참고치입니다. 손익 및 현금흐름 분기 값은 누적 금액입니다.

## 최초 실행
1. 저장소에 파일 업로드 (`.github/workflows/` 경로 필수)
2. Settings → Secrets and variables → Actions → New repository secret: `DART_API_KEY`
3. Settings → Pages → Source: GitHub Actions
4. Actions → Update DART financial data → Run workflow
5. Settings 또는 About → Website에 `https://ghkdtpcks00-ux.github.io/townboy/` 등록 (About 설정은 수동)
6. 자동 업데이트: 매월 1일 한국시간 09:15 (UTC 00:15); GitHub 예약 작업은 지연될 수 있음

**주의:** ZIP은 소스코드이며 API 키를 포함하지 않습니다. 실제 데이터 수집/배포는 사용자의 저장소에서 최초 실행 후 확인하세요.
