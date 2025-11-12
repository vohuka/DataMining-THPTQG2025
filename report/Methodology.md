# BÁO CÁO NGHIÊN CỨU

**Tên đề tài:** Phân tích Tác động của Cải cách Kỳ thi Tốt nghiệp THPT 2025 đến Kết quả của thí sinh tại TP. Hồ Chí Minh

## Tóm tắt

Kỳ thi Tốt nghiệp THPT năm 2025 đánh dấu một bước chuyển mình quan trọng trong giáo dục Việt Nam với những thay đổi về cấu trúc môn thi, phương pháp đánh giá năng lực và tỷ trọng điểm học bạ. Nghiên cứu này sử dụng các kỹ thuật khai phá dữ liệu để phân tích sâu bộ dữ liệu điểm thi của các thí sinh tại TP. Hồ Chí Minh. 

**Mục tiêu chính:**
1. Đánh giá tác động của chương trình mới lên phổ điểm
2. Xác định các yếu tố ảnh hưởng chính đến kết quả thi
3. Phân tích xu hướng học tập của học sinh (thiên hướng Văn, Toán hay cân bằng)
4. Kiểm chứng các giả thuyết học thuật như "Hiệu ứng Tuổi Tương đối" (Relative Age Effect) trong bối cảnh giáo dục Việt Nam

Bằng cách kết hợp thống kê mô tả, mô hình học máy có diễn giải (XAI) và các kiểm định thống kê, nghiên cứu này mong muốn cung cấp những bằng chứng thực nghiệm giá trị, hỗ trợ các nhà hoạch định chính sách, các cơ sở giáo dục và giáo viên trong việc tối ưu hóa chương trình giảng dạy và đánh giá theo định hướng phát triển năng lực.

---

## 1. Giới thiệu (Introduction)

Kỳ thi Tốt nghiệp Trung học Phổ thông (THPT) quốc gia là một trong những kỳ thi quan trọng nhất, không chỉ quyết định việc xét tốt nghiệp mà còn là cơ sở chính cho việc tuyển sinh đại học. Năm 2025, kỳ thi có những thay đổi mang tính bước ngoặt:

- **Chương trình giáo dục phổ thông mới:** Lần đầu tiên áp dụng cho kỳ thi
- **Giảm số môn thi:** Chỉ còn 4 môn thi trong 3 buổi, giảm áp lực cho thí sinh
- **Tăng tỷ trọng xét tuyển:** Điểm học bạ chiếm 50% trong xét công nhận tốt nghiệp
- **Thay đổi cấu trúc đề thi:** Đặc biệt là môn Ngữ văn, chuyển từ ghi nhớ sang đánh giá năng lực tư duy, sáng tạo

Những thay đổi này tạo ra một bối cảnh đặc biệt để nghiên cứu sự thích ứng của học sinh. TP. Hồ Chí Minh (TPHCM), với vị thế là một trung tâm kinh tế - giáo dục hàng đầu, là một trường hợp điển hình để phân tích "lợi thế đô thị" (urban advantage) trong việc thích ứng với các cải cách giáo dục.

### Câu hỏi nghiên cứu (Research Questions)

**RQ1:** Cải cách thi năm 2025 đã tác động đến phân bố điểm của thí sinh TPHCM như thế nào so với mặt bằng chung của cả nước?

**RQ2:** Các yếu tố nhân khẩu học như độ tuổi và tháng sinh (Hiệu ứng Tuổi Tương đối) có ảnh hưởng đến kết quả học tập trong kỳ thi mới hay không?

**RQ3:** Mối tương quan giữa các môn thi đã thay đổi ra sao dưới tác động của việc giảm số môn thi và chương trình học tích hợp? Học sinh có xu hướng học thiên về Văn hay Toán?

**RQ4:** Yếu tố nào (môn thi, đặc điểm cá nhân, xu hướng học tập) là quan trọng nhất trong việc dự đoán tổng điểm của thí sinh theo mô hình đánh giá mới?

---

## 2. Phương pháp Nghiên cứu (Methodology)

Nghiên cứu sẽ được tiến hành qua ba giai đoạn chính:
1. Chuẩn bị và làm giàu dữ liệu
2. Phân tích thống kê mô tả và suy luận
3. Xây dựng mô hình dự báo và diễn giải

### 2.0. Mô tả Dữ liệu (Dataset Description)

