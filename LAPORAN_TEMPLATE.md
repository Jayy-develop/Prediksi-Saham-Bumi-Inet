# LAPORAN PROYEK MACHINE LEARNING: PREDIKSI HARGA SAHAM BUMI & INET

## 1. Pendahuluan & Latar Belakang
Proyek ini bertujuan untuk memprediksi harga saham 30 hari ke depan serta arah pergerakan tren (Naik/Turun) untuk saham **PT Bumi Resources Tbk (BUMI.JK)** dan **PT Indonesia Energy Corporation Tbk (INET.JK)**. Proyek ini mengintegrasikan data pergerakan harga historis dengan analisis sentimen berita terkini secara real-time guna memperkuat akurasi prediksi.

---

## 2. Dataset
Dataset yang digunakan diperoleh dari Yahoo Finance API menggunakan pustaka `yfinance`:
* **BUMI_stock.csv**: Berisi data historis pergerakan harga saham BUMI (1,200+ baris).
* **INET_stock.csv**: Berisi data historis pergerakan harga saham INET (680+ baris).
* **Fitur yang Diekstrak**:
  * Fitur Harga OHLC: `Open`, `High`, `Low`, `Close`, `Volume`.
  * Rata-rata Bergerak (Moving Averages): `MA5`, `MA10`, `MA20`.
  * Indikator Momentum: `RSI` (14-period).
  * Saluran Volatilitas: `Bollinger Bands` (`BB_Upper`, `BB_Lower`, `BB_Mid`).
  * Tren Makro: `MACD` (Moving Average Convergence Divergence).
  * Keuntungan Harian & Kemarin: `Return`, `Prev_Close`.

---

## 3. Metodologi & Algoritma Supervised Machine Learning
Proyek ini mengimplementasikan **4 algoritma supervised machine learning** yang terbagi dalam dua tugas utama:

### A. Regresi (Prediksi Nilai Harga Saham)
1. **Linear Regression (LR)**: Algoritma statistik sederhana yang memodelkan hubungan linear antara fitur teknikal dan harga penutupan esok hari.
2. **Random Forest Regressor (RFR)**: Metode ensemble berbasis pohon keputusan yang menangkap pola non-linear dan interaksi kompleks antar indikator teknikal.

### B. Klasifikasi (Prediksi Arah Tren - Naik/Turun)
3. **Logistic Regression (LogReg)**: Algoritma klasifikasi linear untuk mengestimasi probabilitas tren pergerakan harga esok hari (Naik = 1, Turun = 0).
4. **Random Forest Classifier (RFC)**: Klasifikator ensemble berbasis pohon keputusan untuk memprediksi arah tren dengan voting mayoritas pohon.

---

## 4. Analisis & Perbandingan Hasil Evaluasi Model
Data dibagi menjadi **80% training** dan **20% testing** secara sekuensial (untuk menghindari bias data deret waktu).

### A. Perbandingan Model Regresi (Prediksi Harga)

| Saham | Algoritma | RMSE | MAE | R-Squared (R2) |
|---|---|---|---|---|
| **BUMI** | **Linear Regression** | **14.6491** | **8.3823** | **0.9737** (Sangat Baik) |
| **BUMI** | Random Forest | 80.4638 | 48.1082 | 0.2077 |
| **INET** | **Linear Regression** | **56.7831** | **33.8220** | **0.9046** (Sangat Baik) |
| **INET** | Random Forest | 186.2424 | 113.1292 | -0.0261 |

*Analisis*: Linear Regression terbukti jauh lebih unggul dan stabil untuk model regresi satu langkah ke depan (*one-step-ahead prediction*) dengan nilai $R^2$ mencapai **97.37% (BUMI)** dan **90.46% (INET)**. Model Random Forest Regressor mengalami *overfitting* pada data training sehingga menghasilkan kinerja buruk ($R^2$ rendah/negatif) di data testing yang belum pernah dilihat sebelumnya.

### B. Perbandingan Model Klasifikasi (Prediksi Tren Pergerakan)

| Saham | Algoritma | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|---|
| **BUMI** | **Logistic Regression** | **61.60%** | **60.00%** | 9.57% | 16.51% |
| **BUMI** | Random Forest | 55.27% | 31.25% | 10.64% | 15.87% |
| **INET** | **Logistic Regression** | **52.63%** | **44.30%** | **64.81%** | **52.63%** |
| **INET** | Random Forest | 46.62% | 31.11% | 25.93% | 28.28% |

*Analisis*: Untuk tugas klasifikasi arah tren, **Logistic Regression** mengungguli Random Forest Classifier di kedua saham dengan akurasi mencapai **61.60%** pada saham BUMI dan **52.63%** pada saham INET. 

---

## 5. Integrasi Sentimen Berita Nyata (NewsAPI & TextBlob NLP)
Untuk memperkuat prediksi deret waktu murni, proyek ini menggunakan **RealNewsAPI** untuk menarik berita finansial terkait BUMI dan INET secara real-time. Sentimen dianalisis menggunakan TextBlob NLP:
* **Sentimen Positif**: Memberikan dorongan (*boost*) peningkatan probabilitas dan tingkat keyakinan (confidence) tren Naik.
* **Sentimen Negatif**: Memberikan bias penurunan tren ke Arah Turun.
* **Integrasi**: Sentimen diterapkan pada 7 hari pertama proyeksi untuk memberikan pengaruh psikologis pasar jangka pendek.

---

## 6. Visualisasi Hasil Proyek

Berikut adalah grafik visualisasi hasil proyek yang otomatis disimpan dalam folder `output/`:

### A. Grafik Evaluasi Model Regresi (Actual vs Predicted)
Grafik ini membandingkan data aktual pada test set dengan nilai yang diprediksi oleh algoritma terbaik (Linear Regression):
* **BUMI**: ![BUMI Evaluasi Plot](output/eval_actual_vs_pred_BUMI.png)
* **INET**: ![INET Evaluasi Plot](output/eval_actual_vs_pred_INET.png)

### B. Grafik Proyeksi Prediksi 30 Hari Ke Depan
Grafik ini menggabungkan 60 hari data historis terakhir dengan 30 hari proyeksi harga saham masa depan secara dinamis:
* **BUMI**: ![BUMI Prediksi Plot](output/visualisasi_prediksi_30_hari_BUMI.png)
* **INET**: ![INET Prediksi Plot](output/visualisasi_prediksi_30_hari_INET.png)

---

## 7. Kesimpulan & Saran
1. **Algoritma Supervised Terbaik**: Linear Regression adalah model terbaik untuk estimasi harga, sementara Logistic Regression adalah model terbaik untuk klasifikasi arah pergerakan tren.
2. **Kesesuaian Proyek**: Proyek ini telah berhasil mengintegrasikan model machine learning dengan data eksternal (sentimen berita) secara sukses dan dinamis.
3. **Saran Pengembangan**:
   * Menambahkan tuning hiperparameter (*GridSearchCV*) pada model Random Forest untuk mengurangi *overfitting*.
   * Menggunakan model sekuensial yang lebih kompleks seperti LSTM atau GRU jika ingin memperpanjang proyeksi deret waktu murni secara lebih akurat.
