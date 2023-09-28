import requests

# curl -X POST "http://127.0.0.1:8000/bar" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"foo\":1,\"age\":2,\"name\":\"333\"}"
res = requests.post("http://127.0.0.1:8000/bar", json={"foo": 1, "age": 12, "name": "xiao123"})
print(res.json())  # {'foo': 1, 'age': 12, 'name': 'xiao123'}

# 搜索文档
search_documents_url = "http://localhost:8000/search_documents"
response = requests.post(search_documents_url, json={"query": "暖和的大衣","num": 5})
print(response.json())

# 添加文档
add_document_url = "http://localhost:8000/add_document"
response = requests.post(add_document_url, json={"document": "灰度数据。"})
print(response.json())

# 搜索文档
search_documents_url = "http://localhost:8000/search_documents"
response = requests.post(search_documents_url, json={"query": "灰度数据","num": 5})
print(response.json())

