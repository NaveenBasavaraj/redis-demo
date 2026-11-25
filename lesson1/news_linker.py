import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

NEWEST_KEY = "links:newest"
MAX_LINKS = 100


def post_link(title, url):
    link_id = client.incr("links:next_id")  # 1
    client.set("link:" + str(link_id) + ":title", title)  # 2
    client.set("link:" + str(link_id) + ":url", url)  # 3
    client.lpush(NEWEST_KEY, link_id)  # 4
    client.ltrim(NEWEST_KEY, 0, MAX_LINKS - 1)  # 5
    return link_id


def show_newest(count):
    link_ids = client.lrange(NEWEST_KEY, 0, count - 1)  # 1
    print("Newest", len(link_ids), "links:")
    for link_id in link_ids:  # 2
        title_key = "link:" + link_id + ":title"
        url_key = "link:" + link_id + ":url"
        replies = client.mget([title_key, url_key])  # 3
        print("  #" + link_id, replies[0], "->", replies[1])


post_link("Redis 8 is out", "https://redis.io/blog")
post_link("Why Python is slow", "https://example.com/python")
post_link("Learn Docker in a weekend", "https://example.com/docker")
post_link("SQL indexes explained", "https://example.com/sql")

show_newest(3)
print("Total links in the list:", client.llen(NEWEST_KEY))

client.close()
