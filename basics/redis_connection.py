import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)
if __name__ == "__main__":
    print(redis_client.ping())

    # Store a result
    result = redis_client.set("link:python", "https://youtube.com")
    print("SET result:", result)

    # Retrieve the URL
    url = redis_client.get("link:python")
    print("GET result:", url)

    # Retrieve a nonexistent key
    missing_url = redis_client.get("link:doesnotexist")
    print("Missing key:", missing_url)

    # first value
    redis_client.set("link:python", "https://youtube.com")

    # Overwrite with another URL
    result = redis_client.set("link:python", "https://google.com")

    print("SET result:", result)
    print("Current value:", redis_client.get("link:python"))

    # Overwrite with NX
    result = redis_client.set(
        "link:python",
        "https://amazon.com",
        nx=True,
    )

    print("SET with NX result:", result)
    print("current value:", redis_client.get("link:python"))
