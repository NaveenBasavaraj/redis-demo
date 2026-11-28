import secrets
import string
import time

from redis_connection import redis_client

alpha_numeric_char = string.ascii_letters + string.digits


def generate_short_code():
    return "".join(secrets.choice(alpha_numeric_char) for _ in range(6))


def create_short_url(original_url, ttl=None):
    while True:
        short_code = generate_short_code()
        key = f"link:{short_code}"

        result = redis_client.set(key, original_url, nx=True, ex=ttl)

        if result:
            return short_code


def get_original_url(short_code):
    return redis_client.get(f"link:{short_code}")


def get_ttl(short_code):
    return redis_client.ttl(f"link:{short_code}")


if __name__ == "__main__":
    # ----------------------------------------
    # 1. Create a link that expires in 10 sec
    # ----------------------------------------

    original_url = "https://www.amazon.in/products/some-long-product-url"

    short_code = create_short_url(original_url, ttl=10)
    key = f"link:{short_code}"

    print("\n--- Temporary Link ---")
    print("Short code:", short_code)
    print("Redis key:", key)
    print("Stored URL:", get_original_url(short_code))
    print("Initial TTL:", get_ttl(short_code))

    # ----------------------------------------
    # 2. Observe TTL countdown
    # ----------------------------------------

    print("\n--- TTL Countdown ---")

    for _ in range(5):
        remaining_ttl = get_ttl(short_code)
        stored_url = get_original_url(short_code)

        print(f"TTL: {remaining_ttl}s | URL exists: {stored_url is not None}")

        time.sleep(2)

    # ----------------------------------------
    # 3. Wait for expiration
    # ----------------------------------------

    print("\n--- Waiting for Expiration ---")

    time.sleep(2)

    print("TTL after expiration:", get_ttl(short_code))
    print("URL after expiration:", get_original_url(short_code))

    # ----------------------------------------
    # 4. Create a link that expires in 1 hour
    # ----------------------------------------

    url2 = "https://www.flipkart.in/products/some-long-product-url"

    short_code2 = create_short_url(url2, ttl=3600)
    key2 = f"link:{short_code2}"

    print("\n--- One-Hour Link ---")
    print("Short code:", short_code2)
    print("Redis key:", key2)
    print("Stored URL:", get_original_url(short_code2))
    print("TTL:", get_ttl(short_code2))

    # ----------------------------------------
    # 5. Create a permanent link
    # ----------------------------------------

    url3 = "https://www.google.in/something-long"

    short_code3 = create_short_url(url3, ttl=None)
    key3 = f"link:{short_code3}"

    print("\n--- Permanent Link ---")
    print("Short code:", short_code3)
    print("Redis key:", key3)
    print("Stored URL:", get_original_url(short_code3))
    print("TTL:", get_ttl(short_code3))
