# THPT 2025 HCMC Score Analysis

## 🌐 Report Website

Truy cập trang web xem báo cáo trực quan và đầy đủ tại đây (Access the website to explore the comprehensive and visual report here):

👉 **https://data-mining-thptqg-2025.vercel.app/**  

<p align="center">
  <a href="#vi"><b>🇻🇳 Tiếng Việt</b></a> •
  <a href="#en"><b>🇬🇧 English</b></a>
</p>

---

<a id="vi"></a>

## 🇻🇳 Tổng quan (Tiếng Việt)

Dự án phân tích dữ liệu điểm thi THPT Quốc gia năm 2025 của 129,148 thí sinh tại TP. Hồ Chí Minh, dựa trên bộ thống kê chính thức của Bộ GD&ĐT và báo cáo học thuật chi tiết được soạn thảo bằng LaTeX trong thư mục `report/`.

Mục tiêu chính:

- Đo lường **lợi thế đô thị** (urban advantage) của TP.HCM so với mặt bằng cả nước  
- Khai phá **xu hướng học tập** (thiên Văn / thiên Toán / cân bằng) và xây dựng mô hình **dự báo tổng điểm** bằng Random Forest & Gradient Boosting  
- Kiểm chứng **Hiệu ứng tuổi tương đối (Relative Age Effect)** theo quý sinh  
- Khám phá mối liên hệ (mang tính vui vẻ) giữa **cung hoàng đạo** và kết quả thi  

---

### 🧭 Cấu trúc repository

```text
.
├── report/
│   ├── *.tex                     # Source LaTeX của báo cáo chính
│   ├── report.pdf                # Bản PDF final report
│   ├── bao-cao-15-7-2025-...pdf  # File PDF thống kê gốc của Bộ GD&ĐT
│   ├── Methodology.md            # Mô tả chi tiết phương pháp & pipeline
│   ├── diem_thi_thpt_2025.csv    # Dữ liệu gốc (đã ẩn danh)
│   ├── diem_thi_thpt_2025_new.csv# Dữ liệu sau cleaning & feature engineering
│   ├── data_cleaning.py          # Làm sạch dữ liệu
│   ├── feature_engineering.py    # Làm giàu dữ liệu (feature engineering)
│   ├── encryption.py             # Mã hóa số báo danh & họ tên
│   ├── h1.py ... h4.py           # Code cho 4 hướng nghiên cứu
│   ├── h1.txt ... h4.txt         # Kết quả thống kê/summary tương ứng
│   └── h[1-4]_*.png              # Hình minh họa/diagram cho từng hướng
└── website/
    └── ...                       # Mã nguồn website demo (report viewer / dashboard)
````

---

### 🎯 Các hướng nghiên cứu

Bám sát báo cáo học thuật, thư mục `report/` hiện thực 4 hướng phân tích chính:

1. **Hướng 1 – Phổ điểm & Lợi thế đô thị**

   * Thống kê mô tả, so sánh TP.HCM với toàn quốc
   * ANOVA theo nhóm tuổi & tổ hợp ba môn
   * Kiểm định phân phối (Kolmogorov–Smirnov)

2. **Hướng 2 – Xu hướng học & mô hình dự báo**

   * Phân loại thí sinh: *Thiên Văn – Thiên Toán – Cân bằng* bằng Cohen’s d
   * Phân tích tương quan giữa 9 môn thi
   * Xây dựng mô hình dự báo tổng điểm (Linear Regression, Random Forest, Gradient Boosting)
   * Giải thích mô hình bằng **SHAP** (Explainable AI)

3. **Hướng 3 – Hiệu ứng tuổi tương đối (RAE)**

   * Chia thí sinh theo **quý sinh (Q1–Q4)**
   * ANOVA kiểm tra sự khác biệt tổng điểm & từng môn giữa các quý

4. **Hướng 4 – Cung hoàng đạo & kết quả thi**

   * Gán cung hoàng đạo từ ngày sinh
   * So sánh điểm thi giữa 12 cung, mang tính khám phá & đối chiếu với niềm tin chiêm tinh

Chi tiết phương pháp, công thức và tất cả bảng số liệu đều được trình bày trong `report/report.pdf` và các file `h1.txt`–`h4.txt`.

---

### 🧪 Cách chạy code & tái lập kết quả

> Yêu cầu: Python 3.10+ và các thư viện phổ biến như `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `shap`…

1. **Tạo & kích hoạt môi trường ảo (khuyến nghị)**

```bash
python -m venv .venv
source .venv/bin/activate  # hoặc .venv\Scripts\activate trên Windows
pip install -r requirements.txt  # nếu repo có sẵn
```

2. **Làm sạch & chuẩn hóa dữ liệu**

```bash
cd report
python data_cleaning.py
```

