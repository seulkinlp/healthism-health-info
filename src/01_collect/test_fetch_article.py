"""헬스조선 기사 1건 수집 테스트: div.par에서 본문 추출이 되는지 확인"""
import requests
from bs4 import BeautifulSoup

URL = "https://health.chosun.com/site/data/html_dir/2026/07/14/2026071402610.html"

# User-Agent: 우리가 누구인지 밝히는 이름표 (연구용 크롤러임을 명시)
HEADERS = {"User-Agent": "HealthismResearchBot/0.1 (academic research)"}

resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()          # 200 OK가 아니면 에러 발생
resp.encoding = "utf-8"          # 한글 깨짐 방지

soup = BeautifulSoup(resp.text, "lxml")

title = soup.select_one("h1")    # 제목 후보 (안 맞으면 조정)
body = soup.select_one("div.par")  # 아까 확인한 본문 컨테이너

print("=== 제목 ===")
print(title.get_text(strip=True) if title else "h1 없음 - 다른 태그 찾아야 함")
print("\n=== 본문 앞 300자 ===")
print(body.get_text(strip=True)[:300] if body else "div.par 없음!")