import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

csv_path = 'diem_thi_thpt_2025_new.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")
df_analysis = pd.read_csv(csv_path)

lines = []

lines.append("===== PHÂN TÍCH KHÁM PHÁ: CUNG HOÀNG ĐẠO VÀ KẾT QUẢ THI =====\n")

# Danh sách 9 môn
subjects_9 = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 
              'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']

# Thống kê theo cung hoàng đạo
zodiac_stats = df_analysis.groupby('Cung Hoàng Đạo').agg({
    'Tổng điểm': ['mean', 'std', 'count'],
    'Toán': 'mean',
    'Ngữ văn': 'mean',
    'Tiếng Anh': 'mean',
    'Vật lí': 'mean',
    'Hóa học': 'mean',
    'Sinh học': 'mean',
    'Lịch sử': 'mean',
    'Địa lí': 'mean',
    'GDCD/KTPL': 'mean'
}).round(2)

lines.append("Thống kê điểm theo Cung Hoàng Đạo:")
lines.append(str(zodiac_stats.sort_values(('Tổng điểm', 'mean'), ascending=False)))
lines.append("")

# ANOVA test
zodiacs = [df_analysis[df_analysis['Cung Hoàng Đạo'] == z]['Tổng điểm'].dropna() 
           for z in df_analysis['Cung Hoàng Đạo'].unique() 
           if z != 'Không xác định']
f_stat_zodiac, p_value_zodiac = stats.f_oneway(*zodiacs)

lines.append("ANOVA Test - So sánh điểm tổng giữa 12 cung hoàng đạo:")
lines.append(f"   F-statistic: {f_stat_zodiac:.4f}")
lines.append(f"   p-value: {p_value_zodiac:.6f}")
lines.append(
    f"   Kết luận: Với p-value = {p_value_zodiac:.4f}, "
    f"{'có' if p_value_zodiac < 0.05 else 'không có'} bằng chứng đủ mạnh để khẳng định sự khác biệt có ý nghĩa thống kê giữa các nhóm."
)


# Tạo dictionary để lưu điểm cao nhất cho mỗi môn
subjects = {
    'Tổng điểm': ('Tổng điểm', 'mean'),
    'Ngữ văn': ('Ngữ văn', 'mean'),
    'Toán': ('Toán', 'mean'),
    'Tiếng Anh': ('Tiếng Anh', 'mean'),
    'Vật lí': ('Vật lí', 'mean'),
    'Hóa học': ('Hóa học', 'mean'),
    'Sinh học': ('Sinh học', 'mean'),
    'Lịch sử': ('Lịch sử', 'mean'),
    'Địa lí': ('Địa lí', 'mean'),
    'GDCD/KTPL': ('GDCD/KTPL', 'mean')
}

lines.append("Cung hoàng đạo có điểm cao nhất theo môn:")
for subject, col in subjects.items():
    max_score = zodiac_stats[col].max()
    top_zodiacs = zodiac_stats[zodiac_stats[col] == max_score].index.tolist()
    lines.append(f"{subject}: {', '.join(top_zodiacs)}")
lines.append("")

# Danh sách các tổ hợp 3 môn phổ biến (khối A, B, C, D)
three_subject_combos = {
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

# Phân tích tổ hợp môn thi theo cung hoàng đạo
lines.append("Tổ hợp môn thi phổ biến nhất theo cung hoàng đạo:")
for zodiac in df_analysis['Cung Hoàng Đạo'].unique():
    if zodiac != 'Không xác định':
        top_combinations = df_analysis[df_analysis['Cung Hoàng Đạo'] == zodiac]['Tổ hợp tự chọn'].value_counts()
        max_count = top_combinations.max()
        top_combs = top_combinations[top_combinations == max_count].index.tolist()
        lines.append(f"{zodiac}: {', '.join(top_combs)}")

lines.append("\nTổ hợp điểm cao nhất theo Cung Hoàng Đạo:")
for combo_name, subjects_list in three_subject_combos.items():
    combo_means = {}
    for zodiac in df_analysis['Cung Hoàng Đạo'].unique():
        if zodiac != 'Không xác định':
            zodiac_data = df_analysis[df_analysis['Cung Hoàng Đạo'] == zodiac]
            # Tính tổng các mean của từng môn trong combo
            mean_score = sum([zodiac_data[sub].mean() for sub in subjects_list if sub in zodiac_data])
            if not pd.isna(mean_score):
                combo_means[zodiac] = mean_score

    if combo_means:
        max_score = max(combo_means.values())
        top_zodiacs = [z for z, s in combo_means.items() if s == max_score]
        combo_codes = combo_name.split(',')
        lines.append(f"\nTổ hợp {', '.join(combo_codes)} ({', '.join(subjects_list)}):")
        lines.append(f"Cung hoàng đạo tổng mean cao nhất: {', '.join(top_zodiacs)} (tổng mean: {max_score:.2f})")

# Ghi ra file
with open('h4.txt', 'w', encoding='utf-8-sig') as f:
    for line in lines:
        f.write(line + '\n')

# --- TRỰC QUAN HÓA ---

# Boxplot so sánh Tổng điểm theo Cung Hoàng Đạo
subjects_all = subjects_9 + ['Tổng điểm']

plt.figure(figsize=(20, 25))  # Tăng kích thước để chứa 10 boxplot
fig, axes = plt.subplots(5, 2, figsize=(20, 25))  # 5 hàng x 2 cột = 10 ô
axes = axes.flatten()

df_plot = df_analysis[df_analysis['Cung Hoàng Đạo'] != 'Không xác định']

for idx, subject in enumerate(subjects_all):
    ax = axes[idx]
    sns.boxplot(data=df_plot, x='Cung Hoàng Đạo', y=subject, ax=ax, palette='pastel')
    ax.set_title(f'Phân Bố {subject} Theo Cung Hoàng Đạo', fontsize=14, fontweight='bold')
    ax.set_xlabel('Cung Hoàng Đạo', fontsize=10)
    ax.set_ylabel(subject, fontsize=10)
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('h4_boxplot_all_subjects.png', dpi=300, bbox_inches='tight')
#Bỏ show plt.show() vì không cần hiển thị mà cần xuất png