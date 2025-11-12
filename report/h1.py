import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from tqdm import tqdm 

# Đọc file dữ liệu
df_analysis = pd.read_csv('diem_thi_thpt_2025_new.csv')

# --- DANH SÁCH CÁC TỔ HỢP 3 MÔN (KEY) ---
combo_3_subjects = {
    'A00': ['Toán', 'Vật lí', 'Hóa học'],
    'A01': ['Toán', 'Vật lí', 'Tiếng Anh'],
    'A02': ['Toán', 'Vật lí', 'Sinh học'],
    'A03': ['Toán', 'Vật lí', 'Lịch sử'],
    'A04': ['Toán', 'Vật lí', 'Địa lí'],
    'A05': ['Toán', 'Hóa học', 'Lịch sử'],
    'A06': ['Toán', 'Hóa học', 'Địa lí'],
    'A07': ['Toán', 'Lịch sử', 'Địa lí'],
    'A08': ['Toán', 'Lịch sử', 'GDCD/KTPL'],
    'A09': ['Toán', 'Địa lí', 'GDCD/KTPL'],
    'A10': ['Toán', 'Vật lí', 'GDCD/KTPL'],
    'A11': ['Toán', 'Hóa học', 'GDCD/KTPL'],
    'B00': ['Toán', 'Hóa học', 'Sinh học'],
    'B02': ['Toán', 'Sinh học', 'Địa lí'],
    'B03': ['Toán', 'Sinh học', 'Ngữ văn'],
    'B04': ['Toán', 'Sinh học', 'GDCD/KTPL'],
    'B08': ['Toán', 'Sinh học', 'Tiếng Anh'],
    'C00': ['Ngữ văn', 'Lịch sử', 'Địa lí'],
    'C01': ['Ngữ văn', 'Toán', 'Vật lí'],
    'C02': ['Ngữ văn', 'Toán', 'Hóa học'],
    'C03': ['Ngữ văn', 'Toán', 'Lịch sử'],
    'C04': ['Ngữ văn', 'Toán', 'Địa lí'],
    'C05': ['Ngữ văn', 'Vật lí', 'Hóa học'],
    'C08': ['Ngữ văn', 'Hóa học', 'Sinh học'],
    'C12': ['Ngữ văn', 'Lịch sử', 'Sinh học'],
    'C13': ['Ngữ văn', 'Sinh học', 'Địa lí'],
    'C14': ['Ngữ văn', 'Toán', 'GDCD/KTPL'],
    'C17': ['Ngữ văn', 'Hóa học', 'GDCD/KTPL'],
    'C19': ['Ngữ văn', 'Lịch sử', 'GDCD/KTPL'],
    'C20': ['Ngữ văn', 'Địa lí', 'GDCD/KTPL'],
    'D01': ['Ngữ văn', 'Toán', 'Tiếng Anh'],
    'D07': ['Toán', 'Hóa học', 'Tiếng Anh'],
    'D08': ['Toán', 'Sinh học', 'Tiếng Anh'],
    'D09': ['Toán', 'Lịch sử', 'Tiếng Anh'],
    'D10': ['Toán', 'Địa lí', 'Tiếng Anh'],
    'D11': ['Ngữ văn', 'Vật lí', 'Tiếng Anh'],
    'D12': ['Ngữ văn', 'Hóa học', 'Tiếng Anh'],
    'D13': ['Ngữ văn', 'Sinh học', 'Tiếng Anh'],
    'D14': ['Ngữ văn', 'Lịch sử', 'Tiếng Anh'],
    'D15': ['Ngữ văn', 'Địa lí', 'Tiếng Anh'],
    'D66': ['Ngữ văn', 'GDCD/KTPL', 'Tiếng Anh'],
    'D84': ['Toán', 'Tiếng Anh', 'GDCD/KTPL']
}


# --- TÍNH TOÁN LẠI ĐIỂM TỔ HỢP 3 MÔN ---
print("Bắt đầu logic mới: Tính toán lại điểm cho từng tổ hợp 3 môn...")
combo_data_list = []

