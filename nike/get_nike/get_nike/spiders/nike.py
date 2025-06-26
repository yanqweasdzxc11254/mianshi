import scrapy
import json
from urllib.parse import urljoin, quote
from urllib.parse import urlencode


class NikeSpider(scrapy.Spider):
    name = "nike"
    allowed_domains = ["nike.com.cn"]
    start_urls = ["https://www.nike.com.cn/w/"]

    def parse(self, response):
        res = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(res)
        data = data["props"]["pageProps"]["initialState"]["Wall"]["products"]
        for i in range(0, len(data)):
            # title = data[i]["title"] + "/" + data[i]["subtitle"]
            # price = data[i]["price"]["currency"] + ' ' + str(data[i]["price"]["currentPrice"])
            # color = data[i]["colorDescription"]
            # sku = data[i]["cloudProductId"] + "/" + data[i]["pid"] + "/" + data[i]["id"]
            details_url = urljoin("https://www.nike.com.cn", quote(data[i]["url"].split("}")[1]))
            print(details_url)
            # yield {
            #         'details_url': details_url,
            #     }

            yield scrapy.Request(
            url=details_url,
            method='GET',
            callback=self.parse_details,
        )
        # api_url = "https://api.nike.com.cn/cic/browse/v2?queryid=products&anonymousId=DSWXEFC2F509B6406E2F63845AD541EB38E7&country=cn&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(CN)%26filter%3Dlanguage(zh-Hans)%26filter%3DemployeePrice(true)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=zh-Hans&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D"
        api_url = "https://api.nike.com.cn/cic/browse/v2?"

        # 设置请求头信息
        headers = {
            "sec-ch-ua-platform": "\"Windows\"",
            "Referer": "https://www.nike.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0"
        }

        # 设置请求参数
        params = {
            "queryid": "products",
            "anonymousId": "DSWXEFC2F509B6406E2F63845AD541EB38E7",
            "country": "cn",
            "endpoint": "/product_feed/rollup_threads/v2?filter=marketplace(CN)&filter=language(zh-Hans)&filter=employeePrice(true)&anchor=24&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24",
            "language": "zh-Hans",
            "localizedRangeStr": "{lowestPrice} — {highestPrice}"
        }
        query_string = urlencode(params)
        api_url = "https://api.nike.com.cn/cic/browse/v2?" + query_string

        # 发起API请求
        yield scrapy.Request(
            url=api_url,
            headers={**headers, 'Content-Type': 'application/json'},
            method='GET',
            callback=self.parse_api,
        )

    def parse_api(self, response):
        # 处理API响应
        if response.status == 200:
            data = response.json()
            data = data["data"]["products"]["products"]
            for i in range(0, len(data)):
                details_url = urljoin("https://www.nike.com.cn", quote(data[i]["url"].split("}")[1]))
                print(details_url)
                # yield {
                #     'details_url': details_url,
                # }
                yield scrapy.Request(
                    url=details_url,
                    method='GET',
                    callback=self.parse_details,
                )
    def parse_details(self, response):
        res = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(res)
        # （标题（title） 价格(price) 颜色(color) 尺码(size) 网站货号(sku) 详情(details) 大图的URL (img_urls)
        details_url = data["props"]["pageProps"]["selectedProduct"]["productInfo"]["url"]
        title = data["props"]["pageProps"]["selectedProduct"]["productInfo"]["fullTitle"]
        details = data["props"]["pageProps"]["selectedProduct"]["productInfo"]["productDescription"]
        price = data["props"]["pageProps"]["selectedProduct"]["prices"]["currency"] +' '+ str(data["props"]["pageProps"]["selectedProduct"]["prices"]["currentPrice"])
        color = data["props"]["pageProps"]["selectedProduct"]["colorDescription"]
        sku = data["props"]["pageProps"]["selectedProduct"]["globalProductId"] + "/" + data["props"]["pageProps"]["selectedProduct"]["id"]
        sizes_list = data["props"]["pageProps"]["selectedProduct"]["sizes"]
        sizes = []
        # ["props"]["pageProps"]["selectedProduct"]["sizes"][1]["localizedLabel"]
        for i in sizes_list:
            size = i["localizedLabel"]
            sizes.append(size)
        img_urls_list = data["props"]["pageProps"]["selectedProduct"]["contentImages"]
        img_urls = []
        # ["props"]["pageProps"]["selectedProduct"]["contentImages"][0]["properties"]["squarish"]["url"]
        for i in range(0, len(img_urls_list)):
            img_url = img_urls_list[i].get("properties", {}).get("squarish", {}).get("url", "")
            if not img_url:
                img_url = img_urls_list[i].get("properties", {}).get("portrait", {}).get("url", "")
            img_urls.append(img_url)
        yield {
            'details_url': details_url,
            'title': title,
            'details': details,
            'price': price,
            'color': color,
            'sku': sku,
            'sizes': sizes,
            'img_urls': img_urls,
        }
            
           