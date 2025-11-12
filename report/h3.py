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

lines.append("===== QUÝ SINH VÀ KẾT QUẢ THI =====\n")

# Danh sách 9 môn
subjects_9 = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 
              'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']

# Đặt lại thứ tự cho cột "Quý sinh"
quarter_order = ['Q1', 'Q2', 'Q3', 'Q4']
df_analysis['Quý sinh'] = pd.Categorical(df_analysis['Quý sinh'], categories=quarter_order, ordered=True)

# Thống kê theo quý sinh
quarter_stats = df_analysis.groupby('Quý sinh').agg({
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

lines.append("Thống kê điểm theo Quý sinh:")
lines.append(str(quarter_stats.sort_values(('Tổng điểm', 'mean'), ascending=False)))
lines.append("")

# ANOVA test
quarters = [df_analysis[df_analysis['Quý sinh'] == q]['Tổng điểm'].dropna() 
           for q in df_analysis['Quý sinh'].unique() 
           if pd.notna(q)]
f_stat_quarter, p_value_quarter = stats.f_oneway(*quarters)

lines.append("ANOVA Test - So sánh điểm tổng giữa các quý sinh:")
lines.append(f"   F-statistic: {f_stat_quarter:.4f}")
lines.append(f"   p-value: {p_value_quarter:.6f}")
lines.append(
    f"   Kết luận: Với p-value = {p_value_quarter:.4f}, "
    f"{'có' if p_value_quarter < 0.05 else 'không có'} bằng chứng đủ mạnh để khẳng định sự khác biệt có ý nghĩa thống kê giữa các nhóm."
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

lines.append("Quý sinh có điểm cao nhất theo môn:")
for subject, col in subjects.items():
    max_score = quarter_stats[col].max()
    top_quarters = quarter_stats[quarter_stats[col] == max_score].index.tolist()
    lines.append(f"{subject}: {', '.join(top_quarters)}")
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

# Phân tích tổ hợp môn thi theo Quý sinh
lines.append("Tổ hợp môn thi phổ biến nhất theo Quý sinh:")
for quarter in df_analysis['Quý sinh'].unique():
    if pd.notna(quarter):
        top_combinations = df_analysis[df_analysis['Quý sinh'] == quarter]['Tổ hợp tự chọn'].value_counts()
        max_count = top_combinations.max()
        top_combs = top_combinations[top_combinations == max_count].index.tolist()
        lines.append(f"{quarter}: {', '.join(top_combs)}")

lines.append("\nTổ hợp điểm cao nhất theo Quý sinh:")
for combo_name, subjects_list in three_subject_combos.items():
    combo_means = {}
    for quarter in df_analysis['Quý sinh'].unique():
        if pd.notna(quarter):
            quarter_data = df_analysis[df_analysis['Quý sinh'] == quarter]
            # Tính tổng các mean của từng môn trong combo
            mean_score = sum([quarter_data[sub].mean() for sub in subjects_list if sub in quarter_data])
            if not pd.isna(mean_score):
                combo_means[quarter] = mean_score

    if combo_means:
        max_score = max(combo_means.values())
        top_quarters = [q for q, s in combo_means.items() if s == max_score]
        combo_codes = combo_name.split(',')
        lines.append(f"\nTổ hợp {', '.join(combo_codes)} ({', '.join(subjects_list)}):")
        lines.append(f"Quý sinh tổng mean cao nhất: {', '.join(top_quarters)} (tổng mean: {max_score:.2f})")

# Ghi ra file
with open('h3.txt', 'w', encoding='utf-8-sig') as f:
    for line in lines:
        f.write(line + '\n')

# --- TRỰC QUAN HÓA ---

# Boxplot so sánh Tổng điểm theo Quý sinh
subjects_all = subjects_9 + ['Tổng điểm']

plt.figure(figsize=(20, 25))  # Tăng kích thước để chứa 10 boxplot
fig, axes = plt.subplots(5, 2, figsize=(20, 25))  # 5 hàng x 2 cột = 10 ô
axes = axes.flatten()

df_plot = df_analysis[df_analysis['Quý sinh'].notna()]

for idx, subject in enumerate(subjects_all):
    ax = axes[idx]
    sns.boxplot(data=df_plot, x='Quý sinh', y=subject, ax=ax, palette='pastel', order=quarter_order)
    ax.set_title(f'Phân Bố {subject} Theo Quý sinh', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quý sinh', fontsize=10)
    ax.set_ylabel(subject, fontsize=10)
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('h3_boxplot_all_subjects.png', dpi=300, bbox_inches='tight')
#Bỏ show plt.show() vì không cần hiển thị mà cần xuất png