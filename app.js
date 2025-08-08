let criteria = [];

const DEFAULT_OPS = {
  select: ['==', '!=', 'contains'],
  selectSimple: ['==', '!='],
  text: ['==', '!=', 'contains'],
  numeric: ['>', '<', '>=', '<=', '==', '!='],
  currency: ['>', '<', '>=', '<=', '==', '!='],
  percent: ['>', '<', '>=', '<=', '==', '!=']
};

const COLUMN_TYPES = {
  'Company Name': {type: 'text'},
  'Price (EUR)': {type: 'currency'},
  'Country': {type: 'select', values: ['Afghanistan', 'South Africa', 'Albania', 'Algeria', 'Germany', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Saudi Arabia', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Belarus', 'Myanmar', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chile', 'China', 'Cyprus', 'Colombia', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Cook Islands', 'North Korea', 'South Korea', 'Costa Rica', 'Ivory Coast', 'Croatia', 'Cuba', 'Denmark', 'Djibouti', 'Dominica', 'Egypt', 'United Arab Emirates', 'Ecuador', 'Eritrea', 'Spain', 'Estonia', 'Eswatini', 'United States', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Equatorial Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Solomon Islands', 'India', 'Indonesia', 'Iraq', 'Iran', 'Ireland', 'Iceland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Kiribati', 'Kuwait', 'Laos', 'Lesotho', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'North Macedonia', 'Madagascar', 'Malaysia', 'Malawi', 'Maldives', 'Mali', 'Malta', 'Morocco', 'Marshall Islands', 'Mauritius', 'Mauritania', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Mozambique', 'Namibia', 'Nauru', 'Nepal', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'New Zealand', 'Oman', 'Uganda', 'Uzbekistan', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Netherlands', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'United Kingdom', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'San Marino', 'Saint Vincent and the Grenadines', 'Saint Lucia', 'El Salvador', 'Samoa', 'Sao Tome and Principe', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'Sudan', 'South Sudan', 'Sri Lanka', 'Sweden', 'Switzerland', 'Suriname', 'Syria', 'Tajikistan', 'Tanzania', 'Chad', 'Czech Republic', 'Thailand', 'East Timor', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkmenistan', 'Turkey', 'Tuvalu', 'Ukraine', 'Uruguay', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']},
  'Continent': {'type': 'select', 'values': ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']},
  'Economic Groups': {type: 'select', values: ['OECD', 'G7', 'G20', 'EU', 'ASEAN', 'MERCOSUR', 'ECOWAS', 'UEMOA', 'SACU', 'Pacific Alliance', 'BRICS', 'BRICS+', 'G24', 'G15', 'OPEC', 'Commonwealth', 'Arab League']},
  'Sector': {type: 'select', values: ['Healthcare', 'Financials', 'Technology', 'Industrials', 'Consumer Discretionary', 'Materials', 'Real Estate', 'Communication Services', 'Energy', 'Consumer Staples', 'Utilities']},
  'Industry': {type: 'select', values: ['Biotechnology', 'Banks - Regional', 'Software - Application', 'Software - Infrastructure', 'Medical Devices', 'Shell Companies', 'Asset Management', 'Oil & Gas Exploration & Production', 'Drug Manufacturers - Specialty & Generic', 'Specialty Industrial Machinery', 'Aerospace & Defense', 'Capital Markets', 'Internet Content & Information', 'Information Technology Services', 'Semiconductors', 'Packaged Foods', 'Medical Instruments & Supplies', 'Auto Parts', 'Specialty Chemicals', 'Oil & Gas Midstream', 'Telecom Services', 'Restaurants', 'Credit Services', 'Diagnostics & Research', 'Oil & Gas Equipment & Services', 'Medical Care Facilities', 'Health Information Services', 'Communication Equipment', 'Engineering & Construction', 'Electrical Equipment & Parts', 'Gold', 'Entertainment', 'Specialty Retail', 'Electronic Components', 'Specialty Business Services', 'Insurance - Property & Casualty', 'Real Estate Services', 'Other Industrial Metals & Mining', 'Education & Training Services', 'Advertising Agencies', 'Utilities - Regulated Electric', 'Internet Retail', 'REIT - Mortgage', 'Marine Shipping', 'Building Products & Equipment', 'Furnishings,Fixtures & Appliances', 'Computer Hardware', 'Apparel Retail', 'Scientific & Technical Instruments', 'Auto Manufacturers', 'Semiconductor Equipment & Materials', 'Household & Personal Products', 'Leisure', 'Auto & Truck Dealerships', 'REIT - Retail', 'Steel', 'Integrated Freight & Logistics', 'Farm & Heavy Construction Machinery', 'Apparel Manufacturing', 'Packaging & Containers', 'REIT - Office', 'Solar', 'Security & Protection Services', 'Conglomerates', 'Electronic Gaming & Multimedia', 'Insurance Brokers', 'Oil & Gas Integrated', 'Farm Products', 'REIT - Residential', 'Staffing & Employment Services', 'Residential Construction', 'Drug Manufacturers - General', 'Rental & Leasing Services', 'Utilities - Renewable', 'Industrial Distribution', 'Banks - Diversified', 'Airlines', 'Consumer Electronics', 'Travel Services', 'Insurance - Specialty', 'Pollution & Treatment Controls', 'Waste Management', 'REIT - Specialty', 'Metal Fabrication', 'Resorts & Casinos', 'Oil & Gas Refining & Marketing', 'Insurance - Life', 'Gambling', 'REIT - Healthcare Facilities', 'Beverages - Non-Alcoholic', 'Trucking', 'Chemicals', 'REIT - Industrial', 'REIT - Diversified', 'Real Estate - Development', 'Consulting Services', 'REIT - Hotel & Motel', 'Agricultural Inputs', 'Building Materials', 'Footwear & Accessories', 'Utilities - Regulated Gas', 'Recreational Vehicles', 'Personal Services', 'Financial Data & Stock Exchanges', 'Food Distribution', 'Utilities - Regulated Water', 'Other Precious Metals & Mining', 'Lodging', 'Broadcasting', 'Mortgage Finance', 'Insurance - Diversified', 'Medical Distribution', 'Healthcare Plans', 'Beverages - Wineries & Distilleries', 'Railroads', 'Grocery Stores', 'Luxury Goods', 'Electronics & Computer Distribution', 'Tobacco', 'Uranium', 'Tools & Accessories', 'Utilities - Diversified', 'Airports & Air Services', 'Discount Stores', 'Oil & Gas Drilling', 'Publishing', 'Beverages - Brewers', 'Home Improvement Retail', 'Pharmaceutical Retailers', 'Utilities - Independent Power Producers', 'Insurance - Reinsurance', 'Copper', 'Financial Conglomerates', 'Coking Coal', 'Thermal Coal', 'Lumber & Wood Production', 'Paper & Paper Products', 'Silver', 'Aluminum', 'Business Equipment & Supplies', 'Confectioners', 'Textile Manufacturing', 'Department Stores', 'Real Estate - Diversified', 'Infrastructure Operations']},
  'Market Cap': {type: 'currency'},
  'Enterprise Value': {type: 'currency'},
  'Earnings Date': {type: 'text'},
  'Ex-Dividend Date': {type: 'text'},
  'Current Share Class': {type: 'text'},
  'Shares Outstanding': {type: 'numeric'},
  'Shares Change (YoY)': {type: 'percent'},
  'Shares Change (QoQ)': {type: 'percent'},
  'Owned by Insiders (%)': {type: 'percent'},
  'Owned by Institutions (%)': {type: 'percent'},
  'Float': {type: 'numeric'},
  'PE Ratio': {type: 'numeric'},
  'Forward PE': {type: 'numeric'},
  'PS Ratio': {type: 'numeric'},
  'PB Ratio': {type: 'numeric'},
  'P/TBV Ratio': {type: 'numeric'},
  'P/FCF Ratio': {type: 'numeric'},
  'P/OCF Ratio': {type: 'numeric'},
  'PEG Ratio': {type: 'numeric'},
  'EV / Earnings': {type: 'numeric'},
  'EV / Sales': {type: 'numeric'},
  'EV / EBITDA': {type: 'numeric'},
  'EV / EBIT': {type: 'numeric'},
  'EV / FCF': {type: 'numeric'},
  'Current Ratio': {type: 'numeric'},
  'Quick Ratio': {type: 'numeric'},
  'Debt / Equity': {type: 'numeric'},
  'Debt / EBITDA': {type: 'numeric'},
  'Debt / FCF': {type: 'numeric'},
  'Interest Coverage': {type: 'numeric'},
  'Return on Equity (ROE)': {type: 'percent'},
  'Return on Assets (ROA)': {type: 'percent'},
  'Return on Invested Capital (ROIC)': {type: 'percent'},
  'Return on Capital Employed (ROCE)': {type: 'percent'},
  'Revenue Per Employee': {type: 'currency'},
  'Profits Per Employee': {type: 'currency'},
  'Employee Count': {type: 'numeric'},
  'Asset Turnover': {type: 'numeric'},
  'Inventory Turnover': {type: 'numeric'},
  'Income Tax': {type: 'currency'},
  'Effective Tax Rate': {type: 'percent'},
  'Beta (5Y)': {type: 'numeric'},
  '52-Week Price Change': {type: 'percent'},
  '50-Day Moving Average': {type: 'currency'},
  '200-Day Moving Average': {type: 'currency'},
  'Relative Strength Index (RSI)': {type: 'numeric'},
  'Average Volume (20 Days)': {type: 'numeric'},
  'Short Interest': {type: 'numeric'},
  'Short Previous Month': {type: 'numeric'},
  'Short % of Shares Out': {type: 'percent'},
  'Short % of Float': {type: 'percent'},
  'Short Ratio (days to cover)': {type: 'numeric'},
  'Revenue': {type: 'currency'},
  'Gross Profit': {type: 'currency'},
  'Operating Income': {type: 'currency'},
  'Pretax Income': {type: 'currency'},
  'Net Income': {type: 'currency'},
  'EBITDA': {type: 'currency'},
  'EBIT': {type: 'currency'},
  'Earnings Per Share (EPS)': {type: 'currency'},
  'Cash & Cash Equivalents': {type: 'currency'},
  'Total Debt': {type: 'currency'},
  'Net Cash': {type: 'currency'},
  'Net Cash Per Share': {type: 'currency'},
  'Equity (Book Value)': {type: 'currency'},
  'Book Value Per Share': {type: 'currency'},
  'Working Capital': {type: 'currency'},
  'Operating Cash Flow': {type: 'currency'},
  'Capital Expenditures': {type: 'currency'},
  'Free Cash Flow': {type: 'currency'},
  'FCF Per Share': {type: 'currency'},
  'Gross Margin': {type: 'percent'},
  'Operating Margin': {type: 'percent'},
  'Pretax Margin': {type: 'percent'},
  'Profit Margin': {type: 'percent'},
  'EBITDA Margin': {type: 'percent'},
  'EBIT Margin': {type: 'percent'},
  'FCF Margin': {type: 'percent'},
  'Dividend Per Share': {type: 'currency'},
  'Dividend Yield': {type: 'percent'},
  'Dividend Growth (YoY)': {type: 'percent'},
  'Years of Dividend Growth': {type: 'numeric'},
  'Payout Ratio': {type: 'percent'},
  'Buyback Yield': {type: 'percent'},
  'Shareholder Yield': {type: 'percent'},
  'Earnings Yield': {type: 'percent'},
  'FCF Yield': {type: 'percent'},
};

const getColumnOps = c => COLUMN_TYPES[c]?.ops || DEFAULT_OPS[COLUMN_TYPES[c]?.type] || DEFAULT_OPS.numeric;
const opLabels = {'==':'=','!=':'≠','>=':'≥','<=':'≤','contains':'contains'};

$(() => {
  const $crit = $('#crit'), $op = $('#op'), $crits = $('#crits'), $results = $('#results');

  $(document).on('keypress', '#val', e => {
    if (e.key === 'Enter') {
        $('#addCrit').click();
    }
  });

  const updateValueInput = c => {
    const inputs = {
      select: () => `<input id="val" type="text" list="values-list" placeholder="&nbsp;Start typing to search...&nbsp;"><datalist id="values-list">${c.values.map(v=>`<option value="${v}"></option>`).join('')}</datalist>`,
      selectSimple: () => `<input id="val" type="text" list="values-list" placeholder="&nbsp;Start typing to search...&nbsp;"><datalist id="values-list">${c.values.map(v=>`<option value="${v}"></option>`).join('')}</datalist>`,
      currency: () => '<input id="val" type="number" step="0.01" placeholder="&nbsp;Value in $ (without symbol)...&nbsp;">',
      percent: () => '<input id="val" type="number" step="0.01" placeholder="&nbsp;Percentage value...&nbsp;">',
      numeric: () => '<input id="val" type="number" step="0.01" placeholder="&nbsp;Numeric value...&nbsp;">',
      text: () => '<input id="val" type="text" placeholder="&nbsp;Text value...&nbsp;">'
    };
    $('#val').replaceWith(inputs[c.type]||inputs.text());
};

  $crit.on('change', () => {
    const c = COLUMN_TYPES[$crit.val()];
    if(!c) return $op.html('<option>&nbsp;Operator...&nbsp;</option>');
    $op.html(getColumnOps($crit.val()).map(op=>`<option value="${op}">&nbsp;${opLabels[op]||op}&nbsp;</option>`).join(''));
    updateValueInput(c);
  });

  $('#addCrit').click(() => {
    const c = $crit.val()?.trim(), o = $op.val(), v = $('#val').val()?.trim();
    if (!c || !o || !v || !COLUMN_TYPES[c] || !getColumnOps(c).includes(o)) {
      return alert('Please check the entered fields');
    }
    
    criteria.push({criterion:c,operator:o,value:v,type:COLUMN_TYPES[c].type});
    updateCriteriaDisplay();
    $crit.val(''); 
    $op.html('<option>&nbsp;Operator...&nbsp;</option>');
    $('#val').replaceWith('<input id="val" type="text" placeholder="&nbsp;Value...&nbsp;">');
  });

  $('#clearBtn').click(() => {
    criteria = [];
    updateCriteriaDisplay();
    $results.empty();
  });

  $('#filterBtn').click(async () => {
    if(!criteria.length) return alert('No criteria defined');
    $results.html('<div class="loading">&nbsp;Processing&nbsp;</div>');
    try {
      const res = await fetch('/filter',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({criteria})});
      const data = await res.json();
      data.error?$results.html(`<p style="color:red;">&nbsp;Error: ${data.error}&nbsp;</p>`):displayResults(data);
    } catch(e) {
      $results.html(`<p style="color:red;">&nbsp;Connection error: ${e.message}&nbsp;</p>`);
    }
  });

  const updateCriteriaDisplay = () => {
    $crits.html(criteria.length ? criteria.map((c,i) => 
      `<button class="criterion-btn" data-index="${i}">&nbsp;${c.criterion} ${opLabels[c.operator]||c.operator} ${c.value} ×&nbsp;</button>`
    ).join('') : '<p class="hint">&nbsp;No criteria&nbsp;</p>');
  };

  $crits.on('click','.criterion-btn',function(){
    criteria.splice($(this).data('index'),1);
    updateCriteriaDisplay();
  });

  const displayResults = r => {
    const data = r.data||r, cols = r.columns||data[0]&&Object.keys(data[0])||[];
    if(!data.length) return $results.html('<p>&nbsp;No companies match the criteria.&nbsp;</p>');
    $results.html(`
      <table>
        <thead><tr>${cols.map(c=>`<th>&nbsp;${c}&nbsp;</th>`).join('')}</tr></thead>
        <tbody>${data.map(row=>`<tr>${cols.map(c=>`<td>&nbsp;${row[c]||'-'}&nbsp;</td>`).join('')}</tr>`).join('')}</tbody>
      </table>
      <p><strong>&nbsp;${data.length}</strong> company(ies) found&nbsp;</p>
      <p class="hint">&nbsp;💡 You can select and copy table cells&nbsp;</p>
    `);
  };

  updateCriteriaDisplay();
  $crit.trigger('change');
});