from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from newspaper import Article
import requests
import time
import pandas as pd
from urllib.parse import urljoin
import json

df = pd.DataFrame(columns=["URL"])
URL=["http://www.chinadaily.com.cn","https://english.news.cn/home.htm"]
File_Path = "/Users/roshen_abraham/Desktop/PC/RA/DR. CHRIS BRONK/project/target files/"

for url in URL:
    parser = 'html.parser'  
    resp = requests.get(url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)
    #time.sleep()
    
    links = []
    base_url = url  # Set the base URL to the current page's URL

    for link in soup.find_all('a', href=True):
        href = link['href']

        # Check if the href attribute is a relative URL
        if href.startswith('/'):
            absolute_url = urljoin(base_url, href)
        else:
            absolute_url = href  # Use the href as-is if it's an absolute URL

        links.append(absolute_url)
    
    links_distinct = pd.Series(links).drop_duplicates().tolist()
    
    content_for_url = []

    title_count = 0         
    for link in links_distinct:
        try:
            article = Article(link)
            article.download()
            time.sleep(2)
            article.parse()
            title_count+=1

            # if title_count == 10:
                # break
#####change#####-------------------------
            if "Israel" in article.text or "Gaza" in article.text:
                article_data = {
                "source": article.source_url,
                "url": link,
                "title": article.title,
                "published_date": article.publish_date.strftime('%Y-%m-%d') if article.publish_date else None,
                "content": article.text
                }
                content_for_url.append(article_data)

#####change#####-------------------------

            # if "Ukraine" in article.text or "UKRAINE" in article.text:
            #     content_for_url.append(f"{link}  {article.text}")    
            
    
        except:
            pass
    time.sleep(2)
 ####change#####-------------------------
    website_name = url.split("//")[-1].replace(".", "_")  # Convert website URL to a valid filename
    with open(f"{File_Path}{website_name}.json", 'w') as file:
        json.dump(content_for_url, file, indent=4)
 ####change#####-------------------------

#     url_data_dict = {"URL": url}

#     # Add content columns to the dictionary
#     for i, content in enumerate(content_for_url):
#         column_name = f"Content_{i+1}"
#         url_data_dict[column_name] = content

#     # Append the URL data dictionary to the DataFrame
#     df = df.append(url_data_dict, ignore_index=True)


# path = "/Users/roshen_abraham/Desktop/PC/RA/DR. CHRIS BRONK/project/target files/output.csv"
# df.to_csv(path, index=False)