* Input: `diem_thi_thpt_2025.csv`
* Output: file đã xử lý trung gian (nếu có) và/hoặc ghi đè vào `diem_thi_thpt_2025_new.csv`

3. **Làm giàu dữ liệu (Feature Engineering)**

```bash
python feature_engineering.py
```

* Thêm các cột: nhóm tuổi, quý sinh, tổ hợp môn, chênh lệch Văn–Toán, cung hoàng đạo, v.v.

4. **Chạy từng hướng phân tích**

```bash
# Hướng 1 – Phổ điểm & urban advantage
python h1.py

# Hướng 2 – Xu hướng học & mô hình dự báo
python h2.py

# Hướng 3 – Relative Age Effect
python h3.py

# Hướng 4 – Zodiac & điểm thi
python h4.py
```

Mỗi script sẽ:

* Sinh các bảng thống kê & biểu đồ `.png` (đặt tên theo cú pháp `h[hướng]_[tên diagram].png`, ví dụ `h1_boxplot_by_combo_3_subjects.png`)
* Ghi summary kết quả vào `h1.txt`–`h4.txt`

5. **Xem báo cáo**

* Mở `report/report.pdf` để xem full báo cáo học thuật
* Hoặc truy cập thư mục `website/` và chạy web demo (tùy framework, ví dụ nếu là static):

```bash
cd ../website
# nếu là app đơn giản dùng e.g. npm, streamlit... thì mô tả thêm ở đây
```

---

### 🔐 Dữ liệu & bảo mật

* Hai file CSV trong repo **đều đã được ẩn danh**:

  * `diem_thi_thpt_2025.csv`: dữ liệu gốc (đã mã hóa số báo danh & họ tên)
  * `diem_thi_thpt_2025_new.csv`: dữ liệu sau khi làm sạch & thêm đặc trưng
* File `encryption.py` mô tả quy trình mã hóa giúp:

  * Bảo vệ danh tính thí sinh
  * Cho phép tái lập pipeline mà không truy cập trực tiếp dữ liệu nhạy cảm

🔎 Nếu bạn **thật sự cần truy cập file gốc không mã hóa** (ví dụ cho mục đích kiểm chứng khoa học hoặc đối chiếu với nguồn Bộ GD&ĐT):

> Vui lòng gửi email đến: **[khangvh.work@gmail.com](mailto:khangvh.work@gmail.com)**
> – Nêu rõ:
>
> * Bạn là ai
> * Bạn đang làm nghiên cứu / dự án gì
> * Tại sao cần truy cập dữ liệu gốc
> * Cam kết tuân thủ quy định bảo mật & đạo đức sử dụng dữ liệu

Quyền truy cập không được đảm bảo và sẽ tùy thuộc vào xét duyệt thủ công.

---

### 🧑‍💻 Công nghệ & thư viện chính

* **Ngôn ngữ:** Python
* **Phân tích & xử lý dữ liệu:** `pandas`, `numpy`, `scipy`
* **Thống kê & kiểm định:** ANOVA, t-test, KS-test, Cohen’s d
* **Machine Learning:** `scikit-learn` (Linear Regression, Random Forest, Gradient Boosting, K-Fold CV)
* **Giải thích mô hình:** `shap` (SHAP values, summary & beeswarm plots)
* **Trực quan hóa:** `matplotlib`, `seaborn`
* **Báo cáo:** LaTeX (`.tex` + `report.pdf`), `Methodology.md`

---

### 👥 Thực hiện

* Võ Hữu Khang – Sinh viên ngành Khoa học Máy tính tại Trường Đại học Bách khoa – Đại học Quốc gia TP. Hồ Chí Minh

Liên hệ nhóm (học thuật): `khang.vohuu@hcmut.edu.vn`

---