Bộ dữ liệu nghiên cứu thu thập từ kỳ thi THPT Quốc gia năm 2025 tại TP.HCM, bao gồm thông tin cá nhân của thí sinh như số báo danh, họ tên, ngày sinh, tỉnh/thành phố (đều là TP.HCM), năm thi (2025) và điểm số từng môn thi cùng tổng điểm. Dữ liệu này cung cấp cơ sở đầy đủ và tin cậy để thực hiện các phân tích sâu về ảnh hưởng của cải cách kỳ thi mới.

---

### 2.1. Chuẩn bị và Làm giàu Dữ liệu (Data Preparation and Feature Engineering)

Dữ liệu đầu vào chỉ bao gồm các thông tin cơ bản. Để phục vụ cho các phân tích sâu, chúng ta cần thực hiện các bước làm sạch và tạo ra các đặc trưng mới (feature engineering).

#### Làm sạch dữ liệu (Data Cleaning)

- **Xử lý giá trị ngoại lai (Outliers):** Đảm bảo điểm thi nằm trong khoảng hợp lệ [0, 10]. Các giá trị bất thường sẽ được kiểm tra và xử lý
- **Xử lý trùng lặp:** Loại bỏ các bản ghi trùng lặp dựa trên số báo danh để đảm bảo tính duy nhất của mỗi thí sinh
- **Chuẩn hóa dữ liệu:** Chuyển đổi cột ngày sinh sang định dạng datetime để phục vụ các tính toán về sau

#### Làm giàu dữ liệu (Feature Engineering)

**1. Tính toán Tuổi và Nhóm tuổi**
- Tính tuổi chính xác của thí sinh tại thời điểm thi (năm 2025)
- Phân loại thí sinh vào 3 nhóm tuổi: "18 tuổi" (thí sinh thi đúng năm) và "> 18 tuổi" (thí sinh thi đúng năm như do lớn hơn 18) và "Thi lại" (thí sinh tự do hoặc thi lại) để phân tích sự khác biệt về kết quả

**2. Xác định Tổ hợp môn thi**

Suy luận tổ hợp môn thí sinh đã chọn dựa trên các cột điểm có giá trị khác 0.

**3. Phân tích Hiệu ứng Tuổi Tương đối (Relative Age Effect)**

- **Cơ sở khoa học:** Nhiều nghiên cứu của OECD đã chỉ ra rằng những học sinh sinh vào đầu năm học thường có lợi thế về mặt thể chất và nhận thức so với những em sinh cuối năm, dẫn đến kết quả học tập cao hơn
- **Cách làm:** Từ ngày sinh, tạo một biến mới là Quý sinh (Birth Quarter):
  - Quý 1: Tháng 1, 2, 3
  - Quý 2: Tháng 4, 5, 6
  - Quý 3: Tháng 7, 8, 9
  - Quý 4: Tháng 10, 11, 12
- Biến này sẽ được dùng để kiểm định giả thuyết về lợi thế của những người sinh sớm hơn trong năm

**4. Tạo các chỉ số phân tích**

- **diem_tb_batbuoc:** Điểm trung bình hai môn bắt buộc (Toán + Ngữ văn)
- **diem_tb_tohop:** Điểm trung bình của tổ hợp môn tự chọn
- **chenhlech_van_toan:** Hiệu số điểm (Ngữ văn - Toán) để đánh giá xu hướng học lệch và tác động của đề Văn mới
- **Cung hoàng đạo:** Xác định cung hoàng đạo từ ngày sinh cho phân tích khám phá

**5. Bảo mật dữ liệu**

Trước khi phân tích, các thông tin định danh như họ tên và số báo danh sẽ được ẩn danh hóa (ví dụ: sử dụng hàm băm) để đảm bảo quyền riêng tư.

---

### 2.2. Các Hướng Phân tích Chính

#### Hướng 1: Phân tích Phổ điểm và Tác động của Chương trình mới

**Mục tiêu:** Đánh giá tổng quan kết quả kỳ thi và xem xét sự khác biệt giữa các nhóm thí sinh.

**Phương pháp:**

**a) Thống kê mô tả (Descriptive Statistics)**

Tính các giá trị trung bình (mean), trung vị (median), độ lệch chuẩn (std), yếu vị (mode) cho từng môn thi. So sánh các giá trị này của TPHCM với số liệu toàn quốc được công bố để đánh giá vị thế của thành phố.

**b) Phân tích Lợi thế Đô thị (Urban Advantage Analysis)**