# Dùng tqdm để theo dõi tiến độ duyệt qua các tổ hợp
for combo_name, subjects in tqdm(combo_3_subjects.items(), desc="Xử lý điểm tổ hợp 3 môn"):
    # 1. Chọn các cột cần thiết: ID, Nhóm tuổi và các môn của tổ hợp
    required_cols = ['Số báo danh', 'Nhóm tuổi'] + subjects
    
    # 2. Lấy data, loại bỏ ngay các hàng thiếu bất kỳ môn nào trong tổ hợp
    valid_students_df = df_analysis[required_cols].dropna()
    
    # 3. Tính tổng điểm MỚI chỉ dựa trên 3 môn của tổ hợp
    valid_students_df['Điểm tổ hợp 3 môn'] = valid_students_df[subjects].sum(axis=1)
    
    # 4. Gán tên tổ hợp
    valid_students_df['Tổ hợp 3 môn'] = combo_name
    
    # 5. Chọn các cột cuối cùng để đưa vào list
    final_cols = ['Số báo danh', 'Nhóm tuổi', 'Tổ hợp 3 môn', 'Điểm tổ hợp 3 môn']
    combo_data_list.append(valid_students_df[final_cols])

# 6. Ghép tất cả lại thành một DataFrame "dài"
# DataFrame này sẽ có nhiều hàng cho cùng 1 SBD nếu SBD đó đủ điều kiện cho nhiều tổ hợp
df_combo_3_scores_long = pd.concat(combo_data_list, ignore_index=True)
print("Hoàn thành tính toán lại điểm tổ hợp 3 môn.")

# Danh sách 9 môn
subjects_9 = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 
              'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']

