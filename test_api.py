
import httpx

response = httpx.get(
    "https://jsonplaceholder.typicode.com/todos/1",
    timeout=5.0
)

response.raise_for_status()

data = response.json()

print(data)
