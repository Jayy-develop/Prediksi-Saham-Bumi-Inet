# 📈 PREDIKSI SAHAM BUMI & INET

Sistem prediksi saham **30 hari ke depan** menggunakan:
- ✨ Real Data dari **Yahoo Finance**
- 🧠 **6 ML Models** (Regression + Classification)
- 📰 **Real-time News Sentiment Analysis** (NEW!)

---

## 🚀 Quick Start

### 1️⃣ Prediksi Standar
```bash
python prediksi.py
```
Output: 30 hari prediksi BUMI & INET dengan harga terkini otomatis

### 2️⃣ Prediksi dengan Sentiment Analysis 🔥 (NEW!)
```bash
python prediksi.py --sentiment
```
Prediksi dengan real-time news sentiment → adjust trend

### 3️⃣ Prediksi dengan Harga Custom
```bash
python prediksi.py 150 180
```

### 4️⃣ Tampilkan N Hari Saja
```bash
python prediksi.py --hari 7
```

### 5️⃣ Update Data Saja
```bash
python prediksi.py --fetch
```

---

## 📰 Real-Time News Sentiment (NEW!)

Analyze news sentiment dari berbagai sumber:

### Single Analysis
```bash
python news_sentiment_v2.py
```
One-time sentiment breakdown

### Live Monitoring (Real-time updates)
```bash
python news_sentiment_v2.py --live
```
Continuous monitoring (5-minute updates)

### Custom Update Interval
```bash
python news_sentiment_v2.py --live --interval 60
```
Live monitoring dengan interval custom (detik)

---

## 📊 Prediksi Output

Tabel harian menampilkan:
- **Hari**: Nomor hari (1-30)
- **Tanggal**: Prediksi untuk tanggal apa
- **Harga**: Harga prediksi (Rp)
- **Perubahan**: Naik/turun dalam Rp & %
- **Tren**: NAIK ↑ atau TURUN ↓
- **Confidence**: Keyakinan prediksi (%)

### Contoh
```
📈 BUMI - Prediksi 30 Hari ke Depan
Hari  Tanggal      Harga        Perubahan       Trend        Confidence  
1     2026-06-07   Rp 152.45    +2.45 (+1.62%)  NAIK ↑       52.3%       
2     2026-06-08   Rp 155.20    +5.20 (+3.42%)  NAIK ↑       58.1%       
3     2026-06-09   Rp 153.80    +3.80 (+2.50%)  TURUN ↓      48.9%       
```

---

## 📁 Struktur File

```
prediksi saham/
├── 🐍 prediksi.py                 ← Main prediction engine
├── 📰 news_sentiment_v2.py         ← News & sentiment analyzer (NEW!)
├── 💾 BUMI_stock.csv               ← Historical data
├── 💾 INET_stock.csv               ← Historical data
├── 📚 README.md                    ← Dokumentasi (file ini)
└── 📊 output/
    ├── prediksi_30_hari.csv        ← Hasil prediksi
    └── sentiment_analysis.csv      ← Sentiment history (NEW!)
```

---

## 🔧 Technical Architecture

### Prediction Engine (prediksi.py)
- **Data Source**: Yahoo Finance API (yfinance)
- **Features**: 14 technical indicators
  - Moving Averages (MA5, MA10, MA20)
  - RSI (14-period)
  - Bollinger Bands
  - MACD
  - Daily Returns, Previous Close
  - OHLC prices, Volume

- **ML Models**: 6 total
  - Regression: LinearRegression, RandomForest (predict close price)
  - Classification: LogisticRegression, RandomForest (predict trend)
  - Ensemble voting untuk confidence

- **Prediction Method**:
  1. Calculate daily change % dari 30 hari terakhir
  2. Add random volatility untuk realism
  3. Vote dari 2 classifiers untuk trend
  4. Apply sentiment adjustment (opsional)
  5. Generate 30-day forecast

### Sentiment Analysis (news_sentiment_v2.py)
- **Data Sources** (multi-source):
  1. NewsAPI (global + Indonesia news)
  2. Indonesian financial news (simulated)
  3. Twitter/X sentiment (simulated)

- **Sentiment Algorithm**:
  - TextBlob polarity analysis
  - Classify: Positive / Negative / Neutral
  - Score range: -1 (very negative) to +1 (very positive)
  - Aggregate dari multiple sources
  - Confidence scoring

- **Impact on Prediction**:
  - Positive sentiment → bias to NAIK ↑
  - Negative sentiment → bias to TURUN ↓
  - Only affects first 7 days (early impact)
  - Max 50% confidence boost per sentiment

---

## 📋 Commands Reference

| Command | Description |
|---------|-------------|
| `python prediksi.py` | Basic 30-day prediction |
| `python prediksi.py --sentiment` | Prediction + sentiment |
| `python prediksi.py --hari 5` | Show only 5 days |
| `python prediksi.py 150 180` | Custom prices |
| `python prediksi.py --fetch` | Update data only |
| `python news_sentiment_v2.py` | One-time sentiment |
| `python news_sentiment_v2.py --live` | Live monitoring |
| `python news_sentiment_v2.py --live --interval 60` | Custom interval |

