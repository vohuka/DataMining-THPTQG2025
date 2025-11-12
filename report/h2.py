import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# ===== ĐỌC DỮ LIỆU =====
csv_path = 'diem_thi_thpt_2025_new.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")
df_analysis = pd.read_csv(csv_path)

# Tách riêng cột nhân khẩu học để xử lý
subjects_9 = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 
              'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD/KTPL']
demographic_cols = ['Nhóm tuổi']

subjects_all = subjects_9 + ['Tổng điểm']

# Lưu kết quả vào file text
lines = []
lines.append("===== HƯỚNG 2: PHÂN TÍCH TƯƠNG QUAN VÀ MÔ HÌNH HÓA DỰ BÁO =====\n")

# ===== PHẦN 1: PHÂN LOẠI XU HƯỚNG HỌC DÙNG COHEN'S D =====

def classify_learning_tendency_cohens_d(row, score_col_1='Ngữ văn', score_col_2='Toán'):
    """
    Phân loại xu hướng học dựa trên Cohen's d (Effect Size)
    
    Cohen's d = (Mean_col1 - Mean_col2) / SD_pooled
    
    Phân loại:
    - |d| < 0.2: Cân bằng (không đáng kể)
    - 0.2 ≤ |d| < 0.5: Cân bằng (lệch nhỏ)
    - 0.5 ≤ |d| < 0.8: Lệch rõ (lệch trung bình)
    - |d| ≥ 0.8: Lệch mạnh (lệch lớn)
    
    Tham khảo: Cohen, J. (1988). Statistical power analysis for the behavioral sciences.
    """
    val_1 = row[score_col_1]
    val_2 = row[score_col_2]
    
    if pd.isna(val_1) or pd.isna(val_2):
        return {'category': 'Không xác định', 'cohens_d': np.nan, 
                'magnitude': 'N/A', 'direction': 'N/A'}
    
    # Tính chênh lệch cá nhân
    diff = val_1 - val_2
    
    # Tính Cohen's d theo cách tiêu chuẩn trên toàn bộ dữ liệu
    # Lấy SD từ cột "Chênh lệch Văn Toán" nếu có, nếu không tính từ dữ liệu
    if 'Chênh lệch Văn Toán' in df_analysis.columns:
        std_diff = df_analysis['Chênh lệch Văn Toán'].dropna().std()
    else:
        std_diff = (df_analysis[score_col_1] - df_analysis[score_col_2]).dropna().std()
    
    cohens_d = diff / std_diff if std_diff != 0 else 0
    
    # Phân loại dựa trên magnitude của Cohen's d
    if abs(cohens_d) < 0.2:
        magnitude = 'Cân bằng (lệch không đáng kể)'
        if abs(cohens_d) < 0.05:
            category = 'Cân bằng hoàn toàn'
        else:
            category = 'Cân bằng'
    elif 0.2 <= abs(cohens_d) < 0.5:
        magnitude = 'Cân bằng (lệch nhỏ)'
        category = 'Cân bằng (lệch nhỏ)'
    elif 0.5 <= abs(cohens_d) < 0.8:
        magnitude = 'Lệch rõ (lệch trung bình)'
        category = 'Lệch rõ'
    else:  # >= 0.8
        magnitude = 'Lệch mạnh (lệch lớn)'
        category = 'Lệch mạnh'
    
    # Xác định hướng lệch
    if cohens_d > 0:
        direction = f'Thiên Văn'
    elif cohens_d < 0:
        direction = f'Thiên Toán'
    else:
        direction = 'Cân bằng hoàn toàn'
    
    return {
        'category': category,
        'cohens_d': cohens_d,
        'magnitude': magnitude,
        'direction': direction
    }

# Áp dụng phân loại cho từng thí sinh
print("Đang phân loại xu hướng học theo Cohen's d...")
classification_results = []
for index, row in tqdm(df_analysis.iterrows(), total=len(df_analysis), desc="Phần 1: Phân loại xu hướng học"):
    classification_results.append(classify_learning_tendency_cohens_d(row, 'Ngữ văn', 'Toán'))

df_analysis['Xu hướng học'] = [r['direction'] for r in classification_results]
df_analysis['Cohens_d'] = [r['cohens_d'] for r in classification_results]
df_analysis['Effect_Size_Magnitude'] = [r['magnitude'] for r in classification_results]
df_analysis['Xu hướng phân loại'] = [r['category'] for r in classification_results]