# Thống kê toàn quốc (thêm dữ liệu của bạn vào đây)
national_stats = {
    'Toán': {
        'Điểm trung bình (Mean)': 4.78,
        'Trung vị (Median)': 4.6,
        'Độ lệch chuẩn (Std)': 1.68,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.35,
        'Số thí sinh điểm <5': 635102,
        'Số thí sinh điểm <5 theo %': 56.395,
        'Số thí sinh điểm >=7': 137741,
        'Số thí sinh điểm >=7 theo %': 12.231,
        'Số thí sinh đạt điểm <=1': 777,
        'Số thí sinh đạt điểm <=1 theo %': 0.069,
        'Số thí sinh đạt điểm 10': 513,
        'Số thí sinh đạt điểm 0': 6,
        'Tỉ lệ điểm 10/1000 thí sinh': 0.4555,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 4.75
    },
    'Ngữ văn': {
        'Điểm trung bình (Mean)': 7.0,
        'Trung vị (Median)': 7.25,
        'Độ lệch chuẩn (Std)': 1.28,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.0,
        'Số thí sinh điểm <5': 70308,
        'Số thí sinh điểm <5 theo %': 6.24,
        'Số thí sinh điểm >=7': 671209,
        'Số thí sinh điểm >=7 theo %': 59.572,
        'Số thí sinh đạt điểm <=1': 87,
        'Số thí sinh đạt điểm <=1 theo %': 0.008,
        'Số thí sinh đạt điểm 10': 0,
        'Số thí sinh đạt điểm 0': 7,
        'Tỉ lệ điểm 10/1000 thí sinh': 0.0,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 7.5
    },
    'Tiếng Anh': {
        'Điểm trung bình (Mean)': 5.38,
        'Trung vị (Median)': 5.25,
        'Độ lệch chuẩn (Std)': 1.45,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.16,
        'Số thí sinh điểm <5': 134478,
        'Số thí sinh điểm <5 theo %': 38.22,
        'Số thí sinh điểm >=7': 53251,
        'Số thí sinh điểm >=7 theo %': 15.135,
        'Số thí sinh đạt điểm <=1': 28,
        'Số thí sinh đạt điểm <=1 theo %': 0.008,
        'Số thí sinh đạt điểm 10': 141,
        'Số thí sinh đạt điểm 0': 2,
        'Tỉ lệ điểm 10/1000 thí sinh': 0.4007,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 5.25
    },
    'Vật lí': {
        'Điểm trung bình (Mean)': 6.99,
        'Trung vị (Median)': 7.0,
        'Độ lệch chuẩn (Std)': 1.52,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.25,
        'Số thí sinh điểm <5': 34029,
        'Số thí sinh điểm <5 theo %': 9.79,
        'Số thí sinh điểm >=7': 186531,
        'Số thí sinh điểm >=7 theo %': 53.663,
        'Số thí sinh đạt điểm <=1': 3,
        'Số thí sinh đạt điểm <=1 theo %': 0.001,
        'Số thí sinh đạt điểm 10': 3929,
        'Số thí sinh đạt điểm 0': 1,
        'Tỉ lệ điểm 10/1000 thí sinh': 11.3033,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 7.5
    },
    'Hóa học': {
        'Điểm trung bình (Mean)': 6.06,
        'Trung vị (Median)': 6.0,
        'Độ lệch chuẩn (Std)': 1.81,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.51,
        'Số thí sinh điểm <5': 70910,
        'Số thí sinh điểm <5 theo %': 29.529,
        'Số thí sinh điểm >=7': 80847,
        'Số thí sinh điểm >=7 theo %': 33.667,
        'Số thí sinh đạt điểm <=1': 8,
        'Số thí sinh đạt điểm <=1 theo %': 0.003,
        'Số thí sinh đạt điểm 10': 625,
        'Số thí sinh đạt điểm 0': 0,
        'Tỉ lệ điểm 10/1000 thí sinh': 2.6027,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 6.25
    },
    'Sinh học': {
        'Điểm trung bình (Mean)': 5.78,
        'Trung vị (Median)': 5.75,
        'Độ lệch chuẩn (Std)': 1.58,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.3,
        'Số thí sinh điểm <5': 22674,
        'Số thí sinh điểm <5 theo %': 32.44,
        'Số thí sinh điểm >=7': 17579,
        'Số thí sinh điểm >=7 theo %': 25.151,
        'Số thí sinh đạt điểm <=1': 1,
        'Số thí sinh đạt điểm <=1 theo %': 0.001,
        'Số thí sinh đạt điểm 10': 82,
        'Số thí sinh đạt điểm 0': 0,
        'Tỉ lệ điểm 10/1000 thí sinh': 1.1732,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 6.5
    },
    'Lịch sử': {
        'Điểm trung bình (Mean)': 6.52,
        'Trung vị (Median)': 6.6,
        'Độ lệch chuẩn (Std)': 1.63,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.36,
        'Số thí sinh điểm <5': 89665,
        'Số thí sinh điểm <5 theo %': 18.63,
        'Số thí sinh điểm >=7': 210702,
        'Số thí sinh điểm >=7 theo %': 43.778,
        'Số thí sinh đạt điểm <=1': 13,
        'Số thí sinh đạt điểm <=1 theo %': 0.003,
        'Số thí sinh đạt điểm 10': 1518,
        'Số thí sinh đạt điểm 0': 2,
        'Tỉ lệ điểm 10/1000 thí sinh': 3.154,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 7.25
    },
    'Địa lí': {
        'Điểm trung bình (Mean)': 6.63,
        'Trung vị (Median)': 6.75,
        'Độ lệch chuẩn (Std)': 1.75,
        'Độ lệch tuyệt đối trung vị (MAD)': 1.45,
        'Số thí sinh điểm <5': 89054,
        'Số thí sinh điểm <5 theo %': 18.69,
        'Số thí sinh điểm >=7': 215695,
        'Số thí sinh điểm >=7 theo %': 45.269,
        'Số thí sinh đạt điểm <=1': 19,
        'Số thí sinh đạt điểm <=1 theo %': 0.004,
        'Số thí sinh đạt điểm 10': 6907,
        'Số thí sinh đạt điểm 0': 3,
        'Tỉ lệ điểm 10/1000 thí sinh': 14.4961,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 7.75
    },
    'GDCD/KTPL': {
        'Điểm trung bình (Mean)': 7.69,
        'Trung vị (Median)': 7.75,
        'Độ lệch chuẩn (Std)': 1.18,
        'Độ lệch tuyệt đối trung vị (MAD)': 0.92,
        'Số thí sinh điểm <5': 6324,
        'Số thí sinh điểm <5 theo %': 2.567,
        'Số thí sinh điểm >=7': 192613,
        'Số thí sinh điểm >=7 theo %': 78.171,
        'Số thí sinh đạt điểm <=1': 0,
        'Số thí sinh đạt điểm <=1 theo %': 0.0,
        'Số thí sinh đạt điểm 10': 1451,
        'Số thí sinh đạt điểm 0': 0,
        'Tỉ lệ điểm 10/1000 thí sinh': 5.8888,
        'Điểm nhiều thí sinh đạt được nhất (Mode)': 8.25
    }
}

