import datetime
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.models.url_metadata import UrlMetadata
from app.utils.config import (
    SOCIAL_MEDIA_WEBSITE_PATTERNS,
    VIDEO_WEBSITE_PATTERNS
)


def get_html_text_length(html: str) -> int:
    if html is None:
        return 0
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return len(text)


def format_telegram_short_text(soup: BeautifulSoup) -> BeautifulSoup:
    decompose_list = ["br"]
    unwrap_list = ["span", "div", "blockquote", "h2"]
    for decompose in decompose_list:
        for item in soup.find_all(decompose):
            item.decompose()
    for unwrap in unwrap_list:
        for item in soup.find_all(unwrap):
            item.unwrap()
    return soup


def unix_timestamp_to_utc(timestamp: int) -> str:
    utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    beijing_time = utc_time + datetime.timedelta(hours=8)
    return beijing_time.strftime("%Y-%m-%d %H:%M")


def second_to_time(second: int) -> str:
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)


async def check_url_type(url: str) -> UrlMetadata:
    url_object = urlparse(url)
    url_host = url_object.hostname
    category, url_type = None, None
    # check if the url is a social media platform website
    for website, patterns in SOCIAL_MEDIA_WEBSITE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url_host):
                category = website
                url_type = "social_media"
    # check if the url is a video website
    if not category:
        for website, patterns in VIDEO_WEBSITE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url_host):
                    category = website
                    url_type = "video"
    # TODO: check if the url is from Mastodon, according to the request cookie
    return UrlMetadata(url, category, url_type)