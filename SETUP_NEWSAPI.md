# 🔧 SETUP REAL NEWS API

Untuk mengaktifkan **REAL-TIME NEWS** yang sebenarnya, kamu perlu setup **NewsAPI**

---

## 📝 Step 1: Daftar NewsAPI (GRATIS)

1. Buka: **https://newsapi.org/**
2. Klik **"Get API Key"** (bagian atas)
3. Isi form mendaftarkan diri (email, password)
4. Verifikasi email Anda
5. **Copy API Key** dari dashboard

💡 **Free Tier NewsAPI:**
- ✅ 100 requests per hari
- ✅ Unlimited news queries
- ✅ Support semua bahasa + Indonesia
- ✅ Real-time news dari 50+ sumber
- ✅ Publish date filtering

---

## 💾 Step 2: Setup API Key

### Option A: Environment Variable (Recommended)

**Windows:**
```bash
# Open Command Prompt dan jalankan:
set NEWSAPI_KEY=your-api-key-here

# Verify:
echo %NEWSAPI_KEY%
```

**Linux/Mac:**
```bash
# Open Terminal dan jalankan:
export NEWSAPI_KEY=your-api-key-here

# Verify:
echo $NEWSAPI_KEY

# Permanent (tambah ke ~/.bashrc atau ~/.zshrc):
echo 'export NEWSAPI_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Option B: Direct Setup (Edit File)

Edit file `config_api.py`:
```python
# Line ~10, ganti:
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')

# Dengan:
NEWSAPI_KEY = 'your-actual-api-key-here'

# Contoh:
NEWSAPI_KEY = 'e1234567890abcdef1234567890abc'
```

---

## ✅ Step 3: Test Setup

Jalankan test untuk verifikasi:
```bash
cd "D:\KECERDASAN BUATAN(AI)\prediksi saham"

# Test 1: Single analysis dengan real API
python news_sentiment_v2.py

# Output yang diharapkan:
# ✅ Downloading BUMI.JK... Found 15 articles
# ✅ Downloading INET.JK... Found 12 articles
```

---

## 🚀 Step 4: Gunakan Real System

### Analisis Sentimen Sekali Jalan
```bash
python news_sentiment_v2.py
```

Output:
```
📊 BUMI - Real Sentiment Analysis
  Searching 'BUMI.JK'... ✅ (45 found)
  📈 SENTIMENT: POSITIVE
     Score: 0.345 (polarity)
     Confidence: 78.5% ⭐
     Trend Prediction: NAIK ↑
  📊 Breakdown (45 articles):
     Strong Positive: 12
     Positive: 18
     Neutral: 10
     Negative: 5
     Strong Negative: 0
```

### Live Monitoring (Auto-Update)
```bash
# Update setiap 1 jam
python news_sentiment_v2.py --live

# Update setiap 5 menit
python news_sentiment_v2.py --live --interval 300

# Update setiap 1 menit (untuk intraday)
python news_sentiment_v2.py --live --interval 60
```

### Prediksi dengan Real Sentiment
```bash
# Jalankan prediksi dengan real sentiment
python prediksi.py --sentiment

# Lihat 5 hari dengan real sentiment
python prediksi.py --sentiment --hari 5
```

---

## 📊 Output Files (Real Data)

Setelah setup, sistem akan generate:

### `output/news_database.csv`
Database semua articles yang di-fetch:
```csv
timestamp,source,title,description,url,sentiment,polarity
2026-06-06T14:30:00,NewsAPI,"BUMI Drops 2.5% Amid...",full description,https://...,N/A,0.0
2026-06-06T14:30:00,NewsAPI,"INET Poised for Recovery",full description,https://...,N/A,0.0
```

### `output/sentiment_history.csv`
Historical sentiment analysis:
```csv
timestamp,stock,sentiment,confidence,score,total_articles
2026-06-06T14:30:00,BUMI,POSITIVE,0.785,0.345,45
2026-06-06T14:30:00,INET,NEUTRAL,0.612,0.102,38
2026-06-06T15:30:00,BUMI,POSITIVE,0.812,0.378,52
```

---

## 🔍 Real Confidence Calculation

Confidence score dihitung dari **REAL DATA**:

```
Confidence = 
  + 20% × Sentiment Strength (polarity)
  + 15% × Article Count (lebih banyak = lebih confident)
  + 15% × Sentiment Consistency (konsistensi voting)
  + 20% × Polarity Magnitude (seberapa kuat signal)
  + 30% × Analyzer Confidence (TextBlob scoring)