# Hàm tính MAD - Median Absolute Deviation
def mad(series):
    return np.median(np.abs(series - np.median(series)))

# Hàm so sánh chỉ số
def compare_stats(local_val, national_val):
    if pd.isna(local_val) or pd.isna(national_val):
        return "N/A"
    diff = local_val - national_val
    return round(diff, 2)

# Hàm tính tỉ lệ phần trăm so với toàn quốc
def percentage_ratio(local_val, national_val):
    if pd.isna(local_val) or pd.isna(national_val) or national_val == 0:
        return "N/A"
    return round((local_val / national_val) * 100, 2)

# Tạo dataframe tổng hợp
statistics_summary_full = pd.DataFrame()

# <-- TÍNH TOÁN THỐNG KÊ (1/5)
for subject in tqdm(subjects_9, desc="1/5: Tính toán thống kê môn học"):
    data = df_analysis[subject].dropna()
    n_total = len(data)
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()
    mad_val = mad(data)
    count_below_5 = (data < 5).sum()
    count_above_eq_7 = (data >= 7).sum()
    
    mode_val = data.mode()
    mode_val = mode_val[0] if not mode_val.empty else np.nan
    
    count_10 = (data == 10).sum()
    count_0 = (data == 0).sum()
    count_leq_1 = (data <= 1).sum()
    
    rate_10_per_1000 = count_10 / n_total * 1000 if n_total > 0 else np.nan
    
    # Lấy thống kê toàn quốc
    nat_stats = national_stats.get(subject, {})

    subject_stats = { 
        'Môn học': subject,
        'Tổng số thí sinh': n_total,
        'Điểm trung bình (Mean)': round(mean_val, 2),
        'Điểm trung bình Toàn quốc': nat_stats.get('Điểm trung bình (Mean)', 'N/A'),
        'Chênh lệch điểm trung bình': compare_stats(round(mean_val, 2), nat_stats.get('Điểm trung bình (Mean)', np.nan)),
        'Trung vị (Median)': round(median_val, 2),
        'Trung vị Toàn quốc': nat_stats.get('Trung vị (Median)', 'N/A'),
        'Chênh lệch Trung vị': compare_stats(round(median_val, 2), nat_stats.get('Trung vị (Median)', np.nan)),
        'Độ lệch chuẩn (Std)': round(std_val, 2),
        'Độ lệch chuẩn Toàn quốc': nat_stats.get('Độ lệch chuẩn (Std)', 'N/A'),
        'Chênh lệch Độ lệch chuẩn': compare_stats(round(std_val, 2), nat_stats.get('Độ lệch chuẩn (Std)', np.nan)),
        'Độ lệch tuyệt đối trung vị (MAD)': round(mad_val, 2),
        'Độ lệch tuyệt đối trung vị (MAD) Toàn quốc': nat_stats.get('Độ lệch tuyệt đối trung vị (MAD)', 'N/A'),
        'Chênh lệch Độ lệch tuyệt đối trung vị (MAD)': compare_stats(round(mad_val, 2), nat_stats.get('Độ lệch tuyệt đối trung vị (MAD)', np.nan)),
        'Số thí sinh điểm <5': count_below_5,
        'Số thí sinh điểm <5 Toàn quốc': nat_stats.get('Số thí sinh điểm <5', 'N/A'),
        'Tỉ lệ Số thí sinh điểm <5 so với toàn quốc (%)': percentage_ratio(count_below_5, nat_stats.get('Số thí sinh điểm <5', np.nan)),
        'Số thí sinh điểm <5 theo %': round((count_below_5 / n_total * 100),3) if n_total > 0 else np.nan,
        'Số thí sinh điểm <5 theo % Toàn quốc': nat_stats.get('Số thí sinh điểm <5 theo %', 'N/A'),
        'Chênh lệch Số thí sinh điểm <5 theo %': compare_stats(round((count_below_5 / n_total * 100),3) if n_total > 0 else np.nan, nat_stats.get('Số thí sinh điểm <5 theo %', np.nan)),
        'Số thí sinh điểm >=7': count_above_eq_7,
        'Số thí sinh điểm >=7 Toàn quốc': nat_stats.get('Số thí sinh điểm >=7', 'N/A'),
        'Tỉ lệ Số thí sinh điểm >=7 so với toàn quốc (%)': percentage_ratio(count_above_eq_7, nat_stats.get('Số thí sinh điểm >=7', np.nan)),
        'Số thí sinh điểm >=7 theo %': round((count_above_eq_7 / n_total * 100),3) if n_total > 0 else np.nan,
        'Số thí sinh điểm >=7 theo % Toàn quốc': nat_stats.get('Số thí sinh điểm >=7 theo %', 'N/A'),
        'Chênh lệch Số thí sinh điểm >=7 theo %': compare_stats(round((count_above_eq_7 / n_total * 100),3) if n_total > 0 else np.nan, nat_stats.get('Số thí sinh điểm >=7 theo %', np.nan)),
        'Điểm nhiều thí sinh đạt được nhất (Mode)': mode_val,
        'Điểm nhiều thí sinh đạt được nhiều nhất (Mode) Toàn quốc': nat_stats.get('Điểm nhiều thí sinh đạt được nhất (Mode)', 'N/A'),
        'Chênh lệch Điểm nhiều thí sinh đạt được nhất (Mode)': compare_stats(mode_val, nat_stats.get('Điểm nhiều thí sinh đạt được nhất (Mode)', np.nan)),
        'Số thí sinh đạt điểm 10': count_10,
        'Số thí sinh đạt điểm 10 Toàn quốc': nat_stats.get('Số thí sinh đạt điểm 10', 'N/A'),
        'Tỉ lệ Số thí sinh đạt điểm 10 so với toàn quốc (%)': percentage_ratio(count_10, nat_stats.get('Số thí sinh đạt điểm 10', np.nan)),
        'Số thí sinh đạt điểm 0': count_0,
        'Số thí sinh đạt điểm 0 Toàn quốc': nat_stats.get('Số thí sinh đạt điểm 0', 'N/A'),
        'Tỉ lệ Số thí sinh đạt điểm 0 so với toàn quốc (%)': percentage_ratio(count_0, nat_stats.get('Số thí sinh đạt điểm 0', np.nan)),
        'Số thí sinh đạt điểm <=1': count_leq_1,
        'Số thí sinh đạt điểm <=1 Toàn quốc': nat_stats.get('Số thí sinh đạt điểm <=1', 'N/A'),
        'Chênh lệch Số thí sinh đạt điểm <=1': compare_stats(count_leq_1, nat_stats.get('Số thí sinh đạt điểm <=1', np.nan)),
        'Số thí sinh đạt điểm <=1 theo %': round((count_leq_1 / n_total * 100),3) if n_total > 0 else np.nan,
        'Số thí sinh đạt điểm <=1 theo % Toàn quốc': nat_stats.get('Số thí sinh đạt điểm <=1 theo %', 'N/A'),
        'Chênh lệch Số thí sinh đạt điểm <=1 theo %': compare_stats(round((count_leq_1 / n_total * 100),3) if n_total > 0 else np.nan, nat_stats.get('Số thí sinh đạt điểm <=1 theo %', np.nan)),
        'Tỉ lệ điểm 10/1000 thí sinh': round(rate_10_per_1000, 4) if not pd.isna(rate_10_per_1000) else np.nan,
        'Tỉ lệ điểm 10/1000 thí sinh Toàn quốc': nat_stats.get('Tỉ lệ điểm 10/1000 thí sinh', 'N/A'),
        'Chênh lệch Tỉ lệ điểm 10/1000 thí sinh': compare_stats(round(rate_10_per_1000, 4) if not pd.isna(rate_10_per_1000) else np.nan, nat_stats.get('Tỉ lệ điểm 10/1000 thí sinh', np.nan))
    }
    
    statistics_summary_full = pd.concat([statistics_summary_full, pd.DataFrame([subject_stats])], ignore_index=True)