So sánh các chỉ số thống kê quan trọng của TPHCM (như điểm trung bình, tỷ lệ điểm giỏi ≥ 7, tỷ lệ điểm 10) với các số liệu tương ứng của toàn quốc được công bố. Phân tích này nhằm xác định các môn học mà học sinh TPHCM thể hiện sự vượt trội, qua đó đánh giá lợi thế của một trung tâm giáo dục lớn trong việc thích ứng với chương trình mới.

**c) Phân tích theo tổ hợp môn thi**

- So sánh thống kê mô tả giữa các tổ hợp môn
- Phân tích chi tiết các tổ hợp 3 môn phổ biến (combo_3) như A00 (Toán-Lý-Hóa), A01 (Toán-Lý-Anh), D01 (Toán-Văn-Anh) để xác định tổ hợp nào có kết quả cao nhất/thấp nhất

**d) Trực quan hóa**

Sử dụng biểu đồ Histogram và Kernel Density Estimation (KDE) để vẽ phổ điểm của từng môn, giúp nhận diện hình dạng phân phối (phân phối chuẩn, lệch trái/phải). Boxplot sẽ được dùng để so sánh điểm số giữa các nhóm tuổi và tổ hợp môn.

**e) Kiểm định thống kê (Statistical Tests)**

- **ANOVA:** So sánh sự khác biệt có ý nghĩa thống kê về điểm trung bình giữa các nhóm (nhóm tuổi, tổ hợp môn)
- **Kolmogorov-Smirnov test:** Kiểm tra xem phân phối điểm có tuân theo phân phối chuẩn hay không, một chỉ báo gián tiếp về tính hiệu quả của đề thi đánh giá năng lực

---

#### Hướng 2: Phân tích Xu hướng Học tập, Tương quan và Mô hình hóa Dự báo

**Mục tiêu:** 
- Xác định xu hướng học tập của học sinh (thiên Văn, thiên Toán, hay cân bằng)
- Tìm hiểu mối liên hệ giữa các môn học
- Xác định các yếu tố có ảnh hưởng lớn nhất đến kết quả thi

**Phương pháp:**

**a) Phân loại Xu hướng Học tập (Learning Tendency Classification)**

Sử dụng Cohen's d effect size để đo lường độ lệch giữa hiệu suất môn Ngữ văn và Toán của từng học sinh. Cohen's d là một công cụ chuẩn trong nghiên cứu giáo dục để đánh giá độ lớn của sự khác biệt.

**Công thức:**
```
Cohen's d = (Điểm Ngữ văn - Điểm Toán) / SD_pooled
```

Trong đó SD_pooled là độ lệch chuẩn chung của hai môn.

**Phân loại xu hướng học:**
- |d| < 0.2: **Cân bằng hoàn toàn** - không có sự lệch đáng kể
- 0.2 ≤ |d| < 0.5: **Cân bằng** - lệch nhỏ
- 0.5 ≤ |d| < 0.8: **Lệch rõ** - cân bằng nhưng có thiên hướng
- |d| ≥ 0.8: **Lệch mạnh**
  - d > 0.8: **Thiên Văn** (Ngữ văn mạnh hơn Toán)
  - d < -0.8: **Thiên Toán** (Toán mạnh hơn Ngữ văn)

Sau khi phân loại, sử dụng ANOVA để kiểm chứng xem xu hướng học tập có ảnh hưởng có ý nghĩa thống kê đến tổng điểm hay không.

**b) Phân tích tương quan**

Sử dụng ma trận tương quan Pearson/Spearman và trực quan hóa bằng heatmap để khám phá mối quan hệ tuyến tính/đơn điệu giữa điểm các môn thi. Giả thuyết cần kiểm chứng: "Liệu các môn trong cùng một tổ hợp (Lý-Hóa, Sử-Địa) có tương quan cao hơn sau cải cách do chương trình tích hợp?"

**c) Mô hình dự báo**

Xây dựng ba loại mô hình với độ phức tạp tăng dần:

1. **Hồi quy tuyến tính (Linear Regression):** 
   - Mô hình cơ sở để dự đoán tổng điểm dựa trên điểm các môn thành phần, tuổi và tổ hợp môn
   - Cung cấp baseline để so sánh với các mô hình phức tạp hơn

2. **Mô hình nâng cao (Gradient Boosting & Random Forest):**
   - Sử dụng các thuật toán mạnh hơn để cải thiện độ chính xác dự báo
   - Các mô hình này có khả năng nắm bắt các mối quan hệ phi tuyến phức tạp trong dữ liệu


