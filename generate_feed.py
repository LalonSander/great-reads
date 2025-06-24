import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import os

NYT_URL = "https://www.nytimes.com/spotlight/the-great-read"
RSS_FILE = "great_read_rss.xml"

def fetch_articles():
    response = requests.get(NYT_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    articles = []
    for item in soup.select("section.css-1hnz86c article"):  # Update selector if NYT changes layout
        title_tag = item.find("h2")
        link_tag = item.find("a", href=True)
        summary_tag = item.find("p")

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.nytimes.com" + link_tag["href"]
            description = summary_tag.get_text(strip=True) if summary_tag else ""
            articles.append({
                "title": title,
                "link": link,
                "description": description,
                "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            })
    return articles

def build_rss(articles):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "NYT - The Great Read"
    ET.SubElement(channel, "link").text = NYT_URL
    ET.SubElement(channel, "description").text = "The Great Read - NYT Spotlight"
    
    for article in articles:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = article["title"]
        ET.SubElement(item, "link").text = article["link"]
        ET.SubElement(item, "description").text = article["description"]
        ET.SubElement(item, "pubDate").text = article["pubDate"]

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    articles = fetch_articles()
    build_rss(articles)