lines = []

# Ghi kết quả thống kê vào danh sách
lines.append(statistics_summary_full.to_string(index=False))

# Vẽ BIỂU ĐỒ
# Histogram và KDE cho các môn chính
fig, axes = plt.subplots(5, 2, figsize=(15, 20))
axes = axes.flatten()
subjects_all = subjects_9 + ['Tổng điểm']

# Vẽ biểu đồ phân bố (Histogram)
for idx, subject in enumerate(tqdm(subjects_all, desc="2/5: Vẽ biểu đồ phân bố (Histogram)")):
    ax = axes[idx]
    
    # XỬ LÝ RIÊNG CHO TỔNG ĐIỂM
    if subject == 'Tổng điểm':
        # Tổng điểm có thể từ 0 đến ~90, nên dùng bins khác
        bins_to_use = np.arange(0, df_analysis[subject].max() + 2, 1)  # Chia theo đơn vị 1 điểm
        xticks_to_use = np.arange(0, df_analysis[subject].max() + 5, 5)  # Hiển thị mỗi 5 điểm
    else:
        # Các môn đơn từ 0-10
        bins_to_use = np.arange(0, 10.25, 0.25)
        xticks_to_use = np.arange(0, 10.5, 0.5)
    
    # Vẽ histogram
    sns.histplot(data=df_analysis, x=subject, kde=True, ax=ax, 
                 bins=bins_to_use, color='skyblue', edgecolor='black')
    
    ax.set_title(f'Phân bố điểm {subject}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Điểm số', fontsize=12)
    ax.set_ylabel('Số lượng thí sinh', fontsize=12)
    
    # Đặt ticks
    ax.set_xticks(xticks_to_use)
    
    # ĐẢM BẢO TRỤC Y HIỂN THỊ ĐẦY ĐỦ
    ax.set_ylim(bottom=0)  # Bắt đầu từ 0
    # Tự động scale theo dữ liệu thực tế
    
    # Thêm đường trung bình và trung vị
    try:
        mean_val = df_analysis[subject].mean()
        median_val = df_analysis[subject].median()
        ax.axvline(mean_val, color='red', 
                   linestyle='--', linewidth=2, label=f'Trung bình: {mean_val:.2f}')
        ax.axvline(median_val, color='green', 
                   linestyle='--', linewidth=2, label=f'Trung vị: {median_val:.2f}')
        ax.legend()
    except:
        pass

