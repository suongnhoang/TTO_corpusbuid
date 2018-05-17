# <p style="text-align: center;color: #0066ff">XÂY DỰNG NGỮ LIỆU TIẾNG VIỆT</p>
### <p style="color: #0066ff">I. CÁC BƯỚC XÂY DỰNG NGỮ LIỆU TIẾNG VIỆT:</p>
 - Bước đầu tiên ta xác định khai thác các loại hình và khai thác theo từng ngày. Lấy tất cả các bài báo trong 1 ngày của từng loại lĩnh vực (trừ một vài lĩnh vực không thể filter được).
 - Thống kê các bài theo thể loại, theo năm, theo thể loại của từng năm và trung bình từng loại mỗi năm. Thông qua kết quả visualize, chọn cụm thể loại có số lượng bài báo nhiều và tương đối nhiều để cân bằng cụm đó, còn lại ta vét cạn các bài post. Cách thức lọc khá đơn giản, với N là ngững của từng lĩnh vực trên 1 năm, nếu số bài ít hơn ngưỡng đó, ta lấy tất cả bài năm đó của lĩnh vực đó, còn ngược lại nếu cao hơn, ta random lại vị trí và chọn ra N bài để khai thác, cứ như vậy cho đến khi nào hết tất cả các lĩnh vực. kết quả cuối cùng ta thu được là khai thác ***72.23%*** trên tổng số bài báo của tất cả các lĩnh vực trong 10 năm qua.        
 - Do các bài báo trên mạng có sự khác nhau về định dạng nên không thể xác định được heading và paragraph của từng đoạn nên chỉ có cách lưu lại tất cả các đoạn riêng lẻ theo từng ***"\<div\>"***.

### <p style="color: #0066ff">II. KẾT QUẢ:</p>       
> "ĐANG CHỜ LÒI CON MẮT, CẬP NHẬT SAU..."

### <p style="color: #0066ff">III. ĐỀ XUẤT CẢI TIẾN XÂY DỰNG NGỮ LIỆU TIẾNG VIỆT:</p>
 - Thêm độ chịu đựng cho việc gửi request lên server.
 - Thay thế các tiến trình đọc, ghi qua hệ cơ sở dữ liệu bằng ***mongodb***.
 - Thêm giao diện bằng framework ***Flask*** và ***reactjs***.
 
### <p style="color: #0066ff">IV. THAM KHẢO:</p>
 - Định dạng corpus TEI: http://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-teiCorpus.html
 - Định dạng header TEI: http://www.tei-c.org/release/doc/tei-p5-doc/en/html/HD.html
 - Định dạng text TEI: http://www.tei-c.org/release/doc/tei-p5-doc/en/html/DS.html
