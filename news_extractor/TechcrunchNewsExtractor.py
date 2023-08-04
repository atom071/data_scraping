import requests
from fake_useragent import UserAgent
ua = UserAgent()

def extract_news():
    try:
        page_number = 1
        while True:
            headers = {
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'X-TC-EC-Auth-Token': '',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': str(ua.random),
                'Content-Type': 'application/json; charset=utf-8',
                'Referer': 'https://techcrunch.com/',
                'X-TC-UUID': '',
                'sec-ch-ua-platform': '"Linux"',
            }

            params = {
                'page': str(page_number),
                '_embed': 'true',
                # 'cachePrevention': '0',
            }

            response = requests.get('https://techcrunch.com/wp-json/tc/v1/magazine', params=params, headers=headers)
            newsData = response.json()
            if len(newsData)<1:
                break
            else:
                for news in newsData:
                    try:
                        yoast_head_json = news.get("yoast_head_json", {})
                        title = yoast_head_json.get("title",'')
                        description = yoast_head_json.get("description", '')
                        author = yoast_head_json.get("author", '')
                        published_time = yoast_head_json.get("article_published_time", '')
                        image_url = yoast_head_json.get("og_image", [])[0].get("url","")
                        article_url = yoast_head_json.get("canonical","")
                        news = {"title":title,"description":description,"author":author,"published_time":published_time,"image_url":image_url,"article_url":article_url}
                        print(news)
                        yield news
                    except:
                        pass
            page_number+=1
    except Exception as exp:
        print("Exception in extract_news",exp)



if __name__ == '__main__':
    list(extract_news())