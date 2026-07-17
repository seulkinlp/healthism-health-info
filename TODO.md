# 연구 세션 로그

## 2026-07-15
- 완료: 헬스조선 수집 스크립트(collect_healthchosun.py) 작성, 파일럿 100건 수집
- 완료: 맥북 작업 환경 세팅 (~/research/healthism-health-info로 통일, .venv 생성)
- 확인됨: 헬스조선 과거 사이트맵 없음(404) → 소급 수집은 네이버 뉴스 API 테스트로
- 교훈: clone 직후 gitignore된 data/ 폴더는 직접 mkdir 필요 / 세션 시작 시 git pull 필수
- 교훈: zsh에서 소문자 path는 PATH 예약 변수 (반복문 변수명 주의)
- 다음: ① 네이버 뉴스 API 소급 테스트 ② 매경헬스 robots.txt 확인 ③ 홈 폴더 정리(별도)

## 2026-07-17 (맥미니)
- 완료: 네이버 뉴스 API 테스트 (test_naver_api.py)
- 확정: 네이버 API 소급 불가 — start 상한 1000으로 최신 ~1,100건, 약 3개월 전까지만 도달
- 확정: 전문지 소급 수집 종결 → 확보 가능 기간만 분석, 장기추세(2015~2025)는 빅카인즈로 커버
- 교훈: 가상환경은 git 동기화 안 됨 — 새 컴퓨터에서 pip install -r requirements.txt 필요
- 다음: ① 매경헬스 robots.txt 확인 ② 헬스조선 정기 수집 계속 + URL 중복 제거 로직
