import urllib.request
import feedparser
import re

# 1. 티스토리 RSS 주소
url = "https://chanhuy.tistory.com/rss"

# 2. 406 에러(봇 차단) 우회를 위해 일반 브라우저처럼 User-Agent 헤더 추가
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'})
response = urllib.request.urlopen(req)
xml_data = response.read()

# 3. RSS 피드 파싱
feed = feedparser.parse(xml_data)

# 4. 최신 글 5개를 마크다운 리스트 형식으로 변환
latest_posts = ""
for entry in feed.entries[:5]:
    latest_posts += f"- [{entry.title}]({entry.link})\n"

# 5. README.md 파일 읽기
with open("README.md", "r", encoding="utf-8") as f:
    readme_text = f.read()

# 6. 정규식을 사용해 주석 사이의 내용을 새 블로그 글 목록으로 교체
readme_text = re.sub(
    r"<!-- BLOG-POST-LIST:START -->.*<!-- BLOG-POST-LIST:END -->",
    f"<!-- BLOG-POST-LIST:START -->\n{latest_posts}<!-- BLOG-POST-LIST:END -->",
    readme_text,
    flags=re.DOTALL
)

# 7. 수정된 내용을 README.md에 덮어쓰기
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_text)