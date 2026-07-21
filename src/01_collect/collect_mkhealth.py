"""매경헬스 기사 수집 (idxno 순차 순회 방식).

- 기사 URL: http://www.mkhealth.co.kr/news/articleView.html?idxno=N
- idxno=1이 2015-03-02, 현재 약 79,000번대
- 결번/삭제 기사 존재 → 건너뛰기
- 기사 페이지에 섹션 정보 없음 → 수집 후 사후 분류
"""
import csv
import time
import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.mkhealth.co.kr/news/articleView.html?idxno={}"
HEADERS = {"User-Agent": "Mozilla/5.0 (research crawler; contact: estherish@snu.ac.kr)"}
OUT_DIR = Path("data/raw/mkhealth")


def parse_article(html, idxno):
    """기사 HTML에서 필요한 필드를 추출. 기사가 아니면 None 반환."""
    soup = BeautifulSoup(html, "html.parser")

    body_tag = soup.select_one("article#article-view-content-div")
    if body_tag is None:
        return None  # 삭제됐거나 기사 페이지가 아님

    # 사진 캡션(figure)은 본문에서 제거
    for fig in body_tag.find_all("figure"):
        fig.decompose()
    body = "\n".join(
        p.get_text(strip=True) for p in body_tag.find_all("p") if p.get_text(strip=True)
    )

    title_tag = soup.select_one("h1.heading")
    subtitle_tag = soup.select_one("h4.subheading")

    # 게재일: <li><i class="icon-clock-o"></i> 입력 2022.09.26 08:33</li>
    date = ""
    clock = soup.select_one("i.icon-clock-o")
    if clock and clock.parent:
        date = clock.parent.get_text(strip=True).replace("입력", "").strip()

    return {
        "idxno": idxno,
        "url": BASE_URL.format(idxno),
        "title": title_tag.get_text(strip=True) if title_tag else "",
        "subtitle": subtitle_tag.get_text(strip=True) if subtitle_tag else "",
        "date": date,
        "body": body,
    }


def collect(start, end, delay=1.0):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"mkhealth_{start}_{end}.csv"

    fields = ["idxno", "title", "subtitle", "date", "url", "body"]
    ok = skipped = failed = 0

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for n in range(start, end + 1):
            try:
                r = requests.get(BASE_URL.format(n), headers=HEADERS, timeout=10)
                if r.status_code != 200:
                    failed += 1
                    continue
                article = parse_article(r.text, n)
                if article is None:
                    skipped += 1
                else:
                    writer.writerow(article)
                    ok += 1
            except requests.RequestException as e:
                failed += 1
                print(f"  [오류] idxno={n}: {e}")

            if n % 20 == 0:
                print(f"  진행 {n}/{end} (수집 {ok} / 결번 {skipped} / 실패 {failed})")
            time.sleep(delay)

    print(f"\n완료: {ok}건 수집 → {out_path}")
    print(f"결번 {skipped}건, 실패 {failed}건")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--delay", type=float, default=1.0)
    args = ap.parse_args()
    collect(args.start, args.end, args.delay)
