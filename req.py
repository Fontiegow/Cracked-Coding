import requests as req

# 1. GET Request Test
response_get = req.get('https://jsonplaceholder.typicode.com/posts/1')
print(f"GET Status: {response_get.status_code}")
print(f"GET Data: {response_get.json()['title']}\n")

# 2. POST Request Test
new_post = {
    "title": "Learning Backend",
    "body": "Day 1 was successful!",
    "userId": 1
}
response_post = req.post('https://jsonplaceholder.typicode.com/posts', json=new_post)
print(f"POST Status: {response_post.status_code}")
print(f"POST Response: {response_post.json()}")

