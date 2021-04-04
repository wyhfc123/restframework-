import requests
proxies={
    "http":"122.246.192.140:3000"
    ""
}
res=requests.get("http://127.0.0.1:8000/test/uview/")
print(res.text)