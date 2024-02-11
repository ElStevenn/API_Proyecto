from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
# Assuming FilesAWSS3 is updated and ready for sync operations
from .get_travel_image import FilesAWSS3  # Adjust import as necessary

BASE_URL = "https://airlinelogos.net"
S3_Handler = FilesAWSS3()
columns = ['airline_name', 'airline_webpage', 'airline_img_url']
airline_logo_dataset = pd.DataFrame(columns=columns)

def fetch_with_retry(url, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} for {url} failed: {str(e)}, retrying after {delay} seconds...")
            time.sleep(delay)
            delay *= 2
    raise Exception(f"Failed to fetch {url} after {max_retries} attempts.")

def extract_logo_details(url, S3_Handler):
    logos_details = []
    try:
        page_content = fetch_with_retry(url, max_retries=3, delay=1)
        soup = BeautifulSoup(page_content, 'lxml')
        thumbnails = soup.find_all("td", class_="thumbnails")
        for thumb in thumbnails:
            img_tag = thumb.find("img", class_="image thumbnail")
            if img_tag and 'src' in img_tag.attrs:
                logo_url = f"{BASE_URL}/{img_tag['src'].lstrip('/')}"
                name_tag = thumb.find("span", class_="thumb_title")
                name = name_tag.text.strip() if name_tag else "Unknown"
                page_url_tag = thumb.find("a")
                page_url = f"{BASE_URL}/{page_url_tag['href'].lstrip('/')}" if page_url_tag and 'href' in page_url_tag.attrs else "No URL"

                logos_details.append({'airline_name': name, 'airline_webpage': page_url, 'airline_img_url': logo_url})
    except Exception as e:
        print(f"Failed to process {url}: {e}")
    return logos_details

def main():
    categories = ['3', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    pages = [64, 17, 21, 26, 21, 22, 22, 24, 23, 20, 14]
    global airline_logo_dataset

    pbar = tqdm(total=sum(pages), desc="Downloading logos")
    for category_n, num_pages in zip(categories, pages):
        for pg_num in range(1, num_pages + 1):
            url = f"{BASE_URL}/thumbnails-{category_n}.html?page={pg_num}"
            logos_details = extract_logo_details(url, S3_Handler)
            airline_logo_dataset = pd.concat([airline_logo_dataset, pd.DataFrame(logos_details)], ignore_index=True)
        pbar.update(num_pages)
    pbar.close()

    airline_logo_dataset.to_csv('logos_dataset.csv', index=False)

if __name__ == "__main__":
    main()
