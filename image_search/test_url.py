import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def save_image(url, folder, count):
    try:
        if not url.startswith("http"):
            print(f'Skipped invalid image URL: {url}')
            return False

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, stream=True)

        if response.status_code == 200:
            file_extension = url.split('.')[-1].split('?')[0].lower()
            if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                file_extension = 'jpg'  # 默认保存为 jpg

            filename = os.path.join(folder, f'image_{count}.{file_extension}')
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'Saved: {filename}')
            return True
        else:
            print(f'Failed to retrieve image: {url}')
            return False
    except Exception as e:
        print(f'Error saving {url}: {e}')
        return False

def get_original_image_url(thumbnail_url):
    '''
    todo: 通过点击缩略图获取原始图片的URL 现在的方法是直接下载缩略图
    :param thumbnail_url:
    :return:
    '''
    headers = {"User-Agent": "Mozilla/5.0"}
    # 访问缩略图页面
    response = requests.get(thumbnail_url, headers=headers)
    print(f'content-type: {response.headers.get("content-type")}')
    if response.status_code == 200:
        # 按照jpeg格式直接下载
        if response.headers.get("content-type") == 'image/jpeg':
            return thumbnail_url

    print('Failed to find original image URL.')
    return None

def bing_image_search(query, folder, num_images):
    img_count = 0
    page = 0
    while img_count < num_images:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first={page * 35}"
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        thumbnails = soup.find_all('img', class_='mimg')
        for thumbnail in thumbnails:
            if img_count >= num_images:
                break

            if 'src' in thumbnail.attrs:
                thumbnail_url = thumbnail['src']
                print(f'Found thumbnail URL: {thumbnail_url}')

                # 获取原始图像 URL
                original_image_url = get_original_image_url(thumbnail_url)

                if original_image_url and save_image(original_image_url, folder, img_count):
                    img_count += 1
            else:
                print('Thumbnail does not have a src attribute.')

        page += 1
        time.sleep(1)

def main():
    folder = 'results'
    os.makedirs(folder, exist_ok=True)

    query = '无人机 地震'
    num_images = 10

    print("Searching Bing...")
    bing_image_search(query, folder, num_images)

if __name__ == "__main__":
    main()
