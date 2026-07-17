"""네이버 뉴스 검색 API 소급 범위 테스트.

질문: '헬스조선' 검색으로 start=1000까지 갔을 때
      pubDate가 얼마나 과거까지 닿는가?
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # .env에서 키 읽기

URL = "https://openapi.naver.com/v1/search/news.json"
HEADERS = {
    "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
    "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET"),
}

def search(query, start=1, display=100, sort="date"):
    params = {"query": query, "start": start, "display": display, "sort": sort}
    r = requests.get(URL, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    query = "헬스조선"

    # 1) 첫 페이지: API 작동 확인 + 전체 검색 결과 수
    first = search(query, start=1)
    print(f"전체 검색 결과 수(total): {first['total']}")
    print(f"첫 기사 pubDate: {first['items'][0]['pubDate']}")

    # 2) 마지막 페이지(start=1000): 도달 가능한 가장 오래된 기사
    last = search(query, start=1000)
    items = last["items"]
    print(f"\nstart=1000 페이지 기사 수: {len(items)}")
    if items:
        print(f"가장 오래된 pubDate: {items[-1]['pubDate']}")

    # 3) 헬스조선 원문 기사 비율 확인
    hc = [i for i in items if "health.chosun.com" in i.get("originallink", "")]
    print(f"이 중 health.chosun.com 원문: {len(hc)}건")
    for i in hc[:3]:
        print(" -", i["pubDate"], "|", i["title"][:40])
