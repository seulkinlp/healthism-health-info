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

## 2026-07-17 (2차, 맥미니)
- 확정: 매경헬스 소급 수집 가능 — idxno 순차 URL, idxno=1이 2015-03-02 (연구기간 시작과 일치)
- 확인: robots.txt는 admin/member 등 내부 경로만 차단, 기사 경로 개방
- 주의: 초기 번호대 published_time 메타태그가 이관일로 통일된 정황 → 본문 날짜 파싱 필요
- 주의: 초기 번호대에 비건강 기사 혼재(예: idxno=5000 통신 기사) → 건강 기사 필터 필요
- 주의: 결번 존재(50000, 70000 빈 출력) → 순회 시 스킵 로직 필요
- 다음: ① 매경헬스 수집 스크립트 작성(collect_mkhealth.py, idxno 순회 방식) ② 헬스경향·코메디닷컴 정찰
- 매경헬스 파싱 대상 확정: 본문 `article#article-view-content-div` (itemprop=articleBody, <p> 단위 / <figure>는 캡션이라 제외), 제목 `h1.heading`, 부제 `h4.subheading`, 게재일 705행 형태 `<li><i class="icon-clock-o"></i> 입력 YYYY.MM.DD HH:MM</li>`, 기자명 info-group 내 링크
- 확인: 기사 페이지 breadcrumb은 '홈>뉴스'까지만 — 서브섹션(건강·질병 등) 판별 불가
- 다음 세션 첫 확인: 섹션별 목록페이지(articleList.html?sc_sub_section_code=S2N46) 과거 페이지네이션 가능 여부
  → 가능하면 섹션 순회 방식(정확), 불가하면 idxno 순회 + 사후 키워드 분류
- 검증 예정: 초기 idxno 기사 날짜 신뢰성 — 사진 URL의 photo/YYYYMM 경로와 대조
