#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask application wrapper for BUMI & INET Stock Prediction System
For WSGI compatibility (deployment on PythonAnywhere).
"""

import os
import json
import csv
import subprocess
import sys
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='public', static_url_path='')

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output')

# Helper to read CSV safely
def read_csv_to_json(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"Error reading CSV {filepath}: {e}")
        return []

# Helper to load stock csv (raw historical)
def load_historical_data(filepath, limit=150):
    if not os.path.exists(filepath):
        return []
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split(',')
            if not parts or len(parts) < 6:
                continue
            date_str = parts[0]
            # Match date format YYYY-MM-DD
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                try:
                    data.append({
                        'Date': date_str,
                        'Close': round(float(parts[1]), 2),
                        'High': round(float(parts[2]), 2),
                        'Low': round(float(parts[3]), 2),
                        'Open': round(float(parts[4]), 2),
                        'Volume': int(float(parts[5])) if parts[5] else 0
                    })
                except ValueError:
                    pass
        # Return the last N items
        return data[-limit:]
    except Exception as e:
        print(f"Error parsing historical CSV {filepath}: {e}")
        return []

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory('public', 'index.html')

@app.route('/index.css')
def index_css():
    return send_from_directory('public', 'index.css')

@app.route('/app.js')
def app_js():
    return send_from_directory('public', 'app.js')

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/api/stock_info')
def api_stock_info():
    bumi_hist = load_historical_data(os.path.join(WORKSPACE_DIR, 'BUMI_stock.csv'), limit=1)
    inet_hist = load_historical_data(os.path.join(WORKSPACE_DIR, 'INET_stock.csv'), limit=1)
    
    info = {
        'BUMI': {
            'symbol': 'BUMI.JK',
            'current_price': bumi_hist[0]['Close'] if bumi_hist else None,
            'date': bumi_hist[0]['Date'] if bumi_hist else None
        },
        'INET': {
            'symbol': 'INET.JK',
            'current_price': inet_hist[0]['Close'] if inet_hist else None,
            'date': inet_hist[0]['Date'] if inet_hist else None
        }
    }
    return jsonify(info)

@app.route('/api/historical')
def api_historical():
    symbol = request.args.get('symbol', 'BUMI')
    limit = int(request.args.get('limit', 150))
    filename = f"{symbol}_stock.csv"
    filepath = os.path.join(WORKSPACE_DIR, filename)
    return jsonify(load_historical_data(filepath, limit))

@app.route('/api/predictions')
def api_predictions():
    filepath = os.path.join(OUTPUT_DIR, 'prediksi_30_hari.csv')
    return jsonify(read_csv_to_json(filepath))

@app.route('/api/sentiment')
def api_sentiment():
    filepath = os.path.join(OUTPUT_DIR, 'sentiment_history.csv')
    history = read_csv_to_json(filepath)
    
    latest_sentiment = {}
    for item in reversed(history):
        stock = item.get('stock')
        if stock not in latest_sentiment:
            latest_sentiment[stock] = item
        if len(latest_sentiment) >= 2:
            break
    return jsonify(latest_sentiment)

@app.route('/api/news')
def api_news():
    filepath = os.path.join(OUTPUT_DIR, 'news_database.csv')
    news = read_csv_to_json(filepath)
    
    try:
        news.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    except:
        pass
    
    symbol = request.args.get('symbol')
    if symbol:
        filtered_news = []
        keywords = [symbol.lower()]
        if symbol.upper() == 'BUMI':
            keywords.extend(['resources', 'coal', 'mineral'])
        elif symbol.upper() == 'INET':
            keywords.extend(['energy', 'indonesia energy'])
        
        for item in news:
            text_to_search = (item.get('title', '') + ' ' + item.get('description', '')).lower()
            if any(kw in text_to_search for kw in keywords):
                filtered_news.append(item)
        return jsonify(filtered_news[:30])
    return jsonify(news[:40])

@app.route('/api/evaluation')
def api_evaluation():
    eval_data = {}
    for stock in ['BUMI', 'INET']:
        eval_data[stock] = {
            'regression': read_csv_to_json(os.path.join(OUTPUT_DIR, f'eval_regression_{stock}.csv')),
            'classification': read_csv_to_json(os.path.join(OUTPUT_DIR, f'eval_classification_{stock}.csv'))
        }
    return jsonify(eval_data)

@app.route('/api/run_prediction', methods=['POST'])
def api_run_prediction():
    params = request.get_json() or {}
    harga_bumi = params.get('harga_bumi')
    harga_inet = params.get('harga_inet')
    sentiment = params.get('sentiment', True)
    days = params.get('days', 30)

    cmd = [sys.executable, 'prediksi.py']
    if harga_bumi is not None and harga_inet is not None:
        cmd.append(str(harga_bumi))
        cmd.append(str(harga_inet))
    if sentiment:
        cmd.append('--sentiment')
    cmd.extend(['--hari', str(days)])
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_DIR, encoding='utf-8')
        return jsonify({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'stderr': f"Execution error: {e}",
            'stdout': "",
            'code': -1
        })

@app.route('/api/run_news_fetch', methods=['POST'])
def api_run_news_fetch():
    cmd = [sys.executable, 'news_sentiment_v2.py']
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_DIR, encoding='utf-8')
        return jsonify({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'stderr': f"Execution error: {e}",
            'stdout': "",
            'code': -1
        })

if __name__ == '__main__':
    app.run(port=8000, debug=True)