---

## 💡 Usage Examples

### Daily Trading Routine
```bash
# Morning - Update & predict
python prediksi.py

# Detailed analysis for today
python prediksi.py --hari 5

# Check sentiment
python news_sentiment_v2.py
```

### Scenario Testing
```bash
# Bullish scenario
python prediksi.py 160 200 --sentiment

# Bearish scenario
python prediksi.py 140 170 --sentiment

# Current with sentiment boost
python prediksi.py --sentiment --hari 10
```

### Live Sentiment Monitoring
```bash
# Start monitoring (update every 5 min)
python news_sentiment_v2.py --live

# For intraday trading (update every minute)
python news_sentiment_v2.py --live --interval 60
```

---

## 📊 Output Files

### prediksi_30_hari.csv
Hasil prediksi untuk BUMI & INET (60 rows total):
```
Saham,Hari,Tanggal,Harga_Prediksi,Perubahan_Rp,Perubahan_Persen,Tren,Confidence
BUMI,1,2026-06-07,152.45,2.45,1.62,NAIK ↑,52.3
BUMI,2,2026-06-08,155.20,5.20,3.42,NAIK ↑,58.1
INET,1,2026-06-07,185.50,-3.50,-1.86,TURUN ↓,45.2
...
```

### sentiment_analysis.csv
Sentiment history (generated dengan --live):
```
timestamp,source,title,description,sentiment_score
2026-06-06 14:28:25,Kontan,BUMI Down 2.5%,...,-0.3
2026-06-06 14:28:25,Bisnis Indonesia,INET Poised for Recovery,...,0.4
...
```

---

## ⚠️ Important Notes

### ✅ What This System Does
- ✅ Provides 30-day trend analysis
- ✅ Integrates multiple data sources (price + sentiment)
- ✅ Generates day-by-day predictions
- ✅ Adjusts for real-time news
- ✅ Exports results to CSV

### ❌ What This System Does NOT Do
- ❌ Guarantee profits or price predictions
- ❌ Replace financial advisors
- ❌ Work 100% accurately (ML is statistical)
- ❌ Predict sudden market shocks
- ❌ Replace risk management

### 📌 Usage Disclaimer
- Use as **reference only**, not as investment advice
- Always consult financial advisor
- Do proper risk management
- Market conditions change constantly
- Past performance ≠ future results

---

## 🛠️ Installation & Setup

### Requirements
- Python 3.8+
- Windows/Mac/Linux

### Install Dependencies
```bash
pip install pandas numpy scikit-learn yfinance requests textblob
```

### Verify Installation
```bash
python -c "import pandas, numpy, sklearn, yfinance, textblob; print('✅ All OK')"
```

### First Run
```bash
# Update data from Yahoo Finance
python prediksi.py --fetch

# Generate predictions
python prediksi.py

# Analyze sentiment
python news_sentiment_v2.py
```

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
pip install --upgrade pandas numpy scikit-learn yfinance requests textblob
```

### Error: File not found (prediksi_30_hari.csv)
```bash
# Generate data first
python prediksi.py --fetch
python prediksi.py
```

### Sentiment not working
Sentiment features are optional. Install:
```bash
pip install requests textblob
```

### Wrong prices
Check Yahoo Finance manually, then use custom:
```bash
python prediksi.py 150 180
```

---

## 📈 Data Quality

- **BUMI.JK**: 1200+ historical rows (5 years)
- **INET.JK**: 680+ historical rows (3 years)
- **Update**: Automatic with `--fetch`
- **Timezone**: Indonesia (WIB)

---

## 🎯 Best Practices

1. **Daily Updates**: Run `python prediksi.py --fetch` every morning
2. **Multiple Views**: Use `--hari` flag to see different timeframes
3. **Sentiment Context**: Cross-reference with `news_sentiment_v2.py`
4. **Trend Analysis**: Look at 30-day trend, not individual days
5. **Risk Management**: Always use stop-loss orders
6. **Diversification**: Don't put all capital in one stock

---

## 📞 Version & Support

- **Version**: 2.1 with Real-time Sentiment
- **Last Update**: June 6, 2026
- **Status**: ✅ Production Ready
- **Python**: 3.8+

---

## 🎓 Learn More

- **Yahoo Finance**: https://finance.yahoo.com
- **Technical Analysis**: https://en.wikipedia.org/wiki/Technical_analysis
- **ML in Finance**: https://scikit-learn.org
- **Sentiment Analysis**: https://textblob.readthedocs.io

---

**Happy Trading & Analysis!** 📊  
*Gunakan sistem ini dengan bijak & responsible*

⚡ **Last Reminder**: This is an AI-powered tool. Always verify decisions independently!
