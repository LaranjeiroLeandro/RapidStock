import pandas as pd
import requests
import re
import time

economic_groups = {
    'OECD': {'Germany', 'Australia', 'Austria', 'Belgium', 'Canada', 'Chile', 'Colombia', 'South Korea', 'Costa Rica', 'Denmark', 'Spain', 'Estonia', 'United States', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Iceland', 'Israel', 'Italy', 'Japan', 'Latvia', 'Lithuania', 'Luxembourg', 'Mexico', 'Norway', 'New Zealand', 'Netherlands', 'Poland', 'Portugal', 'Slovak Republic', 'Czech Republic', 'United Kingdom', 'Slovenia', 'Sweden', 'Switzerland', 'Turkey'},
    'G7': {'Germany', 'Canada', 'United States', 'France', 'Italy', 'Japan', 'United Kingdom', 'European Union'},
    'G20': {'South Africa', 'Germany', 'Saudi Arabia', 'Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'South Korea', 'United States', 'France', 'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'United Kingdom', 'Russia', 'Turkey', 'European Union'},
    'EU': {'Germany', 'Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Croatia', 'Denmark', 'Spain', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Czech Republic', 'Romania', 'Slovakia', 'Slovenia', 'Sweden'},
    'ASEAN': {'Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 'Vietnam'},
    'MERCOSUR': {'Argentina', 'Brazil', 'Paraguay', 'Uruguay', 'Venezuela', 'Bolivia'},
    'ECOWAS': {'Benin', 'Burkina Faso', 'Cape Verde', 'Ivory Coast', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo'},
    'UEMOA': {'Benin', 'Burkina Faso', 'Ivory Coast', 'Guinea-Bissau', 'Mali', 'Niger', 'Senegal', 'Togo'},
    'SACU': {'South Africa', 'Botswana', 'Lesotho', 'Namibia', 'Eswatini'},
    'Pacific Alliance': {'Chile', 'Colombia', 'Mexico', 'Peru'},
    'BRICS': {'Brazil', 'Russia', 'India', 'China', 'South Africa'},
    'BRICS+': {'Brazil', 'Russia', 'India', 'China', 'South Africa', 'Egypt', 'Ethiopia', 'Indonesia', 'Iran', 'Saudi Arabia', 'United Arab Emirates'},
    'G24': {'Argentina', 'Brazil', 'Colombia', 'Ivory Coast', 'Egypt', 'Ethiopia', 'Ghana', 'Guatemala', 'India', 'Iran', 'Lebanon', 'Mexico', 'Nigeria', 'Pakistan', 'Peru', 'Philippines', 'South Africa', 'Sri Lanka', 'Syria', 'Trinidad and Tobago', 'Venezuela'},
    'G15': {'Algeria', 'Argentina', 'Brazil', 'Chile', 'Egypt', 'India', 'Indonesia', 'Iran', 'Jamaica', 'Kenya', 'Malaysia', 'Mexico', 'Nigeria', 'Peru', 'Senegal', 'Sri Lanka', 'Venezuela', 'Zimbabwe'},
    'OPEC': {'Algeria', 'Angola', 'Congo', 'Equatorial Guinea', 'Gabon', 'Iran', 'Iraq', 'Kuwait', 'Libya', 'Nigeria', 'Saudi Arabia', 'United Arab Emirates', 'Venezuela'},
    'Commonwealth': {'Australia', 'Bangladesh', 'Barbados', 'Belize', 'Botswana', 'Brunei', 'Cameroon', 'Canada', 'Cyprus', 'Dominica', 'Eswatini', 'Fiji', 'Gambia', 'Ghana', 'Grenada', 'Guyana', 'India', 'Jamaica', 'Kenya', 'Kiribati', 'Lesotho', 'Malawi', 'Malaysia', 'Maldives', 'Malta', 'Mauritius', 'Mozambique', 'Namibia', 'Nauru', 'New Zealand', 'Nigeria', 'Pakistan', 'Papua New Guinea', 'Rwanda', 'Saint Lucia', 'Saint Kitts and Nevis', 'Saint Vincent and the Grenadines', 'Samoa', 'Seychelles', 'Sierra Leone', 'Singapore', 'Solomon Islands', 'South Africa', 'Sri Lanka', 'Tanzania', 'Tonga', 'Trinidad and Tobago', 'Tuvalu', 'Uganda', 'United Kingdom', 'Vanuatu', 'Zambia'},
    'Arab League': {'Algeria', 'Saudi Arabia', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt', 'United Arab Emirates', 'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 'Morocco', 'Mauritania', 'Oman', 'Palestine', 'Qatar', 'Somalia', 'Sudan', 'Syria', 'Tunisia', 'Yemen'}
}

continent_map = {
    'Europe': {'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City'},
    'North America': {'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States'},
    'South America': {'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'},
    'Asia': {'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'East Timor', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'},
    'Africa': {'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'},
    'Oceania': {'Australia', 'Cook Islands', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu'}
}

currency_cols = ['Price','Market Cap','Enterprise Value','Revenue Per Employee','Profits Per Employee','Income Tax','50-Day Moving Average','200-Day Moving Average','Revenue','Gross Profit','Operating Income','Pretax Income','Net Income','EBITDA','EBIT','Earnings Per Share (EPS)','Cash & Cash Equivalents','Total Debt','Net Cash','Net Cash Per Share','Equity (Book Value)','Book Value Per Share','Working Capital','Operating Cash Flow','Capital Expenditures','Free Cash Flow','FCF Per Share','Dividend Per Share']

multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}

def get_economic_groups(country):
    if not country:
        return ""
    groups = []
    for group_name, countries in economic_groups.items():
        if country in countries:
            groups.append(group_name)
    return ", ".join(groups)

def get_continent(country):
    if not country:
        return ""
    for continent, countries in continent_map.items():
        if country in countries:
            return continent
    return "Autre"

def get_exchange_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=10)
        rates = response.json()['rates']
        return {k: 1/v for k, v in rates.items()}
    except Exception:
        return {}

def parse_suffix_number(val):
    if pd.isna(val):
        return None
    s = str(val).replace(',', '').strip()
    match = re.match(r'^-?[\d\.]+[TBMK]?$', s, flags=re.IGNORECASE)
    if not match:
        try:
            return float(re.sub(r'[^\d\.-]', '', s))
        except ValueError:
            return None
    num = float(s[:-1]) if s[-1].upper() in multipliers else float(s)
    suffix = s[-1].upper() if s[-1].upper() in multipliers else ''
    return num * multipliers.get(suffix, 1)

def format_with_suffix(num):
    if num is None or pd.isna(num):
        return None
    absnum = abs(num)
    for suffix, factor in [('T', 1e12), ('B', 1e9), ('M', 1e6), ('K', 1e3)]:
        if absnum >= factor:
            return f"{round(num / factor, 2)}{suffix}"
    return str(round(num, 2))

def convert_to_eur_generic(val, currency, rates):
    num = parse_suffix_number(val)
    if num is None:
        return None
    rate = rates.get(currency)
    if rate is None:
        return None
    return num * rate

def process_data(input_file='data.parquet', output_file='data.parquet'):
    try:
        df = pd.read_parquet(input_file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} n'existe pas")
        return
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return

    rates = get_exchange_rates()

    for col in currency_cols:
        if col in df.columns:
            df[col] = df.apply(
                lambda row: format_with_suffix(
                    convert_to_eur_generic(row[col], row['Currency'], rates)
                ),
                axis=1
            )

    df.rename(columns={'Price': 'Price (EUR)'}, inplace=True)
    df['Economic Groups'] = df['Country'].apply(get_economic_groups)
    df['Continent'] = df['Country'].apply(get_continent)

    main_columns = ['Link', 'Company Name', 'Price (EUR)', 'Currency', 'Country', 'Continent', 'Economic Groups', 'Sector', 'Industry']
    other_columns = [c for c in df.columns if c not in main_columns]
    df = df[main_columns + other_columns]

    df.to_parquet(output_file, compression='snappy', index=False)
    print(f"Raw data saved: {len(df)} companies")

def main():
    start_time = time.time()
    process_data()
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()