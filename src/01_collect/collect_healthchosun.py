"""헬스조선 뉴스 사이트맵 기반 기사 수집 (파일럿)
사용법: 프로젝트 루트에서 python src/01_collect/collect_healthchosun.py
"""
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

SITEMAP_URL = "https://health.chosun.com/rss/healthchosunRss_utf8.xml"
HEADERS = {"User-Agent": "HealthismResearchBot/0.1 (academic research)"}
DELAY_SEC = 2  # 요청 간격: 서버 부하 예방의 핵심
OUT_DIR = Path("data/raw/healthchosun")

def get_article_urls():
    """사이트맵에서 (URL, 제목, 발행일) 목록 추출"""
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "xml")  # XML 모드로 파싱
    items = []
    for url_tag in soup.find_all("url"):
        loc = url_tag.find("loc")
        title = url_tag.find("news:title")
        pubdate = url_tag.find("news:publication_date")
        if loc:
            items.append({
                "url": loc.get_text(strip=True),
                "title": title.get_text(strip=True) if title else "",
                "pub_date": pubdate.get_text(strip=True) if pubdate else "",
            })
    return items

def fetch_body(url):
    """개별 기사에서 본문 추출"""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    body = soup.select_one("div.par")
    return body.get_text(strip=True) if body else ""

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = get_article_urls()
    print(f"사이트맵에서 {len(items)}건의 기사 URL 확보")

    rows = []
    for i, item in enumerate(items, 1):
        try:
            body = fetch_body(item["url"])
            rows.append({**item, "body": body, "source": "헬스조선"})
            print(f"[{i}/{len(items)}] OK: {item['title'][:30]}")
        except Exception as e:
            print(f"[{i}/{len(items)}] 실패: {item['url']} ({e})")
        time.sleep(DELAY_SEC)  # 매 요청 사이 2초 대기

    df = pd.DataFrame(rows)
    out_path = OUT_DIR / f"healthchosun_{pd.Timestamp.now():%Y%m%d}.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n저장 완료: {out_path} ({len(df)}건)")

if __name__ == "__main__":
    main()