Range: 0-100%
```

### Contoh Real Calculation:
```
BUMI News:
- 45 articles found
- Polarity: +0.345
- Sentiment: POSITIVE
- Consistency: 40% (18 positive dari 45)

Confidence = 20% × 0.345 + 15% × 1.0 + 15% × 0.40 + 20% × 0.345 + 30% × 0.78
           = 0.069 + 0.15 + 0.06 + 0.069 + 0.234
           = 0.582 = 58.2% ⭐
```

---

## 📈 Multi-Source News Strategy

Sistem fetch dari **multiple keywords** untuk akurasi lebih tinggi:

```python
SEARCH_KEYWORDS = {
    'BUMI': [
        'BUMI.JK',
        'PT Bumi Resources',
        'Bumi Resources Mineral',
        'coal Indonesia'  # Relevant industry
    ],
    'INET': [
        'INET.JK',
        'PT Indonesia Energy',
        'Indonesia Energy',
        'INET stock'
    ],
    'GENERAL': [
        'Indonesia stock market',
        'IDX',
        'Jakarta stock exchange'
    ]
}
```

Setiap stock search dengan 4 keyword × 15 articles = 60 potential articles

---

## 🛠️ Troubleshooting

### Error: "NEWSAPI_KEY tidak ditemukan"
**Solution:**
```bash
# Set environment variable
set NEWSAPI_KEY=your-key-here

# Verify
python -c "import os; print(os.getenv('NEWSAPI_KEY'))"
```

### Error: "API request failed"
**Possible causes:**
1. API key salah → re-check di https://newsapi.org/
2. Quota habis → tunggu 24 jam (reset daily)
3. Network issue → check internet connection

**Solution:**
```bash
# Test API key
python -c "
import requests
api_key = 'your-key-here'
url = f'https://newsapi.org/v2/everything?q=bitcoin&apiKey={api_key}&pageSize=1'
response = requests.get(url)
print('✅ API OK' if response.status_code == 200 else '❌ API Error')
"
```

### Error: "No articles found"
1. Check keyword relevance
2. Try different search terms
3. Verify API key quota (100 requests/day limit)

### Sentiment Confidence 0%
1. No articles found
2. Text too short to analyze
3. TextBlob not trained for that language

---

## 💡 Best Practices

1. **Set API key sebagai environment variable** (jangan commit ke git)
2. **Jangan hardcode API key** di source code
3. **Monitor quota** (100 requests/hari = ~3-4 updates)
4. **Cache hasil** untuk avoid redundant API calls
5. **Use --live mode** untuk automated monitoring

---

## 🎯 Production Setup

Untuk production deployment:

```bash
# 1. Setup environment variable (OS level)
# Jangan set di terminal, set di Windows Environment Variables

# 2. Start live monitoring (background)
python news_sentiment_v2.py --live --interval 3600 &

# 3. Integrate dengan prediksi
python prediksi.py --sentiment

# 4. Monitor logs
tail -f output/news_sentiment_log.txt
```

---

## 📞 Support

- **NewsAPI Docs**: https://newsapi.org/docs
- **API Status**: https://newsapi.org/account/api-status
- **Usage Calculator**: https://newsapi.org/account/request-history

---

## ✅ Checklist

- [ ] Daftar di https://newsapi.org/
- [ ] Copy API Key
- [ ] Setup NEWSAPI_KEY environment variable
- [ ] Test: `python news_sentiment_v2.py`
- [ ] Verify CSV files created
- [ ] Run live monitoring
- [ ] Integrate dengan prediksi
- [ ] Monitor sentiment history

---

**Siap!** System sudah connect dengan **REAL NEWS DATA** dari seluruh dunia! 🌍📰