lines.append("\n===== PHẦN 1: PHÂN NHÓM XU HƯỚNG HỌC THEO COHEN'S D =====\n")

lines.append("Ghi chú lý thuyết:")
lines.append("  - Cohen's d là effect size chuẩn trong nghiên cứu giáo dục (Cohen, 1988)")
lines.append("  - Công thức: d = (Mean_Văn - Mean_Toán) / SD_chung")
lines.append("  - Phân loại effect size:")
lines.append("    * |d| < 0.2: Lệch không đáng kể")
lines.append("    * 0.2 ≤ |d| < 0.5: Lệch nhỏ")
lines.append("    * 0.5 ≤ |d| < 0.8: Lệch trung bình")
lines.append("    * |d| ≥ 0.8: Lệch lớn\n")

lines.append("Phân bố thí sinh theo xu hướng học:")
lines.append(str(df_analysis['Xu hướng phân loại'].value_counts()))
lines.append("")

lines.append("Phân bố theo hướng (Thiên Văn / Cân bằng / Thiên Toán):")
lines.append(str(df_analysis['Xu hướng học'].value_counts()))
lines.append("")

lines.append("Thống kê Cohen's d:")
lines.append(f"  - Trung bình: {df_analysis['Cohens_d'].mean():.4f}")
lines.append(f"  - Trung vị: {df_analysis['Cohens_d'].median():.4f}")
lines.append(f"  - Độ lệch chuẩn: {df_analysis['Cohens_d'].std():.4f}")
lines.append(f"  - Min: {df_analysis['Cohens_d'].min():.4f}")
lines.append(f"  - Max: {df_analysis['Cohens_d'].max():.4f}\n")

# ===== PHẦN 2: ANOVA TEST SO SÁNH CÁC NHÓM =====

lines.append("\n===== PHẦN 2: ANOVA TEST - SO SÁNH ĐIỂM GIỮA CÁC XU HƯỚNG HỌC =====\n")

# ANOVA cho 3 hướng (Thiên Văn / Cân bằng / Thiên Toán)
tendency_groups_main = [
    df_analysis[df_analysis['Xu hướng học'] == 'Thiên Văn']['Tổng điểm'].dropna(),
    df_analysis[(df_analysis['Xu hướng học'] != 'Thiên Văn') & 
                (df_analysis['Xu hướng học'] != 'Thiên Toán')]['Tổng điểm'].dropna(),
    df_analysis[df_analysis['Xu hướng học'] == 'Thiên Toán']['Tổng điểm'].dropna()
]

f_stat_main, p_value_main = stats.f_oneway(*tendency_groups_main)

lines.append("ANOVA Test: So sánh Tổng điểm giữa 3 hướng (Thiên Văn / Cân bằng / Thiên Toán)")
lines.append(f"  - F-statistic: {f_stat_main:.4f}")
lines.append(f"  - p-value: {p_value_main:.6f}")
lines.append(f"  - Kết luận: {'CÓ' if p_value_main < 0.05 else 'KHÔNG CÓ'} sự khác biệt có ý nghĩa thống kê (α=0.05)\n")

# ANOVA cho 4 nhóm chi tiết (bao gồm effect size magnitude)
magnitude_groups = df_analysis['Effect_Size_Magnitude'].unique()
magnitude_groups = [m for m in magnitude_groups if pd.notna(m)]

magnitude_anova_groups = [df_analysis[df_analysis['Effect_Size_Magnitude'] == m]['Tổng điểm'].dropna() 
                          for m in magnitude_groups if len(df_analysis[df_analysis['Effect_Size_Magnitude'] == m]) > 0]

if len(magnitude_anova_groups) >= 2:
    f_stat_mag, p_value_mag = stats.f_oneway(*magnitude_anova_groups)
    
    lines.append("ANOVA Test: So sánh Tổng điểm giữa các magnitude của Cohen's d")
    lines.append(f"  - F-statistic: {f_stat_mag:.4f}")
    lines.append(f"  - p-value: {p_value_mag:.6f}")
    lines.append(f"  - Kết luận: {'CÓ' if p_value_mag < 0.05 else 'KHÔNG CÓ'} sự khác biệt có ý nghĩa thống kê\n")

