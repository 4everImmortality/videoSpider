import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64


def save_image(url, folder, count):
    try:
        if url.startswith("data:"):  # 处理 Base64 数据
            header, encoded = url.split(",", 1)
            image_data = base64.b64decode(encoded)
            filename = os.path.join(folder, f'image_{count}.png')
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f'Saved: {filename}')
        else:
            # 检查是否为相对路径，补全为绝对路径
            if not url.startswith("http"):
                url = "https://www.bing.com" + url

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, stream=True)  # 使用 stream
            if response.status_code == 200:
                # 根据 URL 后缀决定文件格式
                file_extension = url.split('.')[-1].split('?')[0].lower()

                # 过滤掉 SVG 图片
                if file_extension in ['svg']:
                    print(f'Skipped SVG image: {url}')
                    return

                if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                    file_extension = 'jpg'  # 默认保存为 jpg

                filename = os.path.join(folder, f'image_{count}.{file_extension}')
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f'Saved: {filename}')
                return True  # 返回是否成功保存
            else:
                print(f'Failed to retrieve image: {url}')
                return False  # 返回失败
    except Exception as e:
        print(f'Error saving {url}: {e}')
        return False  # 返回失败


def bing_image_search(query, folder, num_images):
    img_count = 0
    page = 0
    while img_count < num_images:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first={page * 35}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for img in soup.find_all("img"):
            if img_count >= num_images:
                break
            img_url = img.get("src")
            if img_url:
                if save_image(img_url, folder, img_count):
                    img_count += 1  # 只有成功保存时才增加计数
                print(f'img_url: {img_url}')

        page += 1
        if img_count < num_images and not soup.find_all("img"):
            break


def google_image_search(query, folder, num_images):
    img_count = 0
    page = 0
    while img_count < num_images:
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={urllib.parse.quote(query)}&start={page * 100}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for img in soup.find_all("img"):
            if img_count >= num_images:
                break
            img_url = img.get("src")
            if img_url:
                if save_image(img_url, folder, img_count):
                    img_count += 1  # 只有成功保存时才增加计数

        page += 1
        if img_count < num_images and not soup.find_all("img"):
            break


def main():
    folder = 'results'
    os.makedirs(folder, exist_ok=True)

    query = '无人机 地震救援'
    num_images = 100  # 自定义图片张数

    print("Searching Bing...")
    bing_image_search(query, folder, num_images)

    # print("Searching Google...")
    # google_image_search(query, folder, num_images)


if __name__ == "__main__":
    main()
