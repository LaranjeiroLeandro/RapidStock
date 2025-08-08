from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from pathlib import Path
import re

app = Flask(__name__)

class StockFilter:
    def __init__(self, path='data.parquet'):
        self.df = pd.read_parquet(path) if Path(path).exists() else pd.DataFrame()
        if self.df.empty: return
        
        for col in self.df.select_dtypes(include='object').columns:
            if f"{col}_numeric" in self.df.columns: continue
            
            sample = self.df[col].dropna().head(10).astype(str)
            
            if sample.str.contains(r'^-?\$?-?[\d,]+\.?\d*[TBMK]?$', regex=True, na=False).any():
                self.df[f"{col}_numeric"] = self.df[col].apply(self._parse_currency)
            elif sample.str.contains(r'^-?\d+\.?\d*%$', regex=True, na=False).any():
                self.df[f"{col}_numeric"] = self.df[col].apply(self._parse_percent)

    def _parse_currency(self, val):
        if pd.isna(val) or val == '-': return np.nan
        val = re.sub(r'[\$€,]', '', str(val).strip())
        multiplier = {'T': 1e12,'B': 1e9, 'M': 1e6, 'K': 1e3}.get(val[-1:], 1)
        if val[-1:] in 'TBMK': val = val[:-1]
        try: return float(val) * multiplier
        except: return np.nan

    def _parse_percent(self, val):
        if pd.isna(val) or val == '-': return np.nan
        try: return float(str(val).rstrip('%')) / 100
        except: return np.nan

    def apply_criteria(self, criteria):
        if self.df.empty: return {'data': [], 'columns': []}
        
        df = self.df.copy()
        
        grouped = {}
        for c in criteria:
            col = c['criterion']
            if col not in grouped: grouped[col] = []
            grouped[col].append(c)
        
        for column, crits in grouped.items():
            if column not in df.columns: continue
            
            column_masks = []
            for crit in crits:
                mask = self._apply_single_criterion(df, crit)
                if mask is not None: column_masks.append(mask)
            
            if column_masks:
                combined_mask = column_masks[0]
                for mask in column_masks[1:]:
                    combined_mask = combined_mask | mask
                df = df.loc[combined_mask.fillna(False)]
        
        result_cols = [c for c in self.df.columns if not c.endswith('_numeric')]
        return {'data': df[result_cols].fillna('-').to_dict('records'), 'columns': result_cols}

    def _apply_single_criterion(self, df, criterion):
        column = criterion['criterion']
        operator = criterion['operator']
        value = criterion['value']
        value_type = criterion.get('type', 'text')
        
        try:
            if operator == 'contains':
                return df[column].astype(str).str.contains(str(value), case=False, na=False, regex=False)
            
            if column == 'Economic Groups' and operator == '==':
                def check_group_membership(cell_value):
                    if pd.isna(cell_value): return False
                    groups = [g.strip() for g in str(cell_value).split(',')]
                    return value in groups
                return df[column].apply(check_group_membership)
            
            target_col = column
            parsed_val = value
            
            if value_type in ['currency', 'percent', 'numeric']:
                numeric_col = f"{column}_numeric"
                if numeric_col in df.columns:
                    target_col = numeric_col
                
                if value_type == 'percent':
                    parsed_val = float(value) / 100
                else:
                    parsed_val = float(value)
            
            ops = {'==': lambda x, y: x == y, '!=': lambda x, y: x != y,
                   '>': lambda x, y: x > y, '<': lambda x, y: x < y,
                   '>=': lambda x, y: x >= y, '<=': lambda x, y: x <= y}
            
            return ops.get(operator, lambda x, y: False)(df[target_col], parsed_val)
            
        except Exception as e:
            print(f"Error: {e}")
            return None

filter_engine = StockFilter()

@app.route('/Rapistock.png')

@app.route('/')
def index():
    return Path('index.html').read_text(encoding='utf-8')

@app.route('/filter', methods=['POST'])
def filter_stocks():
    try:
        criteria = request.get_json(silent=True).get('criteria', [])
        return jsonify(filter_engine.apply_criteria(criteria) if criteria else {'error': 'No criteria'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/style.css')
def style():
    return Path('style.css').read_text(encoding='utf-8'), 200, {'Content-Type': 'text/css'}

@app.route('/app.js')
def script():
    return Path('app.js').read_text(encoding='utf-8'), 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)