# Thống kê mô tả
lines.append("Thống kê mô tả theo xu hướng học:")
tendency_stats = df_analysis.groupby('Xu hướng học').agg({
    'Tổng điểm': ['mean', 'std', 'count'],
    'Toán': 'mean',
    'Ngữ văn': 'mean',
    'Tiếng Anh': 'mean',
    'Cohens_d': ['mean', 'std'],
    'Điểm trung bình bắt buộc': 'mean',
    'Điểm trung bình tổ hợp': 'mean'
}).round(2)

lines.append(str(tendency_stats.sort_values(('Tổng điểm', 'mean'), ascending=False)))
lines.append("")

# ANOVA cho từng môn
lines.append("\nPhân tích ANOVA cho từng môn theo xu hướng học:\n")
for subject in subjects_9:
    tendency_subject_groups = [df_analysis[df_analysis['Xu hướng học'] == d][subject].dropna() 
                               for d in ['Thiên Văn', 'Thiên Toán']]
    
    # Lọc nhóm có dữ liệu
    tendency_subject_groups = [g for g in tendency_subject_groups if len(g) > 0]
    
    if len(tendency_subject_groups) >= 2:
        f_stat_subj, p_value_subj = stats.f_oneway(*tendency_subject_groups)
        
        lines.append(f"{subject}:")
        lines.append(f"   F-statistic: {f_stat_subj:.4f}, p-value: {p_value_subj:.6f}")
        lines.append(f"   Kết luận: {'CÓ' if p_value_subj < 0.05 else 'KHÔNG CÓ'} hiệu ứng từ xu hướng học\n")

# ===== PHẦN 3: PHÂN TÍCH MA TRẬN TƯƠNG QUAN =====
print("\nPhần 3: Phân tích ma trận tương quan...")

correlation_matrix = df_analysis[subjects_9].corr(method='pearson')

# Vẽ heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Ma trận tương quan Pearson giữa các môn thi (Năm 2025)', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('h2_correlation_matrix.png', dpi=300, bbox_inches='tight')

# Tìm các cặp môn có tương quan cao nhất
corr_pairs = []
for i in range(len(subjects_9)):
    for j in range(i+1, len(subjects_9)):
        corr_pairs.append({
            'Môn 1': subjects_9[i],
            'Môn 2': subjects_9[j],
            'Hệ số tương quan': correlation_matrix.iloc[i, j]
        })

corr_df = pd.DataFrame(corr_pairs).sort_values('Hệ số tương quan', ascending=False)
lines.append("Top 10 cặp môn có tương quan cao nhất:")
lines.append(str(corr_df.head(10).to_string(index=False)))
lines.append("")

# Tương quan trong các tổ hợp
lines.append("\nTương quan trong các tổ hợp nổi bật:")
lines.append(f"Vật lí - Hóa học: {correlation_matrix.loc['Vật lí', 'Hóa học']:.3f}")
lines.append(f"Lịch sử - Địa lí: {correlation_matrix.loc['Lịch sử', 'Địa lí']:.3f}")
lines.append(f"Toán - Vật lí: {correlation_matrix.loc['Toán', 'Vật lí']:.3f}")
lines.append("")

# ===== PHẦN 4: MÔ HÌNH DỰ BÁO CHUNG (TẤT CẢ THÍCH SINH) =====
print("\nPhần 4: Xây dựng mô hình dự báo...")

# ===== Thêm 'Nhóm tuổi' vào features và Mã hóa (One-Hot) =====
feature_cols = subjects_9 + demographic_cols
X_raw = df_analysis[feature_cols].copy()
y = df_analysis['Tổng điểm'].copy()

# Xử lý missing values cho điểm thi (điền trung bình)
X_raw[subjects_9] = X_raw[subjects_9].fillna(X_raw[subjects_9].mean())

# Xử lý missing values cho cột nhân khẩu học (điền 'Không xác định')
for col in demographic_cols:
    if col in X_raw.columns:
        X_raw[col] = X_raw[col].fillna('Không xác định')

# Mã hóa One-Hot cho các cột nhân khẩu học
# drop_first=True để tránh bẫy biến giả (dummy variable trap)
X = pd.get_dummies(X_raw, columns=demographic_cols, drop_first=True)

# Lấy danh sách tên cột cuối cùng sau khi mã hóa để dùng cho SHAP
feature_cols_processed = X.columns.tolist()

# Lọc y và X khớp nhau (loại bỏ các hàng có Tổng điểm là NaN)
mask = y.notna()
X = X[mask]
y = y[mask]

# Chia tập train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Cập nhật tên cột cho X_test để SHAP dùng (vì X_train, X_test không có header)
X_test.columns = feature_cols_processed

