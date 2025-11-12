import pandas as pd
from datetime import datetime
from tqdm import tqdm

# Đọc file CSV
df = pd.read_csv('diem_thi_thpt_2025.csv', dtype={'Số báo danh': str})

# Các cột điểm thi
score_columns = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']

# Từ điển ánh xạ tổ hợp môn
combo_4_subjects = {
    ('Toán', 'Ngữ văn', 'Vật lí', 'Hóa học'): 'A00, C01, C02, C05',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí'): 'A01, D01, D10, C01',
    ('Toán', 'Ngữ văn', 'Hóa học', 'Sinh học'): 'B00, B03, C02, C08',
    ('Toán', 'Ngữ văn', 'Lịch sử', 'Địa lí'): 'C00, A07, C03, C04',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Lịch sử'): 'D01, C03, D09, D14',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Hóa học'): 'D01, C02, D07, D12',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Sinh học'): 'D01, B03, D08, B08, D13',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Địa lí'): 'D01, C04, D10, D15',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'GDCD/KTPL'): 'D01, C14, D84, D66',
    ('Toán', 'Ngữ văn', 'Hóa học', 'Địa lí'): 'C02, C04, A06',
    ('Toán', 'Ngữ văn', 'Vật lí', 'GDCD/KTPL'): 'C01, C14, A10, C16',
    ('Toán', 'Ngữ văn', 'Hóa học', 'GDCD/KTPL'): 'C02, C14, A11, C1',
    ('Toán', 'Ngữ văn', 'Vật lí', 'Lịch sử'): 'C03, C01, A03, C07',
    ('Toán', 'Ngữ văn', 'Sinh học', 'Địa lí'): 'B03, C04, B02, C13',
    ('Toán', 'Ngữ văn', 'Hóa học', 'Lịch sử'): 'C03, C02, A05, C10',
    ('Toán', 'Ngữ văn', 'Sinh học', 'GDCD/KTPL'): 'B03, C14, B04',
    ('Toán', 'Ngữ văn', 'Sinh học', 'Lịch sử'): 'C03, B03, B01, C12',
    ('Toán', 'Ngữ văn', 'Lịch sử', 'GDCD/KTPL'): 'C03, C14, A08, C19',
    ('Toán', 'Ngữ văn', 'Địa lí', 'GDCD/KTPL'): 'C04, C14, A09, C20',
    ('Toán', 'Ngữ văn', 'Vật lí', 'Sinh học'): 'C14, B03, A02, C06',
    ('Toán', 'Ngữ văn', 'Vật lí', 'Địa lí'): 'C11, C04, A04, C09',
}

combo_6_subjects = {
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học'): 'A00, A01, A02, A16, B00, B03, B08, C01, C02, C05, C06, C08, D01, D07, D08, D11, D12, D13, D72, D90',
    ('Toán', 'Ngữ văn', 'Tiếng Anh', 'Địa lí', 'Lịch sử', 'GDCD/KTPL'): 'A07, A08, A09, C00, C03, C04, C14, C15, C19, C20, D01, D09, D10, D14, D15, D66, D78, D84, D96',
}

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
# Chuẩn hóa key để tra cứu nhanh
combo_4_subjects = {tuple(sorted(k)): v for k, v in combo_4_subjects.items()}
combo_6_subjects = {tuple(sorted(k)): v for k, v in combo_6_subjects.items()}
combo_3_subjects_lookup = {tuple(sorted(v)): k for k, v in combo_3_subjects.items()}

# Hàm lấy cung hoàng đạo
def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 'Bạch Dương'
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 'Kim Ngưu'
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 'Song Tử'
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 'Cự Giải'
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 'Sư Tử'
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 'Xử Nữ'
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 'Thiên Bình'
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 'Bọ Cạp'
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return 'Nhân Mã'
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 'Ma Kết'
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 'Bảo Bình'
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return 'Song Ngư'
    return None

# Task 1: Thêm cột Nhóm tuổi
print("Task 1: Thêm cột Nhóm tuổi...")
age_group = []
for index, row in tqdm(df.iterrows(), desc="Task 1: Nhóm tuổi", total=len(df)):
    birth_date = row['Ngày sinh']
    try:
        birth_year = int(birth_date.split('/')[-1])
        count = sum(pd.notna(row[col]) for col in score_columns)
        
        if birth_year == 2007:
            age_group.append('18')
        elif birth_year < 2007:
            if count == 4:
                age_group.append('>18')
            else:
                age_group.append('Thi lại')
        else:
            age_group.append('None')  
    except:
        age_group.append(None)

