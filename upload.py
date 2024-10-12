import base64
import requests

# 將圖片轉換為 Base64 字串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

# 上傳 Base64 字串
def upload_image(base64_string, upload_url):
    response = requests.post(upload_url, json={"image": base64_string})
    return response.json()

# 使用範例
image_path = "path/to/your/image.jpg"
upload_url = "http://example.com/upload"
base64_string = encode_image(image_path)
response = upload_image(base64_string, upload_url)
print(response)