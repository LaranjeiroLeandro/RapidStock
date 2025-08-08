import requests
from lxml import html
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
import os


xpaths = {
    "Company Name": "/html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div[1]/div[1]",
    "Market Cap": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]",
    "Enterprise Value": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[2]",
    "Current Share Class": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[2]",
    "Shares Outstanding": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[2]/td[2]",
    "Shares Change (YoY)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[3]/td[2]",
    "Shares Change (QoQ)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[4]/td[2]",
    "Owned by Insiders (%)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[5]/td[2]",
    "Owned by Institutions (%)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[6]/td[2]",
    "Float": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[4]/table/tbody/tr[7]/td[2]",
    "PE Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[1]/td[2]",
    "Forward PE": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[2]/td[2]",
    "PS Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[3]/td[2]",
    "PB Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[4]/td[2]",
    "P/TBV Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[5]/td[2]",
    "P/FCF Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[6]/td[2]",
    "P/OCF Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[7]/td[2]",
    "PEG Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[5]/table/tbody/tr[8]/td[2]",
    "EV / Earnings": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[6]/table/tbody/tr[1]/td[2]",
    "EV / Sales": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[6]/table/tbody/tr[2]/td[2]",
    "EV / EBITDA": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[6]/table/tbody/tr[3]/td[2]",
    "EV / EBIT": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[6]/table/tbody/tr[4]/td[2]",
    "EV / FCF": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[6]/table/tbody/tr[5]/td[2]",
    "Current Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[1]/td[2]",
    "Quick Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[2]/td[2]",
    "Debt / Equity": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[3]/td[2]",
    "Debt / EBITDA": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[4]/td[2]",
    "Debt / FCF": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[5]/td[2]",
    "Interest Coverage": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[7]/table/tbody/tr[6]/td[2]",
    "Return on Equity (ROE)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[1]/td[2]",
    "Return on Assets (ROA)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[2]/td[2]",
    "Return on Invested Capital (ROIC)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[3]/td[2]",
    "Return on Capital Employed (ROCE)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[4]/td[2]",
    "Revenue Per Employee": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[5]/td[2]",
    "Profits Per Employee": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[6]/td[2]",
    "Employee Count": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[7]/td[2]",
    "Asset Turnover": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[8]/td[2]",
    "Inventory Turnover": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[8]/table/tbody/tr[9]/td[2]",
    "Income Tax": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[9]/table/tbody/tr[1]/td[2]",
    "Effective Tax Rate": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[1]/div[9]/table/tbody/tr[2]/td[2]",
    "Beta (5Y)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]",
    "52-Week Price Change": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]",
    "50-Day Moving Average": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]",
    "200-Day Moving Average": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[2]",
    "Relative Strength Index (RSI)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[2]",
    "Average Volume (20 Days)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr[6]/td[2]",
    "Short Interest": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[2]",
    "Short Previous Month": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[2]",
    "Short % of Shares Out": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[2]",
    "Short % of Float": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[2]",
    "Short Ratio (days to cover)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[2]",
    "Revenue": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[2]",
    "Gross Profit": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[2]/td[2]",
    "Operating Income": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[3]/td[2]",
    "Pretax Income": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[4]/td[2]",
    "Net Income": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[5]/td[2]",
    "EBITDA": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[6]/td[2]",
    "EBIT": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[7]/td[2]",
    "Earnings Per Share (EPS)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[3]/table/tbody/tr[8]/td[2]",
    "Cash & Cash Equivalents": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[1]/td[2]",
    "Total Debt": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[2]/td[2]",
    "Net Cash": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[3]/td[2]",
    "Net Cash Per Share": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[4]/td[2]",
    "Equity (Book Value)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[5]/td[2]",
    "Book Value Per Share": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[6]/td[2]",
    "Working Capital": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[4]/table/tbody/tr[7]/td[2]",
    "Operating Cash Flow": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[5]/table/tbody/tr[1]/td[2]",
    "Capital Expenditures": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[5]/table/tbody/tr[2]/td[2]",
    "Free Cash Flow": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[5]/table/tbody/tr[3]/td[2]",
    "FCF Per Share": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[5]/table/tbody/tr[4]/td[2]",
    "Gross Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[1]/td[2]",
    "Operating Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[2]/td[2]",
    "Pretax Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[3]/td[2]",
    "Profit Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[4]/td[2]",
    "EBITDA Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[5]/td[2]",
    "EBIT Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[6]/td[2]",
    "FCF Margin": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[6]/table/tbody/tr[7]/td[2]",
    "Dividend Per Share": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]",
    "Dividend Yield": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[2]/td[2]",
    "Dividend Growth (YoY)": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[3]/td[2]",
    "Years of Dividend Growth": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[4]/td[2]",
    "Payout Ratio": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[5]/td[2]",
    "Buyback Yield": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[6]/td[2]",
    "Shareholder Yield": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[7]/td[2]",
    "Earnings Yield": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[8]/td[2]",
    "FCF Yield": "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[9]/td[2]",
}

BATCH_SIZE = 200
PAUSE_MINUTES = 5
MAX_WORKERS = 200

def extract_currency_from_text(text):
    if not text:
        return 'USD'
    match = re.search(r'CURRENCY IS ([A-Z]{3})', text.upper())
    return match.group(1) if match else 'USD'