[⬆ Quay lại đầu trang](#thpt-2025-hcmc-score-analysis) • [🇬🇧 Xem bản tiếng Anh](#en)

---

<a id="en"></a>

## 🇬🇧 Overview (English)

This project analyzes the **2025 Vietnamese National High School Graduation Exam** scores for **129,148 candidates in Ho Chi Minh City**, using the official statistics released by the Ministry of Education and Training and a detailed LaTeX report in the `report/` folder.

Main goals:

* Quantify the **urban advantage** of HCMC compared to the national distribution
* Discover **study patterns** (literature-leaning vs math-leaning vs balanced) and build **predictive models** for total scores
* Test the **Relative Age Effect** by birth quarter
* Explore (for fun) the relationship between **zodiac signs** and exam performance

---

### 🧭 Repository structure

```text
.
├── report/
│   ├── *.tex                     # LaTeX sources of the main report
│   ├── report.pdf                # Final PDF report
│   ├── bao-cao-15-7-2025-...pdf  # Official national statistics from MOET
│   ├── Methodology.md            # Detailed methodology & data pipeline
│   ├── diem_thi_thpt_2025.csv    # Original (anonymized) dataset
│   ├── diem_thi_thpt_2025_new.csv# Cleaned & feature-engineered dataset
│   ├── data_cleaning.py          # Data cleaning
│   ├── feature_engineering.py    # Feature engineering
│   ├── encryption.py             # ID / name encryption utilities
│   ├── h1.py ... h4.py           # 4 research directions
│   ├── h1.txt ... h4.txt         # Text summaries of each direction
│   └── h[1-4]_*.png              # Plots/diagrams, e.g. h1_boxplot_by_combo_3_subjects.png
└── website/
    └── ...                       # Demo website / dashboard source
```

---

### 🎯 Research directions

1. **Direction 1 – Score distributions & urban advantage**

   * Descriptive statistics comparing HCMC vs nationwide
   * One-way ANOVA by age group and by 3-subject combinations
   * Normality checks (Kolmogorov–Smirnov tests)

2. **Direction 2 – Study patterns & predictive modeling**

   * Classify students as *Math-leaning / Literature-leaning / Balanced* using Cohen’s d
   * Pearson correlation matrix across 9 subjects
   * Train total-score predictors (Linear Regression, Random Forest, Gradient Boosting)
   * Explain models with **SHAP** (global & local explanations)

3. **Direction 3 – Relative Age Effect (RAE)**

   * Group candidates by **birth quarter (Q1–Q4)**
   * One-way ANOVA on total score & per-subject scores across quarters

4. **Direction 4 – Zodiac vs exam performance (exploratory)**

   * Map date of birth to zodiac sign
   * Compare scores across 12 signs (purely exploratory, non-causal)

For full methodology, equations and detailed tables, see `report/report.pdf` and the `h1.txt`–`h4.txt` summaries.

---

### 🧪 How to run & reproduce

> Requirements: Python 3.10+ and common data science libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `shap`, …).

1. **Create & activate a virtual environment (recommended)**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. **Data cleaning**

```bash
cd report
python data_cleaning.py
```

* Input: `diem_thi_thpt_2025.csv`
* Output: cleaned intermediate files and/or updates to `diem_thi_thpt_2025_new.csv`

3. **Feature engineering**

```bash
python feature_engineering.py
```

* Adds age group, birth quarter, subject combination, literature–math gap, zodiac sign, etc.

4. **Run the four analysis directions**

```bash
python h1.py  # Direction 1 – distributions & urban advantage
python h2.py  # Direction 2 – study patterns & ML models
python h3.py  # Direction 3 – Relative Age Effect
python h4.py  # Direction 4 – Zodiac analysis
```

Each script will:

* Generate figures as `.png` (named `h[h]_...png`, e.g. `h2_shap_summary.png`)
* Save textual summaries into `h1.txt`–`h4.txt`

5. **Read the report**

* Open `report/report.pdf` for the full academic write-up
* Or go to `website/` to run the demo site (framework-specific commands go here, e.g. `npm run dev`, `streamlit run app.py`, etc.)

---

### 🔐 Data & privacy

* Both CSVs in this repository are **already anonymized**:

  * `diem_thi_thpt_2025.csv`: original score data with encrypted candidate ID & full name
  * `diem_thi_thpt_2025_new.csv`: cleaned + feature-engineered version
* `encryption.py` documents the anonymization logic to:

  * Protect student identities
  * Allow reproducible analysis without exposing sensitive information

🔎 If you **truly need access to the non-anonymized original file** (e.g. for official validation or collaboration with MOET):

> Please email **[khangvh.work@gmail.com](mailto:khangvh.work@gmail.com)** with:
>
> * Who you are
> * What research/project you are doing
> * Why you need the raw data
> * A clear commitment to ethical and secure data usage

Access is not guaranteed and will be reviewed on a case-by-case basis.

---

### 🧑‍💻 Tech stack

* **Language:** Python
* **Data wrangling:** `pandas`, `numpy`
* **Statistics:** ANOVA, t-tests, KS tests, Cohen’s d
* **Machine learning:** `scikit-learn` (Linear Regression, Random Forest, Gradient Boosting, K-Fold CV)
* **Explainability:** `shap` (SHAP values, summary & beeswarm plots)
* **Visualization:** `matplotlib`, `seaborn`
* **Reporting:** LaTeX (`.tex` + `report.pdf`), Markdown (`Methodology.md`)

---

### 👥 Author

* Võ Hữu Khang – Computer Science student at Ho Chi Minh City University of Technology (HCMUT) – Vietnam National University Ho Chi Minh City (VNU-HCM)

Academic contact: `khang.vohuu@hcmut.edu.vn`

---

[⬆ Back to top](#thpt-2025-hcmc-score-analysis) • [🇻🇳 Vietnamese version](#vi)

```
```
