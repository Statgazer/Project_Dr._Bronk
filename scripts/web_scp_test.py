from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from newspaper import Article
import requests
import time
import pandas as pd
from urllib.parse import urljoin

df = pd.DataFrame(columns=["URL"])
URL=["https://english.pravda.ru","https://tass.com"]

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

    content_for_url = []

    title_count = 0         
    for link in links:
        try:
            article = Article(link)
            article.download()
            article.parse()
            title_count+=1

            if title_count == 60:
                break

            
            if "Ukraine" in article.text or "UKRAINE" in article.text:
                content_for_url.append(f"{link}  {article.text}")    
            
    
        except:
            pass
 
    
    url_data_dict = {"URL": url}

    # Add content columns to the dictionary
    for i, content in enumerate(content_for_url):
        column_name = f"Content_{i+1}"
        url_data_dict[column_name] = content

    # Append the URL data dictionary to the DataFrame
    df = df.append(url_data_dict, ignore_index=True)


#path = 
df.to_csv("/Users/roshen_abraham/Desktop/PC/RA/DR. CHRIS BRONK/project/target files/output.csv", index=False)