lines.append(f"Kích thước tập train: {len(X_train)}")
lines.append(f"Kích thước tập test: {len(X_test)}\n")
lines.append(f"Các đặc trưng sử dụng: {', '.join(feature_cols_processed)}\n")


# Mô hình 1: Linear Regression
print("  - Huấn luyện Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

lines.append("1. MÔ HÌNH HỒI QUY TUYẾN TÍNH (LINEAR REGRESSION)")
lines.append(f"   R² Score: {r2_score(y_test, y_pred_lr):.4f}")
lines.append(f"   RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.4f}")
lines.append(f"   MAE: {mean_absolute_error(y_test, y_pred_lr):.4f}\n")

# Mô hình 2: Random Forest
print("  - Huấn luyện Random Forest...")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

lines.append("2. MÔ HÌNH RANDOM FOREST")
lines.append(f"   R² Score: {r2_score(y_test, y_pred_rf):.4f}")
lines.append(f"   RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf)):.4f}")
lines.append(f"   MAE: {mean_absolute_error(y_test, y_pred_rf):.4f}\n")

# Mô hình 3: Gradient Boosting
print("  - Huấn luyện Gradient Boosting...")
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42, 
                                     learning_rate=0.1, max_depth=5)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

lines.append("3. MÔ HÌNH GRADIENT BOOSTING")
lines.append(f"   R² Score: {r2_score(y_test, y_pred_gb):.4f}")
lines.append(f"   RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_gb)):.4f}")
lines.append(f"   MAE: {mean_absolute_error(y_test, y_pred_gb):.4f}\n")

# ===== K-FOLD CROSS VALIDATION =====
print("\nPhần 4b: K-Fold Cross Validation...")
lines.append("\n===== K-FOLD CROSS VALIDATION (K=10) =====\n")

kf = KFold(n_splits=10, shuffle=True, random_state=42)

# Linear Regression
print("  - Linear Regression CV...")
lr_scores = cross_val_score(lr_model, X, y, cv=kf, 
                            scoring='neg_mean_squared_error', n_jobs=-1)
lr_rmse_scores = np.sqrt(-lr_scores)

lines.append("Linear Regression:")
lines.append(f"   RMSE trung bình: {lr_rmse_scores.mean():.4f}")
lines.append(f"   Độ lệch chuẩn: {lr_rmse_scores.std():.4f}\n")

# Random Forest
print("  - Random Forest CV...")
rf_scores = cross_val_score(rf_model, X, y, cv=kf, 
                            scoring='neg_mean_squared_error', n_jobs=-1)
rf_rmse_scores = np.sqrt(-rf_scores)

lines.append("Random Forest:")
lines.append(f"   RMSE trung bình: {rf_rmse_scores.mean():.4f}")
lines.append(f"   Độ lệch chuẩn: {rf_rmse_scores.std():.4f}\n")

# Gradient Boosting
print("  - Gradient Boosting CV...")
gb_scores = cross_val_score(gb_model, X, y, cv=kf, 
                            scoring='neg_mean_squared_error', n_jobs=-1)
gb_rmse_scores = np.sqrt(-gb_scores)

lines.append("Gradient Boosting:")
lines.append(f"   RMSE trung bình: {gb_rmse_scores.mean():.4f}")
lines.append(f"   Độ lệch chuẩn: {gb_rmse_scores.std():.4f}\n")

# Trực quan hóa Cross Validation
models_cv = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'Mean RMSE': [lr_rmse_scores.mean(), rf_rmse_scores.mean(), gb_rmse_scores.mean()],
    'Std RMSE': [lr_rmse_scores.std(), rf_rmse_scores.std(), gb_rmse_scores.std()]
})

plt.figure(figsize=(10, 6))
plt.errorbar(models_cv['Model'], models_cv['Mean RMSE'], 
             yerr=models_cv['Std RMSE'], fmt='o-', capsize=5, capthick=2, 
             markersize=10, linewidth=2, color='steelblue')
plt.title('So sánh hiệu suất mô hình với 10-Fold Cross Validation', 
          fontsize=14, fontweight='bold')
