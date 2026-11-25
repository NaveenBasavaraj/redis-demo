import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

client.set("my_key", "Helo world using Python and Redis")
value = client.get("my_key")

print("Reply:", value)

client.close()
