import requests
import pandas as pd
from tqdm import tqdm
import os

# input your own API key here
API_KEY = input('Please input your YouTube API key: ')
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

def search_youtube(keyword, max_results=50):
    all_videos = []
    next_page_token = None
    total_requests = (max_results // 50) + (1 if max_results % 50 else 0)  # 计算总请求次数

    with tqdm(total=total_requests, desc=f'Searching for: {keyword}', unit='request') as pbar:
        while len(all_videos) < max_results:
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'video',
                'maxResults': min(50, max_results - len(all_videos)),  # 最多请求 50 或剩余的数量
                'key': API_KEY
            }
            if next_page_token:
                params['pageToken'] = next_page_token

            response = requests.get(SEARCH_URL, params=params)
            data = response.json()

            # 提取视频信息
            all_videos.extend(extract_video_links(data))

            next_page_token = data.get('nextPageToken')
            pbar.update(1)  # 更新进度条

            if not next_page_token:
                break  # 没有更多页面时停止

    return all_videos

def extract_video_links(data):
    video_data = []
    for item in data.get('items', []):
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_title = item['snippet']['title']  # 提取视频标题
        video_data.append({'Title': video_title, 'Link': video_url})
    return video_data

def main():
    keywords = [
        '无人机航拍, 地震',
        'drone aerial photography, earthquake'
    ]

    # 设置爬取数量
    max_results = int(input('Please input the total number of videos to crawl: '))

    # 创建结果文件夹
    os.makedirs('results', exist_ok=True)

    for keyword in keywords:
        print(f"Searching for: {keyword}")
        video_data = search_youtube(keyword, max_results)

        # 将结果存储到对应的 Excel 文件
        filename = f"results/{keyword.replace(',', '_').replace(' ', '_')}.xlsx"
        df = pd.DataFrame(video_data)  # 直接用视频数据创建 DataFrame
        df.to_excel(filename, index=False)  # 保存为 Excel 文件
        print(f"Results saved to: {filename}")

if __name__ == '__main__':
    main()
