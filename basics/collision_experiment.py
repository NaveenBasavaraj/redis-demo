import redis
from redis_connection import redis_client


# ----------------------------
# Controlled code generator
# ----------------------------

codes = iter(["ABC123", "XYZ789"])


def generate_short_code():
    return next(codes)


def create_short_url(original_url):
    while True:
        short_code = generate_short_code()
        key = f"link:{short_code}"

        result = redis_client.set(key, original_url, nx=True)

        print(f"Attempted code: {short_code}")
        print(f"Redis result: {result}")

        if result:
            return short_code


def get_original_url(short_code):
    return redis_client.get(f"link:{short_code}")


if __name__ == "__main__":
    # Seed an existing mapping to deliberately cause a collision
    redis_client.set("link:ABC123", "https://amazon.in/product-A")

    print("Existing mapping:")
    print(redis_client.get("link:ABC123"))
    print("-" * 40)

    # Try to create a new short URL
    new_url = "https://flipkart.com/product-B"

    new_short_code = create_short_url(new_url)

    print("-" * 40)
    print("New short code:", new_short_code)
    print("ABC123:", redis_client.get("link:ABC123"))
    print("XYZ789:", redis_client.get("link:XYZ789"))
