# RapidStock - Advanced Stock Screener

A comprehensive web-based stock screening application that allows you to filter and analyze stocks from global markets using multiple financial criteria. The application scrapes data from [stockanalysis.com](https://stockanalysis.com) and provides a user-friendly interface to search through thousands of stocks.

![RapidStock Interface](RapidStock.png)

## Features

- **Multi-criteria filtering**: Filter stocks by financial ratios, market data, and company information
- **Global coverage**: Includes stocks from major exchanges (NYSE, NASDAQ, LSE, Euronext, TSX, and more)
- **Responsive design**: Works seamlessly on desktop and mobile devices
- **Advanced search**: Support for text, numeric, percentage, and categorical filters

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Required Libraries

Install all required dependencies using pip:

```bash
pip install flask pandas numpy requests lxml pathlib concurrent.futures urllib3
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/LaranjeiroLeandro/RapidStock.git
cd RapidStock
```

### 2. Run the Data Scraper (Optional - First Time Setup)

If you want fresh data don't use the `data.parquet` file:

```bash
python scrapper.py
```

This will scrape stock data from stockanalysis.com. **Note**: This process can take several hours depending on the number of stocks.

### 3. Process and Convert Data

After scraping, convert currencies and add economic group information:

```bash
python dataconvert.py
```

### 4. Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

### 5. Open Your Browser

Navigate to `http://localhost:5000` to access the RapidStock interface.

## Usage Guide

### Basic Filtering

The application uses a three-part filtering system:

**Criteria → Operator → Value**

#### Example Usage

Let's filter for profitable companies with good returns:

1. **First Filter**: `Return on Equity (ROE)` `>` `20`
   - This finds companies with ROE greater than 20%

2. **Second Filter**: `Market Cap` `>=` `1000000000`
   - This finds companies with market cap of at least 1 billion EUR

3. **Third Filter**: `Country` `=` `United States`
   - This filters for US companies only

4. **Fourth Filter**: `Sector` `=` `Technology`
   - This narrows down to technology companies

### Special Value Formats

#### Percentage Values (%)
- Enter percentage values as numbers: `15` for 15%
- The system automatically handles the conversion
- Examples: ROE > `20`, Profit Margin >= `10`

#### Currency Values with Suffixes
- **T** = Trillion (1,000,000,000,000)
- **B** = Billion (1,000,000,000) 
- **M** = Million (1,000,000)
- **K** = Thousand (1,000)

Examples:
- Market Cap > `5000000000` (5 billion EUR)
- Revenue >= `100000000` (100 million EUR)
- Free Cash Flow > `5000` (50 thousand EUR)

#### Text and Selection Filters
- **Contains**: Use for partial text matching
- **Equals (==)**: Exact match
- **Not equals (!=)**: Exclude specific values

#### Available Operators
- `=` (equals)
- `≠` (not equals) 
- `≥` (greater than or equal)
- `≤` (less than or equal)
- `>` (greater than)
- `<` (less than)
- `contains` (text search)

### Filter Categories

#### Company Information
- Company Name, Country, Continent, Economic Groups
- Sector, Industry

#### Market Data
- Price, Market Cap, Enterprise Value
- PE Ratio, PS Ratio, PB Ratio, PEG Ratio

#### Financial Performance
- Revenue, Net Income, EBITDA, EPS
- ROE, ROA, ROIC, ROCE
- Profit Margin, Operating Margin, EBITDA Margin

#### Balance Sheet
- Total Debt, Cash & Cash Equivalents, Book Value
- Current Ratio, Quick Ratio, Debt/Equity

#### Stock Performance
- 52-Week Price Change, Beta
- Moving Averages (50-day, 200-day)
- Volume, Short Interest

#### Dividends
- Dividend Yield, Dividend Growth
- Payout Ratio, Years of Dividend Growth

## Data Scraper Configuration

### Modifying the Scraper (`scrapper.py`)

Key configuration variables you can modify:

```python
# Batch processing
BATCH_SIZE = 200          # Number of stocks processed per batch
PAUSE_MINUTES = 5         # Pause between batches (minutes)
MAX_WORKERS = 200         # Concurrent threads for scraping

# Error handling
max_retries = 10          # Retry attempts for failed requests
wait_on_429 = 60         # Wait time for rate limiting (seconds)
```

### Important Scraper Settings

1. **Batch Size**: Reduce if you encounter memory issues
2. **Pause Minutes**: Increase to be more respectful to the source website
3. **Max Workers**: Adjust based on your internet connection and system capabilities
4. **Rate Limiting**: The scraper handles 429 (Too Many Requests) responses automatically

### Adding New Stock Tickers

Edit the `links.txt` file to add new stocks:

```
stocks/AAPL
stocks/MSFT  
stocks/GOOGL
quote/epa/MC  # European stocks
quote/tyo/7203 # Tokyo stocks
```

Follow the format from stockanalysis.com URLs.

## Data Processing Configuration

### Currency Conversion (`dataconvert.py`)

Key configuration options:

```python
# Currency columns to convert
currency_cols = ['Price', 'Market Cap', 'Enterprise Value', ...]

# Economic group definitions
economic_groups = {
    'OECD': {'Germany', 'Australia', 'Austria', ...},
    'G7': {'Germany', 'Canada', 'United States', ...},
    # ... more groups
}

# Continent mapping
continent_map = {
    'Europe': {'Albania', 'Andorra', 'Austria', ...},
    'Asia': {'Afghanistan', 'Armenia', 'Azerbaijan', ...},
    # ... more continents
}
```

### Customizing Economic Groups

To add or modify economic groups, edit the `economic_groups` dictionary in `dataconvert.py`:

```python
economic_groups['Custom_Group'] = {'Country1', 'Country2', 'Country3'}
```

## Server Configuration

### Flask App Settings (`app.py`)

```python
# Server configuration
app.run(debug=True, host='0.0.0.0', port=5000)
```

- **debug=True**: Enable development mode with auto-reload
- **host='0.0.0.0'**: Allow external connections
- **port=5000**: Change the port if needed

### Production Deployment

For production use, modify the server configuration:

```python
app.run(debug=False, host='127.0.0.1', port=5000)
```

## File Structure

```
RapidStock/
│
├── app.py              # Flask backend server
├── app.js              # Frontend JavaScript logic
├── index.html          # Main web interface
├── style.css           # Styling and responsive design
├── scrapper.py         # Data scraping from stockanalysis.com
├── dataconvert.py      # Data processing and currency conversion
├── links.txt           # List of stock tickers to scrape
├── data.parquet        # Processed stock data (generated)
├── LICENSE.txt         # MIT License
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **"No module named 'X'"**: Install missing dependencies with pip
2. **"File not found: data.parquet"**: Run the scraper first
3. **Server won't start**: Check if port 5000 is available
4. **Scraper taking too long**: Reduce BATCH_SIZE or increase PAUSE_MINUTES
5. **429 Rate Limiting**: The scraper handles this automatically, but you can increase wait times

### Performance Tips

- Use SSD storage for better data.parquet read/write performance
- Increase RAM if processing large datasets
- Monitor network usage during scraping
- Use smaller batch sizes on slower connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Data Source

This application sources its data from [stockanalysis.com](https://stockanalysis.com). Please respect [their terms](https://stockanalysis.com/robots.txt) of service and use the scraper responsibly with appropriate delays.

## License

[Specify your license here]

## Support

For issues, questions, or feature requests, please [create an issue](../../issues) in the repository.

---

**⚠️ Disclaimer**: This tool is for educational and research purposes. Always verify financial data independently before making investment decisions. The developers are not responsible for any financial losses incurred from using this application.