**d) Diễn giải mô hình (Explainable AI - XAI)**

Sử dụng kỹ thuật SHAP (SHapley Additive exPlanations) để giải thích kết quả của mô hình Gradient Boosting:
- SHAP values cho biết mỗi yếu tố (điểm Toán, Văn, Anh, tuổi, xu hướng học, tổ hợp môn) đóng góp bao nhiêu vào việc dự đoán tổng điểm của một thí sinh cụ thể
- Điều này giúp trả lời câu hỏi RQ4 một cách minh bạch và khoa học
- Cho phép xác định feature importance tổng thể và feature importance riêng cho từng dự đoán

**e) Đánh giá mô hình**

Sử dụng phương pháp kiểm định chéo K-fold (K=10) và các độ đo:
- **R² (R-squared):** Đo lường tỷ lệ phương sai được giải thích bởi mô hình
- **RMSE (Root Mean Squared Error):** Đo lường sai số trung bình
- **MAE (Mean Absolute Error):** Đo lường sai số tuyệt đối trung bình

Đảm bảo tính tổng quát và độ tin cậy của mô hình.

---

#### Hướng 3: Phân tích Hiệu ứng Tuổi Tương đối (Relative Age Effect)

**Mục tiêu:** Kiểm chứng giả thuyết từ OECD rằng tháng sinh ảnh hưởng đến thành tích học tập tại Việt Nam.

**Giả thuyết (Hypothesis):** Thí sinh sinh vào Quý 1 và Quý 2 có điểm trung bình cao hơn một cách có ý nghĩa thống kê so với thí sinh sinh vào Quý 3 và Quý 4.

Tài liệu tham khảo: [OECD Report on Birth Month and School Performance](https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/05/how-a-student-s-month-of-birth-is-linked-to-performance-at-school_0d415fbc/822ea6ce-en.pdf)

**Phương pháp:**