plt.tight_layout()
plt.savefig('h1_phan_bo_diem_cac_mon.png', dpi=300, bbox_inches='tight')
print("Đã lưu: h1_phan_bo_diem_cac_mon.png")

# Boxplot duy nhất cho Tổng điểm theo nhóm tuổi
# Vẽ 5x2 = 10 boxplot cho 9 môn + Tổng điểm
fig, axes = plt.subplots(5, 2, figsize=(16, 20))
axes = axes.flatten()

# <-- BOXPLOT NHÓM TUỔI (3/5)
for idx, subject in enumerate(tqdm(subjects_all, desc="3/5: Vẽ biểu đồ Boxplot (Nhóm tuổi)")):
    ax = axes[idx]
    sns.boxplot(data=df_analysis, x='Nhóm tuổi', y=subject, ax=ax, palette='Set3', hue='Nhóm tuổi', legend=False)
    ax.set_title(f'Phân bố {subject} theo Nhóm tuổi', fontsize=12, fontweight='bold')
    ax.set_ylabel(subject, fontsize=10)
    ax.set_xlabel('Nhóm tuổi', fontsize=10)

plt.tight_layout()
plt.savefig('h1_boxplot_by_age_group_all_subjects.png', dpi=300, bbox_inches='tight')

# ---Boxplot Tổ hợp 3 môn ---
# Sắp xếp các tổ hợp 3 môn theo thứ tự alphabet để biểu đồ dễ nhìn hơn
sorted_combos = sorted(df_combo_3_scores_long['Tổ hợp 3 môn'].unique())