df['Nhóm tuổi'] = age_group

# Task 2: Thêm cột Tổ hợp tự chọn
print("Task 2: Thêm cột Tổ hợp tự chọn...")
combo = []
for index, row in tqdm(df.iterrows(), desc="Task 2: Tổ hợp tự chọn", total=len(df)):
    subjects_with_data = [col for col in score_columns if pd.notna(row[col])]
    age_group_val = age_group[index]  
    if age_group_val in ['18', '>18'] and len(subjects_with_data) == 4:
        subjects_tuple = tuple(sorted(subjects_with_data))
        combo_val = combo_4_subjects.get(subjects_tuple, None)
        combo.append(combo_val)
    elif age_group_val == 'Thi lại' and len(subjects_with_data) == 3:
        subjects_tuple = tuple(sorted(subjects_with_data))
        combo_val = combo_3_subjects_lookup.get(subjects_tuple, None)
        combo.append(combo_val)
    elif age_group_val == 'Thi lại' and len(subjects_with_data) == 6:
        subjects_tuple = tuple(sorted(subjects_with_data))
        combo_val = combo_6_subjects.get(subjects_tuple, None)
        combo.append(combo_val)
    else:
        combo.append(None)

df['Tổ hợp tự chọn'] = combo

# Task 3: Thêm cột Quý sinh
print("Task 3: Thêm cột Quý sinh...")
quarter = []
for index, row in tqdm(df.iterrows(), desc="Task 3: Quý sinh", total=len(df)):
    birth_date = row['Ngày sinh']
    try:
        month = int(birth_date.split('/')[1])
        if month in [1, 2, 3]:
            quarter.append('Q1')
        elif month in [4, 5, 6]:
            quarter.append('Q2')
        elif month in [7, 8, 9]:
            quarter.append('Q3')
        else:
            quarter.append('Q4')
    except:
        quarter.append(None)

df['Quý sinh'] = quarter

# Task 4: Thêm cột Điểm trung bình bắt buộc
print("Task 4: Thêm cột Điểm trung bình bắt buộc...")
avg_mandatory = []
for index, row in tqdm(df.iterrows(), desc="Task 4: Điểm TB bắt buộc", total=len(df)):
    toan = row['Toán']
    van = row['Ngữ văn']
    if pd.notna(toan) and pd.notna(van):
        avg_mandatory.append(round((float(toan) + float(van)) / 2, 2))
    else:
        avg_mandatory.append(None)

df['Điểm trung bình bắt buộc'] = avg_mandatory

# Task 5: Thêm cột Điểm trung bình tổ hợp
print("Task 5: Thêm cột Điểm trung bình tổ hợp...")
avg_combo = []
for index, row in tqdm(df.iterrows(), desc="Task 5: Điểm TB tổ hợp", total=len(df)):
    other_subjects = [col for col in score_columns if col not in ['Toán', 'Ngữ văn']]
    scores = [float(row[col]) for col in other_subjects if pd.notna(row[col])]
    if scores:
        avg_combo.append(round(sum(scores) / len(scores),2))
    else:
        avg_combo.append(None)

df['Điểm trung bình tổ hợp'] = avg_combo

# Task 6: Thêm cột Chênh lệch Văn Toán
print("Task 6: Thêm cột Chênh lệch Văn Toán...")
diff = []
for index, row in tqdm(df.iterrows(), desc="Task 6: Chênh lệch Văn Toán", total=len(df)):
    toan = row['Toán']
    van = row['Ngữ văn']
    if pd.notna(toan) and pd.notna(van):
        diff.append(round(float(van) - float(toan),2))
    else:
        diff.append(None)

df['Chênh lệch Văn Toán'] = diff

# Task 7: Thêm cột Cung Hoàng Đạo
print("Task 7: Thêm cột Cung Hoàng Đạo...")
zodiac = []
for index, row in tqdm(df.iterrows(), desc="Task 7: Cung Hoàng Đạo", total=len(df)):
    birth_date = row['Ngày sinh']
    try:
        day = int(birth_date.split('/')[0])
        month = int(birth_date.split('/')[1])
        zodiac.append(get_zodiac_sign(day, month))
    except:
        zodiac.append(None)

df['Cung Hoàng Đạo'] = zodiac

# Lưu file mới
df.to_csv('diem_thi_thpt_2025_new.csv', index=False, encoding='utf-8-sig')
print("Hoàn thành! Kết quả đã được lưu vào diem_thi_thpt_2025_new.csv")