- Sử dụng **ANOVA (Analysis of Variance)** để so sánh điểm trung bình tổng và điểm trung bình các môn thi giữa 4 nhóm "Quý sinh"
- Nếu kết quả ANOVA có ý nghĩa thống kê (p-value < 0.05), sẽ tiến hành kiểm định post-hoc (ví dụ: Tukey's HSD) để xác định cụ thể cặp quý nào có sự khác biệt
- Trực quan hóa kết quả bằng biểu đồ bar chart hoặc boxplot để thể hiện sự chênh lệch điểm số giữa các quý

---

#### Hướng 4: Phân tích Khám phá: Cung Hoàng Đạo và Kết quả Thi

Phần này trình bày một hướng phân tích mang tính khám phá, không dựa trên các giả thuyết khoa học đã được thiết lập, nhưng có thể mang lại những góc nhìn thú vị và thu hút sự quan tâm của độc giả đại chúng. Các kết quả trong mục này cần được diễn giải một cách thận trọng và xem như một phân tích bổ sung.

**Mục tiêu:**

Khám phá xem liệu có tồn tại sự khác biệt có ý nghĩa thống kê về kết quả thi giữa 12 nhóm cung hoàng đạo hay không. Phân tích này không nhằm chứng minh mối quan hệ nhân quả mà chỉ đơn thuần là một cách tiếp cận sáng tạo để khai thác dữ liệu.

**Các chỉ số so sánh:**
- Điểm trung bình tổng các môn
- Điểm của các môn thi riêng lẻ (Toán, Ngữ văn, Ngoại ngữ,...)
- Điểm trung bình của tổ hợp môn

**Phương pháp:**

1. **Tạo Đặc trưng:** Dựa vào ngày sinh, ánh xạ mỗi thí sinh vào một trong 12 cung hoàng đạo tương ứng

2. **Phân tích Thống kê:**
   - Tính toán điểm trung bình, độ lệch chuẩn cho từng cung hoàng đạo
   - Sử dụng ANOVA để kiểm tra xem sự chênh lệch về điểm trung bình giữa 12 nhóm có ý nghĩa thống kê hay không (p < 0.05)
   - Nếu ANOVA có ý nghĩa, tiến hành kiểm định post-hoc (Tukey's HSD)

3. **Trực quan hóa:**
   - Biểu đồ để so sánh điểm trung bình của các cung hoàng đạo
   - Biểu đồ hộp (Boxplot) để thể hiện sự phân bố điểm của từng cung

---

## 3. Kết quả Dự kiến và Đóng góp

### Kết quả dự kiến

- Một bức tranh toàn cảnh về kết quả kỳ thi THPT 2025 tại TPHCM, chỉ ra các xu hướng chính trong phổ điểm và sự khác biệt giữa các nhóm thí sinh
- Phân tích chi tiết các xu hướng học tập chính của học sinh TPHCM (tỷ lệ thiên Văn, thiên Toán, cân bằng) và mối liên hệ của chúng với kết quả học tập tổng thể
- Bằng chứng thực nghiệm về sự tồn tại hoặc không tồn tại của "Hiệu ứng Tuổi Tương đối" trong môi trường giáo dục Việt Nam
- Xác định được các yếu tố (môn học, xu hướng học tập, tổ hợp môn) có ảnh hưởng lớn nhất đến thành công của thí sinh trong kỳ thi theo định hướng mới
- So sánh hiệu suất dự báo giữa mô hình tổng quát và mô hình chuyên biệt cho từng nhóm học sinh

### Đóng góp khoa học và thực tiễn

**Về khoa học:**
- Cung cấp một phương pháp luận hoàn chỉnh để phân tích dữ liệu giáo dục quy mô lớn, có thể tái áp dụng cho các tỉnh thành khác hoặc các kỳ thi sau này
- Áp dụng Cohen's d effect size - một công cụ chuẩn trong nghiên cứu giáo dục quốc tế - vào bối cảnh Việt Nam để phân loại xu hướng học tập
- Kết hợp phân tích thống kê truyền thống với kỹ thuật học máy hiện đại (XAI/SHAP) để đảm bảo cả độ chính xác và tính diễn giải

**Về thực tiễn:**
- Kết quả nghiên cứu có thể là nguồn tham khảo quan trọng cho Bộ Giáo dục và Đào tạo, các Sở Giáo dục và các trường THPT trong việc:
  - Điều chỉnh chính sách, chương trình dạy và học phù hợp hơn với mục tiêu phát triển năng lực
  - Hiểu rõ hơn về xu hướng học tập của học sinh để tư vấn định hướng nghề nghiệp
  - Đánh giá hiệu quả của cải cách thi năm 2025
- Cung cấp góc nhìn dựa trên dữ liệu về "lợi thế đô thị" của TPHCM, giúp định hướng các chiến lược giáo dục đặc thù

---

## 4. Công cụ Thực thi

**Ngôn ngữ lập trình:** Python 3.8+

**Thư viện chính:**
- **Xử lý dữ liệu:** pandas, numpy
- **Trực quan hóa:** matplotlib, seaborn
- **Thống kê và Học máy:** 
  - scipy (cho các kiểm định thống kê như ANOVA, K-S test)
  - scikit-learn (cho các mô hình hồi quy và phân loại: Linear Regression, Random Forest, Gradient Boosting)
  - statsmodels (cho phân tích thống kê nâng cao)
- **Diễn giải mô hình:** shap (cho SHAP values và feature importance)
- **Tiện ích:** tqdm (progress bar), warnings (xử lý cảnh báo)

**Môi trường phát triển:**
- Jupyter Notebook / Python IDE
- Yêu cầu RAM: Tối thiểu 8GB (khuyến nghị 16GB cho tập dữ liệu lớn)

**Mở rộng:** Nếu bộ dữ liệu vượt quá 200,000 thí sinh hoặc cần xử lý nhiều tỉnh thành, có thể cân nhắc sử dụng Dask hoặc PySpark để xử lý song song, tăng tốc độ tính toán.

---

## 5. Hạn chế và Hướng phát triển

### Hạn chế

- Nghiên cứu chỉ tập trung vào TP. Hồ Chí Minh, do đó kết quả có thể không đại diện cho toàn bộ học sinh Việt Nam
- Thiếu dữ liệu so sánh với các năm trước để đánh giá rõ hơn tác động của cải cách 2025
- Các biến ngữ cảnh như điều kiện kinh tế - xã hội của gia đình, chất lượng trường học, năng lực giáo viên chưa được đưa vào phân tích

### Hướng phát triển trong tương lai

- Mở rộng nghiên cứu sang các tỉnh thành khác để tăng tính đại diện
- Thu thập dữ liệu các năm trước (2023, 2024) để có phân tích so sánh trước-sau cải cách
- Bổ sung các biến ngữ cảnh (SES, school quality) để phân tích sâu hơn
- Kết hợp phương pháp định tính (phỏng vấn giáo viên, học sinh) để hiểu sâu hơn về các xu hướng quan sát được
