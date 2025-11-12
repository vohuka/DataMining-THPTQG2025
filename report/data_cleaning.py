import pandas as pd
from datetime import datetime
from tqdm import tqdm  # Thêm import tqdm để tạo progress bar

# Đọc file CSV
df = pd.read_csv('diem_thi_thpt_2025.csv')

# Các cột điểm thi
score_columns = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']

# Mở file để ghi kết quả
with open('data_cleaning.txt', 'w', encoding='utf-8') as f:
    f.write("Kết quả kiểm tra dữ liệu:\n\n")
    
    # Task 1: Phát hiện giá trị ngoại lai trong điểm thi
    f.write("1. Hàng có giá trị ngoại lai (điểm thi không trong [0,10]):\n")
    for index, row in tqdm(df.iterrows(), desc="Task 1: Phát hiện ngoại lai", total=len(df)):
        outlier = False
        for col in score_columns:
            val = row[col]
            if pd.notna(val):
                try:
                    val = float(val)
                    if not (0 <= val <= 10):
                        outlier = True
                        break
                except ValueError:
                    outlier = True
                    break
        if outlier:
            f.write(f"Hàng {index+1}: {row.to_dict()}\n")
    f.write("\n")
    
    # Task 2: Kiểm tra Ngày sinh
    f.write("2. Ngày sinh không phù hợp (không đúng định dạng DD/MM/YYYY hoặc không hợp lệ):\n")
    for index, row in tqdm(df.iterrows(), desc="Task 2: Kiểm tra Ngày sinh", total=len(df)):
        birth_date = row['Ngày sinh']
        if pd.notna(birth_date):
            try:
                datetime.strptime(birth_date, '%d/%m/%Y')
            except ValueError:
                f.write(f"Hàng {index+1}: {birth_date}\n")
        else:
            f.write(f"Hàng {index+1}: {birth_date} (rỗng)\n")
    f.write("\n")
    
    # Task 3: Phát hiện trùng lặp SBD
    print("Task 3: Phát hiện trùng lặp SBD đang chạy...")
    f.write("3. Giá trị trùng lặp dựa trên Số báo danh:\n")
    duplicates = df[df.duplicated(subset=['Số báo danh'], keep=False)]
    if not duplicates.empty:
        for sbd in duplicates['Số báo danh'].unique():
            dup_rows = df[df['Số báo danh'] == sbd]
            f.write(f"SBD {sbd}:\n")
            for index, row in dup_rows.iterrows():
                f.write(f"  Hàng {index+1}: {row.to_dict()}\n")
    else:
        f.write("Không có trùng lặp.\n")
    f.write("\n")
    print("Task 3 hoàn thành.")
    
    # Task 4: Hàng có >=5 cột điểm thi có dữ liệu
    f.write("4. Hàng có >=5 cột điểm thi có dữ liệu:\n")
    for index, row in tqdm(df.iterrows(), desc="Task 4: Kiểm tra >=5 cột dữ liệu", total=len(df)):
        count = sum(pd.notna(row[col]) for col in score_columns)
        if count >= 5:
            f.write(f"Hàng {index+1}: {row.to_dict()}\n")
    f.write("\n")
    
    # Task 5: Hàng có >6 cột điểm thi có dữ liệu
    f.write("5. Hàng có >6 cột điểm thi có dữ liệu:\n")
    for index, row in tqdm(df.iterrows(), desc="Task 5: Kiểm tra >6 cột dữ liệu", total=len(df)):
        count = sum(pd.notna(row[col]) for col in score_columns)
        if count > 6:
            f.write(f"Hàng {index+1}: {row.to_dict()}\n")
    f.write("\n")
    
    # Task 6: Kiểm tra thí sinh thi cả nhóm 1 (Vật lí hoặc Hóa học) và nhóm 2 (Lịch sử hoặc Địa lí)
    f.write("6. Hàng có thí sinh thi cả nhóm 1 (Vật lí hoặc Hóa học) và nhóm 2 (Lịch sử hoặc Địa lí):\n")
    group1_cols = ['Vật lí', 'Hóa học']  # Nhóm 1
    group2_cols = ['Lịch sử', 'Địa lí']  # Nhóm 2
    for index, row in tqdm(df.iterrows(), desc="Task 6: Kiểm tra tổ hợp môn", total=len(df)):
        has_group1 = any(pd.notna(row[col]) for col in group1_cols)
        has_group2 = any(pd.notna(row[col]) for col in group2_cols)
        if has_group1 and has_group2:
            f.write(f"Hàng {index+1}: {row.to_dict()}\n")
    f.write("\n")

    # Task 7: Hàng có <4 cột điểm thi có dữ liệu hợp lệ
    f.write("7. Hàng có <4 cột điểm thi có dữ liệu hợp lệ:\n")
    for index, row in tqdm(df.iterrows(), desc="Task 7: Kiểm tra <4 cột dữ liệu hợp lệ", total=len(df)):
        valid_count = 0
        for col in score_columns:
            val = row[col]
            if pd.notna(val):
                try:
                    val = float(val)
                    if 0 <= val <= 10:
                        valid_count += 1
                except ValueError:
                    pass  # Không phải số, không đếm
        if valid_count < 4:
            f.write(f"Hàng {index+1}: {row.to_dict()}\n")
    f.write("\n")

print("Kết quả đã được ghi vào data_cleaning.txt")