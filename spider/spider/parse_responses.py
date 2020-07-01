import pickle
import datetime
from spider.common import config, init_db
from gemeinsprache.utils import cyan, red, blue, green, yellow, magenta
from dateutil.parser import parse as parse_timestamp
import pytz
from bs4 import BeautifulSoup

MAX_REQUESTS = 20
MAX_ARTICLES_PER_SOURCE = 100
NULL_DATE = datetime.datetime(1960, 1, 1)

db = init_db()

seen = set()


def ensure_tztime(ts):
    if isinstance(ts, str):
        ts = parse_timestamp(ts)
    try:
        return pytz.utc.localize(ts)
    except:
        return ts


def parse_sitemap(row):
    if not row or not row["content"]:
        return []
    sitemap_url = row["url"]

    soup = BeautifulSoup(row["content"], "xml")
    elements = soup.findAll("url")
    rows = []
    print(row.keys())
    for elem in elements:
        url_node = elem.find("loc")
        lastmod_node = elem.find("lastmod")
        xmlmeta = "\n".join([str(e) for e in elem.children]).encode("utf-8")

        try:
            lastmod = parse_timestamp(lastmod_node.text.strip())
        except:
            lastmod = NULL_DATE

        try:
            url = url_node.text.strip()
        except:
            continue

        if url:
            url = url.strip()
            if url in seen:
                continue

            row = {
                "url": url.strip(),
                "site": row["site"],
                "name": row["name"],
                "city": row["city"],
                "state": row["state"],
                "loc": row["loc"],
                "lastmod": lastmod,
                "xmlmeta": xmlmeta,
                "is_dumpsterfire": row['is_dumpsterfire']
            }
            rows.append(row)
            seen.add(url.strip())

    rows = list(sorted(rows, key=lambda row: ensure_tztime(["lastmod"]), reverse=True))[
        : min(len(rows), MAX_ARTICLES_PER_SOURCE)
    ]
    print(
        magenta("[ fetch_sitemap ] "),
        f":: Extracted {len(rows)} urls from sitemap: {sitemap_url}",
    )
    return rows


if __name__ == "__main__":
    crawldb = db["articles"]
    responsedb = db["sitemaps"]
    spiderqueue = db["spiderqueue"]
    seen.update([row["url"] for row in spiderqueue])


    queue = [row for row in responsedb]

    parsed = []
    for row in queue:
        parsed.extend(parse_sitemap(row))
    filtered = [row for row in parsed if row and row["url"] not in seen]
    crawldb.upsert_many(filtered, ["url"])