print("Đang vẽ Boxplot theo tổ hợp 3 môn (dùng điểm 3 môn)...")
plt.figure(figsize=(20, 12)) # Kích thước lớn hơn để chứa nhiều tổ hợp
# SỬ DỤNG df_combo_3_scores_long và y='Điểm tổ hợp 3 môn'
sns.boxplot(data=df_combo_3_scores_long, x='Tổ hợp 3 môn', y='Điểm tổ hợp 3 môn', 
            palette='Set3', hue='Tổ hợp 3 môn', legend=False, order=sorted_combos)
plt.title('Phân bố ĐIỂM TỔ HỢP 3 MÔN theo Tổ hợp', fontsize=16, fontweight='bold')
plt.xlabel('Tổ hợp 3 môn', fontsize=12)
plt.ylabel('Điểm tổ hợp 3 môn', fontsize=12) # Ghi rõ
plt.xticks(rotation=90) # Xoay nhãn trục X
plt.tight_layout()
plt.savefig('h1_boxplot_by_combo_3_subjects.png', dpi=300, bbox_inches='tight')

# KIỂM ĐỊNH THỐNG KÊ
lines.append("\n===== KIỂM ĐỊNH THỐNG KÊ =====\n")

# ANOVA: So sánh điểm giữa các nhóm tuổi (DÙNG TỔNG ĐIỂM GỐC)
age_groups = [group['Tổng điểm'].dropna() for name, group in df_analysis.groupby('Nhóm tuổi')]
f_stat, p_value_anova = stats.f_oneway(*age_groups)
lines.append("2. ANOVA: So sánh TỔNG ĐIỂM (gốc) giữa các nhóm tuổi")
lines.append(f"   F-statistic: {f_stat:.4f}, p-value: {p_value_anova:.6g}")
lines.append(f"   Kết luận: {'Có' if p_value_anova < 0.05 else 'Không có'} sự khác biệt có ý nghĩa thống kê (α=0.05)\n")


# --- CẬP NHẬT (ANOVA Tổ hợp 3 môn) ---
lines.append("\n3. ANOVA: So sánh ĐIỂM TỔ HỢP 3 MÔN (tính lại) giữa các TỔ HỢP")
# Tạo danh sách các nhóm điểm (Series) cho mỗi tổ hợp 3 môn
# SỬ DỤNG df_combo_3_scores_long và cột 'Điểm tổ hợp 3 môn'
combo_groups = [group['Điểm tổ hợp 3 môn'].dropna() 
                for name, group in df_combo_3_scores_long.groupby('Tổ hợp 3 môn')]

# Chỉ chạy ANOVA nếu có 2 nhóm trở lên
if len(combo_groups) > 1:
    f_stat_combo, p_value_combo_anova = stats.f_oneway(*combo_groups)
    lines.append(f"   F-statistic: {f_stat_combo:.4f}, p-value: {p_value_combo_anova:.6g}")
    lines.append(f"   Kết luận: {'Có' if p_value_combo_anova < 0.05 else 'Không có'} sự khác biệt có ý nghĩa thống kê về Điểm tổ hợp 3 môn giữa các tổ hợp (α=0.05)\n")
else:
    lines.append("   Không đủ số lượng nhóm tổ hợp (cần ít nhất 2) để thực hiện ANOVA.\n")