plt.ylabel('Mean RMSE', fontsize=12)
plt.xlabel('Model', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('h2_cross_validation_comparison.png', dpi=300, bbox_inches='tight')

# ===== DIỄN GIẢI MÔ HÌNH VỚI SHAP =====
# ===== SHAP sẽ tự động bao gồm 'Nhóm tuổi' =====
lines.append("\n===== DIỄN GIẢI MÔ HÌNH VỚI SHAP (SHapley Additive exPlanations) =====\n")
lines.append("Phân tích này cho thấy mức độ ảnh hưởng của từng đặc trưng (bao gồm các môn học và Nhóm tuổi)\n")

try:
    import shap
    
    # Đảm bảo X_test có tên cột chính xác
    X_test_shap = pd.DataFrame(X_test, columns=feature_cols_processed)
    
    explainer = shap.TreeExplainer(gb_model)
    shap_values = explainer.shap_values(X_test_shap)
    
    # Summary Plot (Bar)
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_test_shap, plot_type="bar", show=False)
    plt.title('SHAP Feature Importance (bao gồm Nhóm tuổi)', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('h2_shap_feature_importance.png', dpi=300, bbox_inches='tight')
    
    # Detailed Summary Plot (Dot)
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_test_shap, show=False)
    plt.title('SHAP Summary Plot - Phân tích chi tiết đóng góp của từng đặc trưng', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('h2_shap_detailed_summary.png', dpi=300, bbox_inches='tight')
    
    # Feature Importance từ SHAP
    feature_importance = pd.DataFrame({
        'Feature': feature_cols_processed,
        'SHAP Importance': np.abs(shap_values).mean(axis=0)
    }).sort_values('SHAP Importance', ascending=False)
    
    lines.append("Độ quan trọng của các đặc trưng (SHAP values):")
    lines.append(str(feature_importance.to_string(index=False)))
    lines.append("")
    
except ImportError:
    lines.append("SHAP không được cài đặt. Vui lòng chạy: pip install shap\n")

# ===== PHẦN 5: MÔ HÌNH DỰ BÁO THEO XU HƯỚNG HỌC =====
print("\nPhần 5: Mô hình dự báo theo xu hướng học...")
lines.append("\n===== PHẦN 5: MÔ HÌNH DỰ BÁO THEO XU HƯỚNG HỌC (COHEN'S D) =====\n")

for tendency in tqdm(['Thiên Văn', 'Thiên Toán'], desc="Phần 5: Xu hướng học"):
    df_subset = df_analysis[df_analysis['Xu hướng học'] == tendency].copy()
    
    # Lấy lại X_subset theo logic của Phần 4 (bao gồm Nhóm tuổi)
    X_subset_raw = df_subset[feature_cols].copy()
    y_subset = df_subset['Tổng điểm'].copy()
    
    X_subset_raw[subjects_9] = X_subset_raw[subjects_9].fillna(X_subset_raw[subjects_9].mean())
    for col in demographic_cols:
        if col in X_subset_raw.columns:
            X_subset_raw[col] = X_subset_raw[col].fillna('Không xác định')
            
    X_subset = pd.get_dummies(X_subset_raw, columns=demographic_cols, drop_first=True)
    
    # Đồng bộ hóa các cột (Phòng trường hợp một nhóm không có đủ các loại Nhóm tuổi)
    X_subset = X_subset.reindex(columns=feature_cols_processed, fill_value=0)
    
    mask_subset = y_subset.notna()
    X_subset = X_subset[mask_subset]
    y_subset = y_subset[mask_subset]
    
    if len(X_subset) > 10 and len(y_subset) > 10:
        X_train_sub, X_test_sub, y_train_sub, y_test_sub = train_test_split(
            X_subset, y_subset, test_size=0.2, random_state=42
        )
        
        gb_sub = GradientBoostingRegressor(n_estimators=100, random_state=42)
        gb_sub.fit(X_train_sub, y_train_sub)
        y_pred_sub = gb_sub.predict(X_test_sub)
        
        lines.append(f"Xu hướng '{tendency}' (N={len(X_subset)}):")
        lines.append(f"   R² Score: {r2_score(y_test_sub, y_pred_sub):.4f}")
        lines.append(f"   RMSE: {np.sqrt(mean_squared_error(y_test_sub, y_pred_sub)):.4f}")
        lines.append(f"   MAE: {mean_absolute_error(y_test_sub, y_pred_sub):.4f}\n")

# ===== PHẦN 6: MÔ HÌNH DỰ BÁO THEO COMBO_3 =====
print("\nPhần 6: Mô hình dự báo theo tổ hợp 3 môn...")
lines.append("\n===== PHẦN 6: MÔ HÌNH DỰ BÁO THEO TỔ HỢP 3 MÔN (COMBO_3) =====\n")

# Định nghĩa combo_3
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

# Hàm tách combo code đầu tiên
def extract_first_combo(combo_str):
    if pd.isna(combo_str) or combo_str == '':
        return 'Không xác định'
    first_combo = str(combo_str).split(',')[0].strip()
    return first_combo

df_analysis['Combo_Code'] = df_analysis['Tổ hợp tự chọn'].apply(extract_first_combo)

# Lọc những combo có ≥30 thí sinh
combo_counts = df_analysis['Combo_Code'].value_counts()
valid_combos = combo_counts[combo_counts >= 30].index.tolist()

lines.append(f"Số tổ hợp có ≥30 thí sinh: {len(valid_combos)}")
lines.append(f"Danh sách tổ hợp: {', '.join(valid_combos)}\n")

# Mô hình dự báo cho từng combo_3
lines.append("\nMô hình dự báo Gradient Boosting cho từng tổ hợp 3 môn:\n")

combo_model_results = []

for combo in tqdm(valid_combos, desc="Phần 6: Mô hình combo"):
    df_combo = df_analysis[df_analysis['Combo_Code'] == combo].copy()
    
    if combo in combo_3_subjects:
        combo_feature_cols = combo_3_subjects[combo] + demographic_cols
    else:
        combo_feature_cols = subjects_9 + demographic_cols
    
    # Kiểm tra cột tồn tại
    combo_feature_cols = [col for col in combo_feature_cols if col in df_combo.columns]
    
    if len(combo_feature_cols) == 0:
        continue
    
    X_combo_raw = df_combo[combo_feature_cols].copy()
    y_combo = df_combo['Tổng điểm'].copy()
    
    # Xử lý missing values chi tiết
    subj_combo = [c for c in combo_feature_cols if c in subjects_9]
    demo_combo = [c for c in combo_feature_cols if c in demographic_cols]
    
    # Điền missing values cho subjects (dùng mean của combo đó, nếu không thì mean tổng thể)
    for col in subj_combo:
        if X_combo_raw[col].isna().any():
            fill_val = X_combo_raw[col].mean()
            if pd.isna(fill_val):
                fill_val = df_analysis[col].mean()
            X_combo_raw[col] = X_combo_raw[col].fillna(fill_val)
    
    # Điền missing values cho demographic
    for col in demo_combo:
        X_combo_raw[col] = X_combo_raw[col].fillna('Không xác định')
    
    # One-Hot Encoding
    X_combo = pd.get_dummies(X_combo_raw, columns=demo_combo, drop_first=True)
    
    # Đồng bộ hóa cột (bỏ những cột không cần)
    X_combo = X_combo.fillna(0)
    
    # Lọc dữ liệu hợp lệ
    mask_combo = y_combo.notna()
    X_combo = X_combo[mask_combo]
    y_combo = y_combo[mask_combo]
    
    # Kiểm tra lại NaN
    if X_combo.isnull().any().any() or y_combo.isnull().any():
        continue
    
    if len(X_combo) > 10 and len(y_combo) > 10:
        try:
            X_train_combo, X_test_combo, y_train_combo, y_test_combo = train_test_split(
                X_combo, y_combo, test_size=0.2, random_state=42
            )
            
            gb_combo = GradientBoostingRegressor(n_estimators=100, random_state=42)
            gb_combo.fit(X_train_combo, y_train_combo)
            y_pred_combo = gb_combo.predict(X_test_combo)
            
            r2 = r2_score(y_test_combo, y_pred_combo)
            rmse = np.sqrt(mean_squared_error(y_test_combo, y_pred_combo))
            mae = mean_absolute_error(y_test_combo, y_pred_combo)
            
            subj_combo_str = ', '.join([c for c in subj_combo if c in combo_feature_cols])
            lines.append(f"Tổ hợp '{combo}' (N={len(X_combo)}):")
            lines.append(f"   Môn: {subj_combo_str}")
            lines.append(f"   R² Score: {r2:.4f}")
            lines.append(f"   RMSE: {rmse:.4f}")
            lines.append(f"   MAE: {mae:.4f}\n")
            
            combo_model_results.append({
                'Tổ hợp': combo,
                'Số thí sinh': len(X_combo),
                'R² Score': r2,
                'RMSE': rmse,
                'MAE': mae
            })
        except Exception as e:
            print(f"Lỗi khi huấn luyện combo {combo}: {str(e)}")
            continue

# ===== PHẦN 7: BOXPLOT THEO XU HƯỚNG HỌC =====
print("\nPhần 7: Vẽ biểu đồ Boxplot xu hướng học...")

fig, axes = plt.subplots(5, 2, figsize=(16, 20))
axes = axes.flatten()

subjects_to_plot = subjects_9 + ['Điểm trung bình bắt buộc']

for idx, subject in enumerate(tqdm(subjects_to_plot, desc="Phần 7: Vẽ Boxplot xu hướng")):
    ax = axes[idx]
    df_plot = df_analysis[df_analysis['Xu hướng học'] != 'Không xác định']
    sns.boxplot(data=df_plot, x='Xu hướng học', y=subject, ax=ax, palette='Set2', 
                order=['Thiên Văn', 'Thiên Toán'] if 'Thiên Văn' in df_plot['Xu hướng học'].unique() else None)
    ax.set_title(f'{subject}', fontsize=11, fontweight='bold')
    ax.set_xlabel('')
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('So sánh điểm theo Xu hướng học (dựa trên Cohen\'s d)', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('h2_boxplot_learning_tendency.png', dpi=300, bbox_inches='tight')
plt.close()

# ===== PHẦN 8: BOXPLOT THEO TỔ HỢP COMBO (SỬA LẠI) =====
print("\nPhần 8: Vẽ biểu đồ Boxplot tổ hợp 3 môn (theo từng môn, đầy đủ combos)...")

# DÙNG TẤT CẢ combo_3_subjects (bỏ ngưỡng ≥30) để không bị mất các tổ hợp nhỏ
all_combo_codes = list(combo_3_subjects.keys())

# Map: môn -> các combo chứa môn đó
combos_by_subject = {
    subj: [code for code, subs in combo_3_subjects.items() if subj in subs]
    for subj in subjects_9
}

# Danh sách cần vẽ: 9 môn + 2 chỉ số bổ sung
subjects_combo_plot = subjects_9 + ['Tổng điểm', 'Điểm trung bình bắt buộc']

fig, axes = plt.subplots(len(subjects_combo_plot), 1, figsize=(22, 3.0 * len(subjects_combo_plot)))
axes = axes.flatten()

for idx, subject in enumerate(subjects_combo_plot):
    ax = axes[idx]

    if subject in subjects_9:
        # Lấy tất cả combo có môn này (không lọc theo valid_combos)
        allowed_combos = combos_by_subject.get(subject, [])
        # Thêm 'Không xác định' nếu tồn tại
        include_unknown = 'Không xác định' in df_analysis['Combo_Code'].unique()
        x_order = allowed_combos + (['Không xác định'] if include_unknown else [])
        # Lọc dữ liệu chỉ các combo thật sự chứa môn đó hoặc Không xác định
        df_sub = df_analysis[df_analysis['Combo_Code'].isin(x_order)].copy()
        # Loại bỏ hàng không có điểm môn đó
        df_sub = df_sub[pd.notna(df_sub[subject])]
    else:
        # Với 'Tổng điểm' và 'Điểm trung bình bắt buộc' -> dùng toàn bộ combos xuất hiện
        include_unknown = 'Không xác định' in df_analysis['Combo_Code'].unique()
        x_order = all_combo_codes + (['Không xác định'] if include_unknown else [])
        df_sub = df_analysis[df_analysis['Combo_Code'].isin(x_order)].copy()
        metric_col = subject
        df_sub = df_sub[pd.notna(df_sub[metric_col])]

    if df_sub.empty or len(x_order) == 0:
        ax.text(0.5, 0.5, 'Không có dữ liệu', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(subject, fontsize=12, fontweight='bold')
        ax.set_xlabel('Tổ hợp môn', fontsize=11)
        ax.set_ylabel(subject, fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        continue

    sns.boxplot(data=df_sub, x='Combo_Code', y=subject, order=x_order,
                ax=ax, palette='Set3')
    ax.set_title(f'{subject}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Tổ hợp 3 môn', fontsize=11)
    ax.set_ylabel(subject, fontsize=11)
    ax.tick_params(axis='x', rotation=40)
    ax.grid(axis='y', alpha=0.25)

plt.suptitle('Phân bố điểm theo từng MÔN và các TỔ HỢP 3 MÔN liên quan',
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('h2_boxplot_combo_3.png', dpi=300, bbox_inches='tight')
plt.close()

# ===== PHẦN 9: PHÂN PHỐI COHEN'S D =====
print("\nPhần 9: Vẽ biểu đồ phân phối Cohen's d...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df_analysis['Cohens_d'].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].axvline(df_analysis['Cohens_d'].mean(), color='red', linestyle='--', linewidth=2, label=f'Trung bình: {df_analysis["Cohens_d"].mean():.3f}')
axes[0].axvline(df_analysis['Cohens_d'].median(), color='green', linestyle='--', linewidth=2, label=f'Trung vị: {df_analysis["Cohens_d"].median():.3f}')
axes[0].set_title('Phân bố Cohen\'s d', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Cohen\'s d', fontsize=11)
axes[0].set_ylabel('Tần suất', fontsize=11)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Boxplot
axes[1].boxplot(df_analysis['Cohens_d'].dropna())
axes[1].set_title('Boxplot Cohen\'s d', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Cohen\'s d', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('h2_cohens_d_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ===== THAY ĐỔI 4: Thêm phần phân tích so sánh cho 'Nhóm tuổi' =====
print("\nPhần 10: Phân tích so sánh theo Nhóm tuổi...")
lines.append("\n===== PHẦN 10: PHÂN TÍCH SO SÁNH THEO NHÓM TUỔI =====\n")

# Lấy các nhóm tuổi duy nhất, loại bỏ NaN
age_groups = df_analysis['Nhóm tuổi'].dropna().unique()
age_group_data = [df_analysis[df_analysis['Nhóm tuổi'] == g]['Tổng điểm'].dropna() for g in age_groups]

# Chỉ thực hiện ANOVA nếu có 2 nhóm trở lên
if len(age_group_data) >= 2:
    f_stat_age, p_value_age = stats.f_oneway(*age_group_data)
    lines.append("ANOVA Test: So sánh Tổng điểm giữa các Nhóm tuổi")
    lines.append(f"  - F-statistic: {f_stat_age:.4f}")
    lines.append(f"  - p-value: {p_value_age:.6f}")
    lines.append(f"  - Kết luận: {'CÓ' if p_value_age < 0.05 else 'KHÔNG CÓ'} sự khác biệt có ý nghĩa thống kê (α=0.05)\n")

# Thống kê mô tả
lines.append("Thống kê mô tả theo Nhóm tuổi:")
age_stats = df_analysis.groupby('Nhóm tuổi').agg({
    'Tổng điểm': ['mean', 'std', 'count'],
    'Toán': 'mean',
    'Ngữ văn': 'mean',
    'Tiếng Anh': 'mean',
    'Hóa học': 'mean',
    'Vật lí': 'mean',
    'Sinh học': 'mean',
    'Lịch sử': 'mean',
    'Địa lí': 'mean',
    'GDCD/KTPL': 'mean'
}).round(2)
lines.append(str(age_stats.sort_values(('Tổng điểm', 'mean'), ascending=False)))
lines.append("")

# Vẽ Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_analysis.dropna(subset=['Nhóm tuổi', 'Tổng điểm']), 
            x='Nhóm tuổi', y='Tổng điểm', palette='viridis')
plt.title('So sánh Tổng điểm giữa các Nhóm tuổi', fontsize=14, fontweight='bold')
plt.xlabel('Nhóm tuổi', fontsize=12)
plt.ylabel('Tổng điểm', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('h2_boxplot_nhom_tuoi.png', dpi=300, bbox_inches='tight')
plt.close()

# ===== LƯU KẾT QUẢ =====
print("\nPhần cuối: Lưu kết quả...")
with open('h2_new.txt', 'w', encoding='utf-8-sig') as f:
    for line in lines:
        f.write(line + '\n')

print("\n✓ Đã lưu kết quả vào file: h2_results_cohens_d.txt")
print("\nCác file biểu đồ được lưu:")
print("  - h2_correlation_matrix.png")
print("  - h2_cross_validation_comparison.png")
print("  - h2_shap_feature_importance.png")
print("  - h2_shap_detailed_summary.png")
print("  - h2_boxplot_learning_tendency.png")
print("  - h2_boxplot_combo_3.png")
print("  - h2_cohens_d_distribution.png")
print("  - h2_boxplot_nhom_tuoi.png") # Biểu đồ mới
print("\n✓ Hoàn thành phân tích Hướng 2 với Cohen's d và Nhóm tuổi!")