def load_links():
    with open("links.txt", "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def create_session():
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=200, pool_maxsize=200)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    return session

def extract_company_info(link, session, max_retries=5, wait_on_429=60):
    tries = 0
    while tries < max_retries:
        try:
            response = session.get(f"https://stockanalysis.com/{link}/company/")
            if response.status_code == 429:
                print(f"429 on company {link}, retrying in {wait_on_429}s ({tries+1}/{max_retries})")
                time.sleep(wait_on_429)
                tries += 1
                continue
            response.raise_for_status()
            tree = html.fromstring(response.content)
            info = {}
            rows = tree.xpath("/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/table/tbody/tr")
            for row in rows:
                try:
                    label = row.xpath("./td[1]")[0].text_content().strip()
                    if label in ["Country", "Sector", "Industry"]:
                        info[label] = row.xpath("./td[2]")[0].text_content().strip()
                except:
                    continue
            return {k: info.get(k) for k in ["Country", "Sector", "Industry"]}
        except Exception as e:
            print(f"Error (company) {link}: {e}")
            tries += 1
            if tries < max_retries:
                time.sleep(2)
    print(f"Failed company info for {link} after {max_retries} tries.")
    return {"Country": None, "Sector": None, "Industry": None}

def extract_data(link, session, max_retries=10, wait_on_429=60):
    tries = 0
    while tries < max_retries:
        try:
            response = session.get(f"https://stockanalysis.com/{link}/statistics/")
            if response.status_code == 429:
                time.sleep(wait_on_429)
                tries += 1
                continue
            response.raise_for_status()
            tree = html.fromstring(response.content)
            data = {'Link': link.upper()}
            for key, xpath in xpaths.items():
                try:
                    elements = tree.xpath(xpath)
                    data[key] = elements[0].text_content().strip() if elements else None
                except:
                    data[key] = None
            try:
                price_element = tree.xpath("/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div[1]")
                price_text = price_element[0].text_content().strip() if price_element else None
                currency_element = tree.xpath("/html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div[1]/div[2]")
                currency_text = currency_element[0].text_content().strip() if currency_element else ""
                currency = extract_currency_from_text(currency_text)
                data['Price'] = price_text
                data['Currency'] = currency
            except:
                data['Price'] = None
                data['Currency'] = None
            company_info = extract_company_info(link, session, max_retries, wait_on_429)
            final_data = {
                'Link': data['Link'],
                'Company Name': data['Company Name'],
                'Price': data['Price'],
                'Currency': data['Currency'],
                'Country': company_info['Country'],
                'Sector': company_info['Sector'],
                'Industry': company_info['Industry']
            }
            for key, value in data.items():
                if key not in final_data:
                    final_data[key] = value
            return final_data
        except Exception as e:
            print(f"Error {link}: {e}")
            tries += 1
            if tries < max_retries:
                time.sleep(2)
    return None

def process_batch(links_batch, batch_num, session):
    print(f"Processing batch {batch_num} ({len(links_batch)} links)")
    batch_start = time.time()
    batch_data = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(extract_data, link, session): link for link in links_batch}
        for future in as_completed(futures):
            result = future.result()
            if result:
                batch_data.append(result)
                print(f"{result['Link']} processed ({len(batch_data)}/{len(links_batch)})")
    elapsed = time.time() - batch_start
    print(f"Batch {batch_num} done: {len(batch_data)}/{len(links_batch)} in {elapsed:.2f}s")
    return batch_data

def save_data(all_data, filename="data.parquet"):
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_parquet(filename, compression='snappy', index=False)
        print(f"Saved {len(df)} records to {filename}")
    else:
        print("No data to save")

def load_existing_data(filename="data.parquet"):
    if os.path.exists(filename):
        try:
            df = pd.read_parquet(filename)
            print(f"Loaded existing data: {len(df)} records")
            return df.to_dict('records')
        except:
            print("Failed loading existing data")
    return []

def get_processed_links(existing_data):
    return {item['Link'].lower() for item in existing_data if 'Link' in item}

def main():
    start = time.time()
    all_links = load_links()
    existing_data = load_existing_data()
    processed = get_processed_links(existing_data)
    remaining = [link for link in all_links if link not in processed]
    print(f"Total links: {len(all_links)}")
    print(f"Processed: {len(processed)}")
    print(f"Remaining: {len(remaining)}")
    if not remaining:
        print("All links processed.")
        return
    all_data = existing_data.copy()
    session = create_session()
    total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(remaining), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch_links = remaining[i:i + BATCH_SIZE]
        batch_data = process_batch(batch_links, batch_num, session)
        all_data.extend(batch_data)
        save_data(all_data)
        if batch_num < total_batches:
            print(f"Pause {PAUSE_MINUTES} min before next batch...")
            time.sleep(PAUSE_MINUTES * 60)
    total_time = time.time() - start
    print(f"\nSummary:")
    print(f"Total processed: {len(all_data)}")
    print(f"New added: {len(all_data) - len(existing_data)}")
    print(f"Elapsed time: {total_time:.2f}s ({total_time/60:.1f}min)")
    print(f"Batches processed: {total_batches}")

if __name__ == "__main__":
    main()