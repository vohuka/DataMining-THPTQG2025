import pandas as pd
import hashlib
from cryptography.fernet import Fernet
import os

# ===== CHỌN PHƯƠNG PHÁP MÃ HÓA =====
# Phương pháp 1: SHA-256 Hash (một chiều, không thể giải mã)
# Phương pháp 2: Fernet Encryption (hai chiều, có thể giải mã bằng key)

def hash_sha256(text):
    """Mã hóa một chiều bằng SHA-256"""
    return hashlib.sha256(str(text).encode()).hexdigest()

def encrypt_fernet(text, cipher):
    """Mã hóa hai chiều bằng Fernet"""
    return cipher.encrypt(str(text).encode()).decode()

def encrypt_csv(input_file, output_file, method='sha256'):
    """
    Mã hóa Số báo danh và Họ và tên trong file CSV
    
    Parameters:
    - input_file: đường dẫn file CSV gốc
    - output_file: đường dẫn file CSV sau khi mã hóa
    - method: 'sha256' (một chiều) hoặc 'fernet' (hai chiều)
    """
    # Đọc file CSV
    df = pd.read_csv(input_file, dtype={'Số báo danh': str})
    
    cipher = None
    key = None
    
    if method == 'fernet':
        # Tạo hoặc đọc key
        key_file = 'encryption_key.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            print(f"[!] Đã tạo key mới và lưu vào {key_file}")
        
        cipher = Fernet(key)
    
    # Mã hóa Số báo danh và Họ và tên
    print(f"Đang mã hóa bằng phương pháp: {method.upper()}...")
    
    if method == 'sha256':
        df['Số báo danh'] = df['Số báo danh'].apply(hash_sha256)
        df['Họ và tên'] = df['Họ và tên'].apply(hash_sha256)
    elif method == 'fernet':
        df['Số báo danh'] = df['Số báo danh'].apply(lambda x: encrypt_fernet(x, cipher))
        df['Họ và tên'] = df['Họ và tên'].apply(lambda x: encrypt_fernet(x, cipher))
    
    # Lưu file mới
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✓ Đã lưu file mã hóa: {output_file}")
    
    if method == 'fernet':
        print(f"✓ Key đã được lưu tại: {key_file}")
        print(f"[!] LƯU Ý: Giữ key này an toàn để có thể giải mã sau này!")

# ===== SỬ DỤNG =====

# PHƯƠNG PHÁP 1: SHA-256 (một chiều, không thể giải mã)
print("\n===== MÃ HÓA FILE 1 (diem_thi_thpt_2025.csv) =====")
encrypt_csv('diem_thi_thpt_2025.csv', 'diem_thi_thpt_2025_encrypted.csv', method='sha256')

print("\n===== MÃ HÓA FILE 2 (diem_thi_thpt_2025_new.csv) =====")
encrypt_csv('diem_thi_thpt_2025_new.csv', 'diem_thi_thpt_2025_new_encrypted.csv', method='sha256')

# PHƯƠNG PHÁP 2: Fernet (hai chiều, có thể giải mã)
# Bỏ comment các dòng dưới nếu muốn dùng Fernet
# print("\n===== MÃ HÓA FILE 1 BẰNG FERNET =====")
# encrypt_csv('diem_thi_thpt_2025.csv', 'diem_thi_thpt_2025_fernet.csv', method='fernet')

# print("\n===== MÃ HÓA FILE 2 BẰNG FERNET =====")
# encrypt_csv('diem_thi_thpt_2025_new.csv', 'diem_thi_thpt_2025_new_fernet.csv', method='fernet')

print("\n===== HOÀN THÀNH =====")