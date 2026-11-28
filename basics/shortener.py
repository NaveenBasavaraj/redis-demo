import secrets
import string
from redis_connection import redis_client

alpha_numeric_char = string.ascii_letters + string.digits


def generate_short_code():
    return "".join(secrets.choice(alpha_numeric_char) for _ in range(6))


def create_short_url(original_url):
    while True:
        short_code = generate_short_code()
        key = f"link:{short_code}"
        result = redis_client.set(key, original_url, nx=True)
        if result:
            return short_code


def get_original_url(short_code):
    return redis_client.get(f"link:{short_code}")


if __name__ == "__main__":
    # for _ in range(10):
    #     print(generate_short_code())

    original_url = "https://www.amazon.in/products/some-long-product-url"

    short_code = create_short_url(original_url)
    stored_url = get_original_url(short_code)

    print("Short code:", short_code)
    print("Redis key:", f"link:{short_code}")
    print("Stored URL:", stored_url)  # redis_client.get(f"link:{short_code}"))