# Kolmogorov-Smirnov test: Kiểm tra phân phối chuẩn
# <-- KIỂM ĐỊNH K-S (4/5)
for subject in tqdm(subjects_all, desc="4/5: Chạy kiểm định K-S"):
    # Thêm try-except
    try:
        data_ks = df_analysis[subject].dropna()
        if not data_ks.empty:
            ks_stat, ks_pvalue = stats.kstest(data_ks, 'norm')
            lines.append(f"4. K-S test: Kiểm tra phân phối chuẩn cho môn {subject}")
            lines.append(f"   KS-statistic: {ks_stat:.4f}, p-value: {ks_pvalue:.6g}")
            lines.append(f"   Kết luận: Dữ liệu {'KHÔNG' if ks_pvalue < 0.05 else ''} tuân theo phân phối chuẩn\n")
        else:
            lines.append(f"4. K-S test: Không có dữ liệu cho môn {subject} để kiểm định.\n")
    except Exception as e:
        lines.append(f"4. K-S test: Lỗi khi kiểm định môn {subject}: {e}\n")


lines.append("\n===== PHÂN TÍCH LỢI THẾ ĐÔ THỊ (URBAN ADVANTAGE) =====\n")

# PHÂN TÍCH LỢI THẾ ĐÔ THỊ (5/5)
for subject in tqdm(subjects_9, desc="5/5: Phân tích Lợi thế đô thị"):
    tphcm_mean = statistics_summary_full[statistics_summary_full['Môn học'] == subject]['Điểm trung bình (Mean)'].values[0]
    national_mean = national_stats.get(subject, {}).get('Điểm trung bình (Mean)', np.nan)
    
    if not np.isnan(national_mean):
        advantage = tphcm_mean - national_mean
        percentage_advantage = (advantage / national_mean * 100) if national_mean != 0 else 0
        
        lines.append(f"{subject}:")
        lines.append(f"   TPHCM: {tphcm_mean:.2f}")
        lines.append(f"   Toàn quốc: {national_mean:.2f}")
        lines.append(f"   Lợi thế đô thị: +{advantage:.2f} ({percentage_advantage:+.2f}%)\n")

# PHÂN TÍCH DỰA TRÊN CHUỖI TỔ HỢP GỐC
lines.append("\n===== PHÂN TÍCH THEO TỔ HỢP MÔN TỰ CHỌN (GỐC) =====\n") 
combo_stats = df_analysis.groupby('Tổ hợp tự chọn').agg({
    'Tổng điểm': ['mean', 'std', 'count'] # Dùng TỔNG ĐIỂM GỐC
}).round(2)

lines.append("Nhằm trả lời 2 câu hỏi: 1. Thí sinh chọn Tổ hợp (chuỗi gốc) nào nhiều nhất? 2. Tổ hợp (chuỗi gốc) nào có điểm trung bình (gốc) cao nhất?")
lines.append("Thống kê tổ hợp môn (sắp xếp theo số thí sinh):")
lines.append(str(combo_stats.sort_values(('Tổng điểm', 'count'), ascending=False)))


# --- Thống kê tổ hợp 3 môn ---
lines.append("\n===== PHÂN TÍCH THEO TỔ HỢP 3 MÔN (ĐIỂM TÍNH LẠI) =====\n")

# SỬ DỤNG df_combo_3_scores_long và 'Điểm tổ hợp 3 môn'
combo_3_stats = df_combo_3_scores_long.groupby('Tổ hợp 3 môn').agg(
    # Đổi tên cột agg để rõ ràng
    Điểm_TB_3_môn=('Điểm tổ hợp 3 môn', 'mean'),
    Độ_lệch_chuẩn_3_môn=('Điểm tổ hợp 3 môn', 'std'),
    Số_lượng=('Điểm tổ hợp 3 môn', 'count')
).round(2)

lines.append("Thống kê cho từng tổ hợp 3 môn (sắp xếp theo số thí sinh):")
lines.append(str(combo_3_stats.sort_values('Số_lượng', ascending=False)))

lines.append("\nThống kê cho từng tổ hợp 3 môn (sắp xếp theo điểm trung bình 3 môn):")
lines.append(str(combo_3_stats.sort_values('Điểm_TB_3_môn', ascending=False)))

# Ghi lại toàn bộ kết quả ra file
print("\nĐang ghi kết quả ra file h1.txt...")
with open('h1.txt', 'w', encoding='utf-8-sig') as f:
    for line in lines:
        f.write(line + '\n')

print("\nHoàn thành! Kết quả đã được lưu vào h1.txt")