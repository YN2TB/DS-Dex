---
subject: AI Test — ôn thi
tags: [ai, on-thi, tu-luan, ngan-hang-cau-hoi]
source: "https://hungbil.github.io/AI-TEST/ — bóc tách toàn bộ 23 đề (1380 câu)"
---

# Ngân hàng câu tự luận & câu code

> [!info] Nguồn và phạm vi
> Trích xuất trực tiếp từ dữ liệu đề của **https://hungbil.github.io/AI-TEST/** — 23 đề × 60 câu = **1380 câu**, gồm **1265 trắc nghiệm**, **69 câu tự luận**, **46 câu code**.
> Trang tự ghi rõ: *"đây là bộ câu hỏi ôn tập cộng đồng, biên soạn từ phản hồi không chính thức của người thi... **không phải đề thi chính thức hoặc đề bị lộ**"* — hãy dùng như tài liệu luyện tập, không phải đề tủ.
> **Đáp án mẫu và rubric bên dưới là của chính bộ đề**, không phải tôi viết. Tôi chỉ nhóm lại theo chủ đề và bỏ trùng lặp.

## 📊 Phân bố

| Nhóm chủ đề | Số câu tự luận | Tổng điểm |
|---|---|---|
| Thiết kế bài toán AI cho sản phẩm | 15 | 72 |
| Chọn mô hình & đánh đổi kỹ thuật | 17 | 120 |
| Đánh giá mô hình: metric, confusion matrix, overfitting | 9 | 72 |
| RAG, retrieval & chống bịa đặt | 8 | 48 |
| Dữ liệu & tiền xử lý | 6 | 48 |
| API, tích hợp & debug | 4 | 32 |
| Responsible AI: privacy, fairness, oversight | 10 | 60 |
| **Tổng** | **69** | **452** |

**Thang điểm câu tự luận:** 4 điểm × 20 câu, 6 điểm × 10 câu, 8 điểm × 39 câu.
Câu 8 điểm đều được gắn nhãn `sfiaBand: L3-L4`, `difficulty: applied-reasoning` — đây là nhóm dùng để phân loại mức sẵn sàng lên Level 4.

---

## ✍️ Phần 1 — Câu tự luận (69 câu)

### Thiết kế bài toán AI cho sản phẩm

#### 1. Bạn cần xây AI phân loại và ưu tiên ticket hỗ trợ khách hàng. Trình bày output, dữ liệu đầu vào, metric chính, rủi ro và baseline không-AI.
**4 điểm** · Module C · 🔁 **xuất hiện 4 lần** (chỉ khác số liệu): `E01-C19`, `E04-C20`, `E06-C19`, `E09-C20`

> [!example]- Đáp án mẫu
> Output nên là label loại ticket + priority/risk score + ranking.
> Dữ liệu gồm nội dung ticket, lịch sử khách hàng, SLA, sản phẩm liên quan.
> Metric nên kết hợp chất lượng phân loại với thời gian xử lý hoặc tỷ lệ ticket quan trọng được đẩy lên.
> Rủi ro gồm bias, privacy, leakage, tự động ưu tiên sai; cần human review cho ca quan trọng.
> Baseline là rule-based theo keyword/SLA.

> [!check]- Rubric chấm (5 ý)
> - [ ] Nêu output rõ: label/score/ranking.
> - [ ] Nêu ít nhất 2 nguồn dữ liệu hợp lý.
> - [ ] Chọn metric gắn với mục tiêu sản phẩm.
> - [ ] Nêu rủi ro và cách giảm.
> - [ ] Có baseline không-AI.

*Tags:* `product-ai`

#### 2. Xây AI trích xuất thông tin từ hồ sơ PDF. Nêu pipeline, kiểm tra chất lượng và human review.
**4 điểm** · Module C · 🔁 **xuất hiện 4 lần** (chỉ khác số liệu): `E02-C20`, `E04-C19`, `E07-C20`, `E09-C19`

> [!example]- Đáp án mẫu
> Pipeline gồm OCR/parse, tách trường cần trích xuất, LLM hoặc model extraction, kiểm tra định dạng/ràng buộc, trả confidence, lưu log.
> Quality kiểm bằng bộ hồ sơ gắn nhãn, so sánh từng field, đo lỗi nghiêm trọng.
> Human review cho field quan trọng, confidence thấp hoặc dữ liệu mâu thuẫn.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có parse/OCR.
> - [ ] Có extraction và validation.
> - [ ] Có confidence.
> - [ ] Có đánh giá theo field.
> - [ ] Có human review.

*Tags:* `document-ai`

#### 3. Đề xuất tính năng AI gợi ý câu trả lời cho nhân viên CS. Làm sao để tăng năng suất nhưng không gây rủi ro trả lời sai?
**4 điểm** · Module C · 🔁 **xuất hiện 4 lần** (chỉ khác số liệu): `E03-C20`, `E05-C19`, `E08-C20`, `E10-C19`

> [!example]- Đáp án mẫu
> AI chỉ nên gợi ý, nhân viên duyệt trước khi gửi.
> Dùng RAG từ policy mới nhất, citation, guardrail không bịa cam kết, log phản hồi, đánh giá bằng thời gian xử lý và chất lượng CSAT/QA.
> Ca nhạy cảm như khiếu nại pháp lý/tài chính cần chuyển người có thẩm quyền.

> [!check]- Rubric chấm (5 ý)
> - [ ] AI là copilot, không tự gửi trong ca nhạy cảm.
> - [ ] Dùng nguồn/policy có kiểm soát.
> - [ ] Có guardrail/citation.
> - [ ] Có metric năng suất và chất lượng.
> - [ ] Có escalation.

*Tags:* `copilot`

#### 4. Thiết kế trợ lý FAQ cho học viên dùng mô hình ngôn ngữ cho khoảng 110 câu hỏi thường gặp. Ràng buộc: - FAQ thông thường được trả lời tự động. - Không gửi dữ liệu nhạy cảm thô cho dịch vụ ngoài. - Yêu cầu thay đổi thông tin, hoàn tiền hoặc quyết định ảnh hưởng lớn phải chuyển người. Hãy trình bày: (1) cách phân luồng; (2) một ví dụ hội thoại; (3) cách kiểm thử và giám sát.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E01-C11`, `N26E06-C10`

> [!example]- Đáp án mẫu
> Dùng một bước phân loại yêu cầu: FAQ có thể trả tự động từ tài liệu đã duyệt, còn yêu cầu nhạy cảm hoặc có hành động ảnh hưởng lớn phải handoff cho người có thẩm quyền.
> Dữ liệu nhạy cảm được loại bỏ hoặc thay mã trước khi gửi ra ngoài.
> Ví dụ hỏi giờ làm việc thì trả trực tiếp; yêu cầu đổi thông tin tài khoản thì chuyển người.
> Kiểm thử cả câu bình thường, câu chứa PII và câu vượt quyền; theo dõi lỗi, độ trễ và tỷ lệ handoff.

> [!check]- Rubric chấm (5 ý)
> - [ ] Phân biệt FAQ và yêu cầu rủi ro.
> - [ ] Không gửi dữ liệu nhạy cảm thô.
> - [ ] Có human handoff.
> - [ ] Có ví dụ hội thoại.
> - [ ] Có kiểm thử/monitoring cơ bản.

*Tags:* `llm` `privacy` `human-in-the-loop` `essay`

#### 5. Thiết kế trợ lý hỗ trợ dịch vụ dùng mô hình ngôn ngữ cho khoảng 190 câu hỏi thường gặp. Ràng buộc: - FAQ thông thường được trả lời tự động. - Không gửi dữ liệu nhạy cảm thô cho dịch vụ ngoài. - Yêu cầu thay đổi thông tin, hoàn tiền hoặc quyết định ảnh hưởng lớn phải chuyển người. Hãy trình bày: (1) cách phân luồng; (2) một ví dụ hội thoại; (3) cách kiểm thử và giám sát.
**8 điểm** · Module C · `L3-L4` · `N26E09-C10` (Khóa mới 2026 · Đề 09)

> [!example]- Đáp án mẫu
> Dùng một bước phân loại yêu cầu: FAQ có thể trả tự động từ tài liệu đã duyệt, còn yêu cầu nhạy cảm hoặc có hành động ảnh hưởng lớn phải handoff cho người có thẩm quyền.
> Dữ liệu nhạy cảm được loại bỏ hoặc thay mã trước khi gửi ra ngoài.
> Ví dụ hỏi giờ làm việc thì trả trực tiếp; yêu cầu đổi thông tin tài khoản thì chuyển người.
> Kiểm thử cả câu bình thường, câu chứa PII và câu vượt quyền; theo dõi lỗi, độ trễ và tỷ lệ handoff.

> [!check]- Rubric chấm (5 ý)
> - [ ] Phân biệt FAQ và yêu cầu rủi ro.
> - [ ] Không gửi dữ liệu nhạy cảm thô.
> - [ ] Có human handoff.
> - [ ] Có ví dụ hội thoại.
> - [ ] Có kiểm thử/monitoring cơ bản.

*Tags:* `llm` `privacy` `human-in-the-loop` `essay`

---

### Chọn mô hình & đánh đổi kỹ thuật

#### 6. Bạn phải chọn giữa model 6B chạy nhanh/rẻ và model 8B chất lượng cao hơn cho app mobile. Nêu tiêu chí quyết định.
**4 điểm** · Module C · 🔁 **xuất hiện 4 lần** (chỉ khác số liệu): `E01-C20`, `E03-C19`, `E06-C20`, `E08-C19`

> [!example]- Đáp án mẫu
> Cần so sánh chất lượng theo benchmark nghiệp vụ, latency trên thiết bị/hạ tầng, chi phí inference, RAM/VRAM, tần suất request, rủi ro output sai và khả năng fallback.
> Có thể dùng 6B cho luồng thường, 8B cho ca khó hoặc premium nếu chênh lệch chất lượng đáng tiền.

> [!check]- Rubric chấm (5 ý)
> - [ ] Nêu chất lượng theo task thật.
> - [ ] Nêu latency/chi phí/tài nguyên.
> - [ ] Nêu rủi ro/safety.
> - [ ] Có phương án phân tầng hoặc fallback.
> - [ ] Không kết luận máy móc model lớn luôn tốt.

*Tags:* `model-selection`

#### 7. Giải thích cách huấn luyện một neural network nhỏ để phân loại câu hỏi theo chủ đề với khoảng 5000 mẫu. Ràng buộc: - Không dùng mạng sâu. - Cần giải thích forward pass, loss, backpropagation và cập nhật trọng số bằng ví dụ số nhỏ. Hãy trình bày: (1) flow huấn luyện; (2) một ví dụ cập nhật một trọng số; (3) cách phát hiện overfit.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E03-C10`, `N26E13-C11`

> [!example]- Đáp án mẫu
> Forward pass tạo dự đoán, loss đo sai số, backprop dùng chain rule để tính gradient, sau đó gradient descent cập nhật w_new=w-η×grad.
> Có thể minh họa với một nơ-ron tuyến tính và số nhỏ.
> Chia train/validation/test, theo dõi train loss và validation loss; nếu train tiếp tục tốt lên nhưng validation xấu đi thì có dấu hiệu overfit.
> So sánh với baseline đơn giản trước khi chọn mạng.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích đúng forward/loss/backprop/update.
> - [ ] Có ví dụ cập nhật số nhỏ.
> - [ ] Có train/validation/test.
> - [ ] Nhận biết overfit.
> - [ ] Có baseline để so sánh.

*Tags:* `backpropagation` `neural-network` `essay`

#### 8. Một classifier dùng để phân loại câu hỏi theo chủ đề được kiểm tra trên 550 mẫu validation và hiện có TP=24, FP=6, FN=8, TN=42. Nhóm cân nhắc hạ threshold để bắt được nhiều ca dương tính hơn. Ràng buộc: - Bỏ sót dương tính gây hậu quả lớn hơn một cảnh báo nhầm. - Không được chỉ nhìn accuracy. Hãy giải thích: (1) precision và recall sẽ thường thay đổi theo hướng nào; (2) metric nên ưu tiên; (3) cách chọn threshold bằng validation.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E03-C12`, `N26E08-C12`

> [!example]- Đáp án mẫu
> Khi hạ threshold, thường có nhiều dự đoán dương hơn: recall có xu hướng tăng nhưng precision có thể giảm vì FP tăng.
> Vì FN gây hậu quả lớn hơn, recall nên được ưu tiên, nhưng vẫn theo dõi precision/F1 để tránh quá nhiều cảnh báo nhầm.
> Thử một số threshold trên validation và chọn theo tiêu chí đã thống nhất; test chỉ dùng đánh giá cuối.

> [!check]- Rubric chấm (5 ý)
> - [ ] Hiểu trade-off precision/recall.
> - [ ] Chọn metric theo hậu quả FN.
> - [ ] Không chỉ dùng accuracy.
> - [ ] Chọn threshold trên validation.
> - [ ] Giữ test cho đánh giá cuối.

*Tags:* `confusion-matrix` `threshold` `essay`

#### 9. Bạn có 6000 mẫu để phân loại lỗi mức thấp hay mức cao và cần chọn giữa logistic regression, SVM tuyến tính và neural network nhỏ. Ràng buộc: - MVP trong 3 tuần. - Kết quả cần tương đối dễ giải thích. - Hai lớp hơi lệch. Hãy nêu: (1) baseline nên thử trước; (2) thứ tự thử các mô hình tiếp theo; (3) tiêu chí để quyết định.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E05-C12`, `N26E10-C11`

> [!example]- Đáp án mẫu
> Nên bắt đầu logistic regression vì nhanh và dễ giải thích.
> Có thể thử SVM tuyến tính tiếp nếu dữ liệu phù hợp; neural network nhỏ chỉ nên thử khi baseline chưa đạt và có lý do rõ.
> Dùng train/validation/test, confusion matrix, precision, recall, F1, latency và độ đơn giản để so sánh.
> Chọn mô hình theo ràng buộc chứ không mặc định mô hình phức tạp hơn là tốt hơn.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có baseline hợp lý.
> - [ ] Có thứ tự thử mô hình.
> - [ ] Có metric cho lệch lớp.
> - [ ] Có xét latency/độ phức tạp.
> - [ ] Lập luận theo ràng buộc.

*Tags:* `model-selection` `essay`

#### 10. Xây dựng SVM tuyến tính cho bài toán phân loại ticket lỗi hay câu hỏi sử dụng. Ràng buộc: - Có khoảng 4500 mẫu đã gắn nhãn và số đặc trưng không lớn. - Cần so sánh với logistic regression. - Không yêu cầu kernel nâng cao. Hãy trình bày: (1) ý nghĩa margin và support vectors; (2) các bước train/evaluate; (3) khi nào giữ SVM hoặc quay về baseline.
**8 điểm** · Module C · `L3-L4` · `N26E02-C11` (Khóa mới 2026 · Đề 02)

> [!example]- Đáp án mẫu
> SVM tuyến tính tìm ranh giới có margin lớn; support vectors là các mẫu gần biên và ảnh hưởng mạnh đến ranh giới.
> Chuẩn hóa đặc trưng khi cần, chia train/validation/test, thử C ở mức cơ bản trên validation rồi đánh giá confusion matrix, precision, recall và F1 trên test.
> So sánh với logistic regression về chất lượng, tốc độ và khả năng giải thích; chỉ giữ SVM nếu có lợi ích rõ.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích margin đúng.
> - [ ] Giải thích support vectors đúng.
> - [ ] Có train/validation/test.
> - [ ] Có metric phù hợp.
> - [ ] Có so sánh với baseline.

*Tags:* `svm` `classification` `essay`

#### 11. Bạn có 5000 mẫu để phân loại câu hỏi theo chủ đề và cần chọn giữa logistic regression, SVM tuyến tính và neural network nhỏ. Ràng buộc: - MVP trong 3 tuần. - Kết quả cần tương đối dễ giải thích. - Hai lớp hơi lệch. Hãy nêu: (1) baseline nên thử trước; (2) thứ tự thử các mô hình tiếp theo; (3) tiêu chí để quyết định.
**8 điểm** · Module C · `L3-L4` · `N26E03-C11` (Khóa mới 2026 · Đề 03)

> [!example]- Đáp án mẫu
> Nên bắt đầu logistic regression vì nhanh và dễ giải thích.
> Có thể thử SVM tuyến tính tiếp nếu dữ liệu phù hợp; neural network nhỏ chỉ nên thử khi baseline chưa đạt và có lý do rõ.
> Dùng train/validation/test, confusion matrix, precision, recall, F1, latency và độ đơn giản để so sánh.
> Chọn mô hình theo ràng buộc chứ không mặc định mô hình phức tạp hơn là tốt hơn.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có baseline hợp lý.
> - [ ] Có thứ tự thử mô hình.
> - [ ] Có metric cho lệch lớp.
> - [ ] Có xét latency/độ phức tạp.
> - [ ] Lập luận theo ràng buộc.

*Tags:* `model-selection` `essay`

#### 12. Một classifier dùng để phân loại phản hồi tích cực hay tiêu cực được kiểm tra trên 600 mẫu validation và hiện có TP=40, FP=10, FN=20, TN=30. Nhóm cân nhắc hạ threshold để bắt được nhiều ca dương tính hơn. Ràng buộc: - Bỏ sót dương tính gây hậu quả lớn hơn một cảnh báo nhầm. - Không được chỉ nhìn accuracy. Hãy giải thích: (1) precision và recall sẽ thường thay đổi theo hướng nào; (2) metric nên ưu tiên; (3) cách chọn threshold bằng validation.
**8 điểm** · Module C · `L3-L4` · `N26E04-C11` (Khóa mới 2026 · Đề 04)

> [!example]- Đáp án mẫu
> Khi hạ threshold, thường có nhiều dự đoán dương hơn: recall có xu hướng tăng nhưng precision có thể giảm vì FP tăng.
> Vì FN gây hậu quả lớn hơn, recall nên được ưu tiên, nhưng vẫn theo dõi precision/F1 để tránh quá nhiều cảnh báo nhầm.
> Thử một số threshold trên validation và chọn theo tiêu chí đã thống nhất; test chỉ dùng đánh giá cuối.

> [!check]- Rubric chấm (5 ý)
> - [ ] Hiểu trade-off precision/recall.
> - [ ] Chọn metric theo hậu quả FN.
> - [ ] Không chỉ dùng accuracy.
> - [ ] Chọn threshold trên validation.
> - [ ] Giữ test cho đánh giá cuối.

*Tags:* `confusion-matrix` `threshold` `essay`

#### 13. Xây dựng SVM tuyến tính cho bài toán phân loại yêu cầu hỗ trợ khẩn cấp hay thông thường. Ràng buộc: - Có khoảng 6500 mẫu đã gắn nhãn và số đặc trưng không lớn. - Cần so sánh với logistic regression. - Không yêu cầu kernel nâng cao. Hãy trình bày: (1) ý nghĩa margin và support vectors; (2) các bước train/evaluate; (3) khi nào giữ SVM hoặc quay về baseline.
**8 điểm** · Module C · `L3-L4` · `N26E06-C11` (Khóa mới 2026 · Đề 06)

> [!example]- Đáp án mẫu
> SVM tuyến tính tìm ranh giới có margin lớn; support vectors là các mẫu gần biên và ảnh hưởng mạnh đến ranh giới.
> Chuẩn hóa đặc trưng khi cần, chia train/validation/test, thử C ở mức cơ bản trên validation rồi đánh giá confusion matrix, precision, recall và F1 trên test.
> So sánh với logistic regression về chất lượng, tốc độ và khả năng giải thích; chỉ giữ SVM nếu có lợi ích rõ.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích margin đúng.
> - [ ] Giải thích support vectors đúng.
> - [ ] Có train/validation/test.
> - [ ] Có metric phù hợp.
> - [ ] Có so sánh với baseline.

*Tags:* `svm` `classification` `essay`

#### 14. Giải thích cách huấn luyện một neural network nhỏ để phân loại ticket lỗi hay câu hỏi sử dụng với khoảng 7000 mẫu. Ràng buộc: - Không dùng mạng sâu. - Cần giải thích forward pass, loss, backpropagation và cập nhật trọng số bằng ví dụ số nhỏ. Hãy trình bày: (1) flow huấn luyện; (2) một ví dụ cập nhật một trọng số; (3) cách phát hiện overfit.
**8 điểm** · Module C · `L3-L4` · `N26E07-C11` (Khóa mới 2026 · Đề 07)

> [!example]- Đáp án mẫu
> Forward pass tạo dự đoán, loss đo sai số, backprop dùng chain rule để tính gradient, sau đó gradient descent cập nhật w_new=w-η×grad.
> Có thể minh họa với một nơ-ron tuyến tính và số nhỏ.
> Chia train/validation/test, theo dõi train loss và validation loss; nếu train tiếp tục tốt lên nhưng validation xấu đi thì có dấu hiệu overfit.
> So sánh với baseline đơn giản trước khi chọn mạng.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích đúng forward/loss/backprop/update.
> - [ ] Có ví dụ cập nhật số nhỏ.
> - [ ] Có train/validation/test.
> - [ ] Nhận biết overfit.
> - [ ] Có baseline để so sánh.

*Tags:* `backpropagation` `neural-network` `essay`

#### 15. Xây dựng SVM tuyến tính cho bài toán phân loại câu hỏi theo chủ đề. Ràng buộc: - Có khoảng 7500 mẫu đã gắn nhãn và số đặc trưng không lớn. - Cần so sánh với logistic regression. - Không yêu cầu kernel nâng cao. Hãy trình bày: (1) ý nghĩa margin và support vectors; (2) các bước train/evaluate; (3) khi nào giữ SVM hoặc quay về baseline.
**8 điểm** · Module C · `L3-L4` · `N26E08-C11` (Khóa mới 2026 · Đề 08)

> [!example]- Đáp án mẫu
> SVM tuyến tính tìm ranh giới có margin lớn; support vectors là các mẫu gần biên và ảnh hưởng mạnh đến ranh giới.
> Chuẩn hóa đặc trưng khi cần, chia train/validation/test, thử C ở mức cơ bản trên validation rồi đánh giá confusion matrix, precision, recall và F1 trên test.
> So sánh với logistic regression về chất lượng, tốc độ và khả năng giải thích; chỉ giữ SVM nếu có lợi ích rõ.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích margin đúng.
> - [ ] Giải thích support vectors đúng.
> - [ ] Có train/validation/test.
> - [ ] Có metric phù hợp.
> - [ ] Có so sánh với baseline.

*Tags:* `svm` `classification` `essay`

#### 16. Giải thích cách huấn luyện một neural network nhỏ để phân loại phản hồi tích cực hay tiêu cực với khoảng 8000 mẫu. Ràng buộc: - Không dùng mạng sâu. - Cần giải thích forward pass, loss, backpropagation và cập nhật trọng số bằng ví dụ số nhỏ. Hãy trình bày: (1) flow huấn luyện; (2) một ví dụ cập nhật một trọng số; (3) cách phát hiện overfit.
**8 điểm** · Module C · `L3-L4` · `N26E09-C11` (Khóa mới 2026 · Đề 09)

> [!example]- Đáp án mẫu
> Forward pass tạo dự đoán, loss đo sai số, backprop dùng chain rule để tính gradient, sau đó gradient descent cập nhật w_new=w-η×grad.
> Có thể minh họa với một nơ-ron tuyến tính và số nhỏ.
> Chia train/validation/test, theo dõi train loss và validation loss; nếu train tiếp tục tốt lên nhưng validation xấu đi thì có dấu hiệu overfit.
> So sánh với baseline đơn giản trước khi chọn mạng.

> [!check]- Rubric chấm (5 ý)
> - [ ] Giải thích đúng forward/loss/backprop/update.
> - [ ] Có ví dụ cập nhật số nhỏ.
> - [ ] Có train/validation/test.
> - [ ] Nhận biết overfit.
> - [ ] Có baseline để so sánh.

*Tags:* `backpropagation` `neural-network` `essay`

---

### Đánh giá mô hình: metric, confusion matrix, overfitting

#### 17. Xây dựng một mô hình phân loại để phân loại yêu cầu hỗ trợ khẩn cấp hay thông thường. Ràng buộc: - Có khoảng 4000 mẫu đã gắn nhãn. - Hai lớp hơi lệch. - Kết quả thử nghiệm có TP=36, FP=4, FN=9, TN=51. Hãy: (1) chọn một baseline dễ hiểu; (2) giải thích accuracy, precision, recall, F1 và metric nên ưu tiên; (3) nêu cách đưa mô hình vào thử nghiệm.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E01-C12`, `N26E11-C11`

> [!example]- Đáp án mẫu
> Có thể bắt đầu bằng logistic regression hoặc cây quyết định nhỏ.
> Chia train/validation/test và giữ test cho đánh giá cuối.
> Từ confusion matrix tính accuracy, precision=TP/(TP+FP), recall=TP/(TP+FN), F1 là trung bình điều hòa precision/recall.
> Nếu bỏ sót lớp dương tính nguy hiểm thì ưu tiên recall hơn accuracy.
> Khi thử nghiệm, đóng gói preprocessing + model thành API đơn giản và theo dõi metric trên dữ liệu mới.

> [!check]- Rubric chấm (5 ý)
> - [ ] Chọn baseline hợp lý.
> - [ ] Chia dữ liệu đúng.
> - [ ] Giải thích đúng bốn metric.
> - [ ] Chọn metric theo hậu quả FP/FN.
> - [ ] Có cách triển khai thử cơ bản.

*Tags:* `classification` `confusion-matrix` `essay`

#### 18. Mô hình dùng để phân loại phản hồi tích cực hay tiêu cực đạt train accuracy 95% nhưng validation accuracy 72%; recall lớp dương tính chỉ 55%. Ràng buộc: - Chưa thể thu thêm dữ liệu trong 2 tuần. - Phải giữ baseline để so sánh. Hãy: (1) nêu các nguyên nhân có thể; (2) nêu ba kiểm tra nên làm; (3) đề xuất vài cách cải thiện đơn giản mà không dùng test để tune.
**8 điểm** · Module C · `L3-L4` · `N26E04-C10` (Khóa mới 2026 · Đề 04)

> [!example]- Đáp án mẫu
> Có thể do overfit, leakage, chia tập không phù hợp, lớp lệch hoặc threshold chưa hợp lý.
> Kiểm tra trùng lặp/leakage giữa train-validation, phân phối lớp và confusion matrix/learning curve.
> Có thể thử regularization, mô hình đơn giản hơn, class weight hoặc điều chỉnh threshold trên validation.
> Test chỉ dùng đánh giá cuối và baseline phải được giữ để so sánh.

> [!check]- Rubric chấm (5 ý)
> - [ ] Nêu được overfit/leakage/lệch lớp.
> - [ ] Có kiểm tra cụ thể.
> - [ ] Không dùng test để tune.
> - [ ] Có biện pháp cải thiện đơn giản.
> - [ ] Giữ baseline để so sánh.

*Tags:* `overfitting` `evaluation` `essay`

#### 19. Mô hình dùng để phân loại yêu cầu hỗ trợ khẩn cấp hay thông thường đạt train accuracy 97% nhưng validation accuracy 74%; recall lớp dương tính chỉ 58%. Ràng buộc: - Chưa thể thu thêm dữ liệu trong 2 tuần. - Phải giữ baseline để so sánh. Hãy: (1) nêu các nguyên nhân có thể; (2) nêu ba kiểm tra nên làm; (3) đề xuất vài cách cải thiện đơn giản mà không dùng test để tune.
**8 điểm** · Module C · `L3-L4` · `N26E06-C12` (Khóa mới 2026 · Đề 06)

> [!example]- Đáp án mẫu
> Có thể do overfit, leakage, chia tập không phù hợp, lớp lệch hoặc threshold chưa hợp lý.
> Kiểm tra trùng lặp/leakage giữa train-validation, phân phối lớp và confusion matrix/learning curve.
> Có thể thử regularization, mô hình đơn giản hơn, class weight hoặc điều chỉnh threshold trên validation.
> Test chỉ dùng đánh giá cuối và baseline phải được giữ để so sánh.

> [!check]- Rubric chấm (5 ý)
> - [ ] Nêu được overfit/leakage/lệch lớp.
> - [ ] Có kiểm tra cụ thể.
> - [ ] Không dùng test để tune.
> - [ ] Có biện pháp cải thiện đơn giản.
> - [ ] Giữ baseline để so sánh.

*Tags:* `overfitting` `evaluation` `essay`

#### 20. Xây dựng một mô hình phân loại để phân loại ticket lỗi hay câu hỏi sử dụng. Ràng buộc: - Có khoảng 7000 mẫu đã gắn nhãn. - Hai lớp hơi lệch. - Kết quả thử nghiệm có TP=30, FP=10, FN=5, TN=55. Hãy: (1) chọn một baseline dễ hiểu; (2) giải thích accuracy, precision, recall, F1 và metric nên ưu tiên; (3) nêu cách đưa mô hình vào thử nghiệm.
**8 điểm** · Module C · `L3-L4` · `N26E07-C10` (Khóa mới 2026 · Đề 07)

> [!example]- Đáp án mẫu
> Có thể bắt đầu bằng logistic regression hoặc cây quyết định nhỏ.
> Chia train/validation/test và giữ test cho đánh giá cuối.
> Từ confusion matrix tính accuracy, precision=TP/(TP+FP), recall=TP/(TP+FN), F1 là trung bình điều hòa precision/recall.
> Nếu bỏ sót lớp dương tính nguy hiểm thì ưu tiên recall hơn accuracy.
> Khi thử nghiệm, đóng gói preprocessing + model thành API đơn giản và theo dõi metric trên dữ liệu mới.

> [!check]- Rubric chấm (5 ý)
> - [ ] Chọn baseline hợp lý.
> - [ ] Chia dữ liệu đúng.
> - [ ] Giải thích đúng bốn metric.
> - [ ] Chọn metric theo hậu quả FP/FN.
> - [ ] Có cách triển khai thử cơ bản.

*Tags:* `classification` `confusion-matrix` `essay`

#### 21. Xây dựng một mô hình phân loại để phân loại lỗi mức thấp hay mức cao. Ràng buộc: - Có khoảng 8500 mẫu đã gắn nhãn. - Hai lớp hơi lệch. - Kết quả thử nghiệm có TP=18, FP=2, FN=6, TN=24. Hãy: (1) chọn một baseline dễ hiểu; (2) giải thích accuracy, precision, recall, F1 và metric nên ưu tiên; (3) nêu cách đưa mô hình vào thử nghiệm.
**8 điểm** · Module C · `L3-L4` · `N26E10-C10` (Khóa mới 2026 · Đề 10)

> [!example]- Đáp án mẫu
> Có thể bắt đầu bằng logistic regression hoặc cây quyết định nhỏ.
> Chia train/validation/test và giữ test cho đánh giá cuối.
> Từ confusion matrix tính accuracy, precision=TP/(TP+FP), recall=TP/(TP+FN), F1 là trung bình điều hòa precision/recall.
> Nếu bỏ sót lớp dương tính nguy hiểm thì ưu tiên recall hơn accuracy.
> Khi thử nghiệm, đóng gói preprocessing + model thành API đơn giản và theo dõi metric trên dữ liệu mới.

> [!check]- Rubric chấm (5 ý)
> - [ ] Chọn baseline hợp lý.
> - [ ] Chia dữ liệu đúng.
> - [ ] Giải thích đúng bốn metric.
> - [ ] Chọn metric theo hậu quả FP/FN.
> - [ ] Có cách triển khai thử cơ bản.

*Tags:* `classification` `confusion-matrix` `essay`

#### 22. Một hệ thống RAG dùng tài liệu kỹ thuật cơ bản trả lời trôi chảy nhưng đôi lúc lấy sai đoạn hoặc ghi sai nguồn. Ràng buộc: - Kho chỉ khoảng 8500 đoạn/tài liệu. - Chưa cần tối ưu hạ tầng phức tạp. Hãy nêu: (1) cách tách lỗi retrieval và lỗi generation; (2) một bộ test nhỏ nên có gì; (3) ba chỉ số/tiêu chí chất lượng nên theo dõi.
**8 điểm** · Module C · `L3-L4` · `N26E10-C12` (Khóa mới 2026 · Đề 10)

> [!example]- Đáp án mẫu
> Tạo bộ câu hỏi có tài liệu đúng đã biết.
> Trước tiên kiểm tra retrieval có đưa đúng đoạn vào top-k hay không; nếu retrieval đúng mà câu trả lời vẫn sai thì lỗi nằm nhiều hơn ở generation/prompt.
> Bộ test nên có câu dễ, câu không có đáp án và câu cần citation.
> Có thể theo dõi retrieval hit-rate, mức bám nguồn/correctness, citation đúng, tỷ lệ abstain đúng và latency.

> [!check]- Rubric chấm (5 ý)
> - [ ] Tách được retrieval và generation.
> - [ ] Có bộ câu hỏi chuẩn nhỏ.
> - [ ] Có kiểm tra câu không đủ nguồn.
> - [ ] Có tiêu chí citation/groundedness.
> - [ ] Có metric retrieval cơ bản.

*Tags:* `rag` `evaluation` `essay`

#### 23. Một hệ thống RAG dùng quy trình nội bộ công ty trả lời trôi chảy nhưng đôi lúc lấy sai đoạn hoặc ghi sai nguồn. Ràng buộc: - Kho chỉ khoảng 9500 đoạn/tài liệu. - Chưa cần tối ưu hạ tầng phức tạp. Hãy nêu: (1) cách tách lỗi retrieval và lỗi generation; (2) một bộ test nhỏ nên có gì; (3) ba chỉ số/tiêu chí chất lượng nên theo dõi.
**8 điểm** · Module C · `L3-L4` · `N26E12-C11` (Khóa mới 2026 · Đề 12)

> [!tip] Gợi ý
> - Tách hai câu hỏi: hệ thống có tìm đúng đoạn không, và có trả đúng theo đoạn đó không.
> - Chuẩn bị một bộ câu hỏi mẫu cùng nguồn đúng để đối chiếu.
> - Nêu metric đơn giản cho retrieval, citation và câu trả lời.

> [!example]- Đáp án mẫu
> Tạo bộ câu hỏi có tài liệu đúng đã biết.
> Trước tiên kiểm tra retrieval có đưa đúng đoạn vào top-k hay không; nếu retrieval đúng mà câu trả lời vẫn sai thì lỗi nằm nhiều hơn ở generation/prompt.
> Bộ test nên có câu dễ, câu không có đáp án và câu cần citation.
> Có thể theo dõi retrieval hit-rate, mức bám nguồn/correctness, citation đúng, tỷ lệ abstain đúng và latency.
> Ví dụ dễ hiểu: câu hỏi về hạn nộp hồ sơ phải lấy đúng đoạn ghi ngày 30/9; nếu đoạn không vào top-k là lỗi retrieval, còn có đoạn đúng nhưng trả sai là lỗi generation.

> [!check]- Rubric chấm (5 ý)
> - [ ] Tách được retrieval và generation.
> - [ ] Có bộ câu hỏi chuẩn nhỏ.
> - [ ] Có kiểm tra câu không đủ nguồn.
> - [ ] Có tiêu chí citation/groundedness.
> - [ ] Có metric retrieval cơ bản.

*Tags:* `rag` `evaluation` `essay`

#### 24. Mô hình dùng để phân loại câu hỏi theo chủ đề đạt train accuracy 98% nhưng validation accuracy 79%; recall lớp dương tính chỉ 63%. Ràng buộc: - Chưa thể thu thêm dữ liệu trong 2 tuần. - Phải giữ baseline để so sánh. Hãy: (1) nêu các nguyên nhân có thể; (2) nêu ba kiểm tra nên làm; (3) đề xuất vài cách cải thiện đơn giản mà không dùng test để tune.
**8 điểm** · Module C · `L3-L4` · `N26E13-C10` (Khóa mới 2026 · Đề 13)

> [!tip] Gợi ý
> - Train cao nhưng validation thấp thường gợi ý overfit, leakage hoặc split chưa đúng.
> - Giữ test riêng; chỉ thử thay đổi trên train/validation.
> - Đề xuất một thay đổi nhỏ rồi nêu cách so với baseline.

> [!example]- Đáp án mẫu
> Có thể do overfit, leakage, chia tập không phù hợp, lớp lệch hoặc threshold chưa hợp lý.
> Kiểm tra trùng lặp/leakage giữa train-validation, phân phối lớp và confusion matrix/learning curve.
> Có thể thử regularization, mô hình đơn giản hơn, class weight hoặc điều chỉnh threshold trên validation.
> Test chỉ dùng đánh giá cuối và baseline phải được giữ để so sánh.
> Ví dụ dễ hiểu: giảm độ sâu cây hoặc tăng regularization rồi so validation recall/F1 với baseline, thay vì đổi mô hình liên tục mà không đo.

> [!check]- Rubric chấm (5 ý)
> - [ ] Nêu được overfit/leakage/lệch lớp.
> - [ ] Có kiểm tra cụ thể.
> - [ ] Không dùng test để tune.
> - [ ] Có biện pháp cải thiện đơn giản.
> - [ ] Giữ baseline để so sánh.

*Tags:* `overfitting` `evaluation` `essay`

---

### RAG, retrieval & chống bịa đặt

#### 25. Thiết kế pipeline RAG cho chatbot hỏi đáp tài liệu nội bộ. Nêu các bước chính và cách giảm hallucination.
**4 điểm** · Module C · 🔁 **xuất hiện 4 lần** (chỉ khác số liệu): `E02-C19`, `E05-C20`, `E07-C19`, `E10-C20`

> [!example]- Đáp án mẫu
> Pipeline: ingest tài liệu, làm sạch/chunking, tạo embedding, lưu vector DB, retrieve theo câu hỏi, có thể rerank, đưa context vào LLM, sinh câu trả lời kèm nguồn, log feedback.
> Giảm hallucination bằng yêu cầu trả lời theo nguồn, hiển thị citation, từ chối khi không đủ context, đánh giá bộ câu hỏi chuẩn và human review giai đoạn đầu.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có ingest/chunk/embed/store.
> - [ ] Có retrieve/rerank/generate.
> - [ ] Có citation hoặc grounding.
> - [ ] Có cách xử lý khi không đủ nguồn.
> - [ ] Có đánh giá/monitoring.

*Tags:* `rag`

#### 26. Thiết kế một trợ lý RAG cho học viên tra cứu tài liệu học tập nội bộ. Ràng buộc: - Khoảng 4000 tài liệu/đoạn tài liệu. - nhóm A và nhóm B có quyền xem khác nhau. - Câu trả lời phải có nguồn. - Có 4 tuần làm bản thử nghiệm. Hãy nêu: (1) pipeline chính; (2) một ví dụ hỏi–đáp; (3) cách kiểm thử trước khi cho dùng thử.
**8 điểm** · Module C · `L3-L4` · `N26E01-C10` (Khóa mới 2026 · Đề 01)

> [!example]- Đáp án mẫu
> Pipeline cơ bản gồm làm sạch tài liệu, chia đoạn, gắn metadata nguồn/quyền, tạo embedding, lập chỉ mục và retrieval.
> Khi có câu hỏi, hệ thống xác thực người dùng, lọc quyền trước retrieval rồi mới đưa đoạn phù hợp vào prompt.
> Câu trả lời phải bám nguồn và nói chưa đủ thông tin khi không có bằng chứng.
> Ví dụ người thuộc nhóm A chỉ nhận tài liệu của A.
> Kiểm thử bằng câu hỏi mẫu, kiểm tra citation, quyền A/B, độ đúng retrieval và thời gian phản hồi.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có ingestion/chunking/embedding/retrieval/generation.
> - [ ] Lọc quyền trước retrieval.
> - [ ] Có ví dụ end-to-end.
> - [ ] Có citation/abstain khi thiếu nguồn.
> - [ ] Có kế hoạch kiểm thử cơ bản.

*Tags:* `rag` `access-control` `essay`

#### 27. Thiết kế một trợ lý RAG cho thành viên dự án tra cứu tài liệu kỹ thuật cơ bản. Ràng buộc: - Khoảng 6000 tài liệu/đoạn tài liệu. - nhóm A và nhóm B có quyền xem khác nhau. - Câu trả lời phải có nguồn. - Có 4 tuần làm bản thử nghiệm. Hãy nêu: (1) pipeline chính; (2) một ví dụ hỏi–đáp; (3) cách kiểm thử trước khi cho dùng thử.
**8 điểm** · Module C · `L3-L4` · `N26E05-C10` (Khóa mới 2026 · Đề 05)

> [!example]- Đáp án mẫu
> Pipeline cơ bản gồm làm sạch tài liệu, chia đoạn, gắn metadata nguồn/quyền, tạo embedding, lập chỉ mục và retrieval.
> Khi có câu hỏi, hệ thống xác thực người dùng, lọc quyền trước retrieval rồi mới đưa đoạn phù hợp vào prompt.
> Câu trả lời phải bám nguồn và nói chưa đủ thông tin khi không có bằng chứng.
> Ví dụ người thuộc nhóm A chỉ nhận tài liệu của A.
> Kiểm thử bằng câu hỏi mẫu, kiểm tra citation, quyền A/B, độ đúng retrieval và thời gian phản hồi.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có ingestion/chunking/embedding/retrieval/generation.
> - [ ] Lọc quyền trước retrieval.
> - [ ] Có ví dụ end-to-end.
> - [ ] Có citation/abstain khi thiếu nguồn.
> - [ ] Có kế hoạch kiểm thử cơ bản.

*Tags:* `rag` `access-control` `essay`

#### 28. Thiết kế một trợ lý RAG cho bạn đọc tra cứu tài liệu thư viện. Ràng buộc: - Khoảng 7500 tài liệu/đoạn tài liệu. - đội A và đội B có quyền xem khác nhau. - Câu trả lời phải có nguồn. - Có 4 tuần làm bản thử nghiệm. Hãy nêu: (1) pipeline chính; (2) một ví dụ hỏi–đáp; (3) cách kiểm thử trước khi cho dùng thử.
**8 điểm** · Module C · `L3-L4` · `N26E08-C10` (Khóa mới 2026 · Đề 08)

> [!example]- Đáp án mẫu
> Pipeline cơ bản gồm làm sạch tài liệu, chia đoạn, gắn metadata nguồn/quyền, tạo embedding, lập chỉ mục và retrieval.
> Khi có câu hỏi, hệ thống xác thực người dùng, lọc quyền trước retrieval rồi mới đưa đoạn phù hợp vào prompt.
> Câu trả lời phải bám nguồn và nói chưa đủ thông tin khi không có bằng chứng.
> Ví dụ người thuộc đội A chỉ nhận tài liệu của A.
> Kiểm thử bằng câu hỏi mẫu, kiểm tra citation, quyền A/B, độ đúng retrieval và thời gian phản hồi.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có ingestion/chunking/embedding/retrieval/generation.
> - [ ] Lọc quyền trước retrieval.
> - [ ] Có ví dụ end-to-end.
> - [ ] Có citation/abstain khi thiếu nguồn.
> - [ ] Có kế hoạch kiểm thử cơ bản.

*Tags:* `rag` `access-control` `essay`

#### 29. Thiết kế một trợ lý RAG cho nhân viên tra cứu quy trình nội bộ công ty. Ràng buộc: - Khoảng 9500 tài liệu/đoạn tài liệu. - phòng A và phòng B có quyền xem khác nhau. - Câu trả lời phải có nguồn. - Có 4 tuần làm bản thử nghiệm. Hãy nêu: (1) pipeline chính; (2) một ví dụ hỏi–đáp; (3) cách kiểm thử trước khi cho dùng thử.
**8 điểm** · Module C · `L3-L4` · `N26E12-C12` (Khóa mới 2026 · Đề 12)

> [!tip] Gợi ý
> - Nhớ chuỗi ingestion → chunking → embedding → retrieval → generation.
> - Lọc quyền trước khi đoạn tài liệu được đưa vào prompt.
> - Cho một ví dụ hỏi–đáp có citation và trường hợp thiếu nguồn.

> [!example]- Đáp án mẫu
> Pipeline cơ bản gồm làm sạch tài liệu, chia đoạn, gắn metadata nguồn/quyền, tạo embedding, lập chỉ mục và retrieval.
> Khi có câu hỏi, hệ thống xác thực người dùng, lọc quyền trước retrieval rồi mới đưa đoạn phù hợp vào prompt.
> Câu trả lời phải bám nguồn và nói chưa đủ thông tin khi không có bằng chứng.
> Ví dụ người thuộc phòng A chỉ nhận tài liệu của A.
> Kiểm thử bằng câu hỏi mẫu, kiểm tra citation, quyền A/B, độ đúng retrieval và thời gian phản hồi.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có ingestion/chunking/embedding/retrieval/generation.
> - [ ] Lọc quyền trước retrieval.
> - [ ] Có ví dụ end-to-end.
> - [ ] Có citation/abstain khi thiếu nguồn.
> - [ ] Có kế hoạch kiểm thử cơ bản.

*Tags:* `rag` `access-control` `essay`

---

### Dữ liệu & tiền xử lý

#### 30. Bạn nhận một bộ dữ liệu 4500 mẫu đã gắn nhãn để phân loại ticket lỗi hay câu hỏi sử dụng. Ràng buộc: - Có một số bản ghi gần trùng nhau. - Một vài cột được tạo sau khi kết quả thực tế đã xảy ra. - Cần báo cáo kết quả đáng tin cậy. Hãy nêu: (1) cách chia train/validation/test; (2) data leakage có thể xuất hiện ở đâu; (3) cách kiểm tra pipeline trước khi train.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E02-C12`, `N26E07-C12`

> [!example]- Đáp án mẫu
> Loại hoặc gom các bản ghi gần trùng để không rơi vào nhiều tập khác nhau.
> Các cột chỉ xuất hiện sau thời điểm dự đoán phải bị loại khỏi feature vì gây leakage.
> Fit preprocessing chỉ trên train rồi áp dụng cho validation/test.
> Dùng validation để chọn mô hình và giữ test cho đánh giá cuối.
> Kiểm tra schema, missing values, tỷ lệ lớp và một vài mẫu bằng tay trước khi train.

> [!check]- Rubric chấm (5 ý)
> - [ ] Chia train/validation/test đúng vai trò.
> - [ ] Nhận ra leakage từ cột hậu nghiệm.
> - [ ] Xử lý bản ghi trùng hợp lý.
> - [ ] Fit preprocessing trên train.
> - [ ] Có kiểm tra dữ liệu cơ bản.

*Tags:* `data-preparation` `leakage` `essay`

#### 31. Mô hình để phân loại phản hồi tích cực hay tiêu cực chạy đúng trong notebook nhưng API xử lý khoảng 80 request/phút lại cho nhiều dự đoán sai bất thường. Ràng buộc: - API vẫn trả HTTP 200. - Một số trường JSON có kiểu dữ liệu khác lúc train. - Có khả năng preprocessing ở API không giống notebook. Hãy nêu: (1) thứ tự debug; (2) một ví dụ lỗi preprocessing/schema; (3) cách ngăn lỗi tương tự khi deploy lại.
**8 điểm** · Module C · `L3-L4` · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `N26E04-C12`, `N26E09-C12`

> [!example]- Đáp án mẫu
> So sánh cùng một input qua notebook và API, kiểm tra schema/kiểu dữ liệu, thứ tự feature, missing value, chuẩn hóa và version model.
> Ví dụ lúc train tuổi là số nhưng API nhận chuỗi, hoặc scaler không được dùng giống lúc train.
> Đóng gói preprocessing cùng model, validate schema, viết test với các input cố định và trả model_version để đối chiếu.

> [!check]- Rubric chấm (5 ý)
> - [ ] Debug từ input/schema đến preprocessing/model.
> - [ ] Có ví dụ lỗi cụ thể.
> - [ ] Kiểm tra feature order/type.
> - [ ] Đóng gói preprocessing nhất quán.
> - [ ] Có regression test/model version.

*Tags:* `api` `debugging` `preprocessing` `essay`

#### 32. Mô hình để phân loại yêu cầu hỗ trợ khẩn cấp hay thông thường chạy đúng trong notebook nhưng API xử lý khoảng 150 request/phút lại cho nhiều dự đoán sai bất thường. Ràng buộc: - API vẫn trả HTTP 200. - Một số trường JSON có kiểu dữ liệu khác lúc train. - Có khả năng preprocessing ở API không giống notebook. Hãy nêu: (1) thứ tự debug; (2) một ví dụ lỗi preprocessing/schema; (3) cách ngăn lỗi tương tự khi deploy lại.
**8 điểm** · Module C · `L3-L4` · `N26E11-C10` (Khóa mới 2026 · Đề 11)

> [!tip] Gợi ý
> - So sánh schema, kiểu dữ liệu và thứ tự feature giữa notebook với API.
> - Kiểm tra bước điền thiếu, mã hóa và scaling có dùng cùng quy tắc không.
> - Nêu một input cụ thể bị sai và cách log tối thiểu để tìm lỗi.

> [!example]- Đáp án mẫu
> So sánh cùng một input qua notebook và API, kiểm tra schema/kiểu dữ liệu, thứ tự feature, missing value, chuẩn hóa và version model.
> Ví dụ lúc train tuổi là số nhưng API nhận chuỗi, hoặc scaler không được dùng giống lúc train.
> Đóng gói preprocessing cùng model, validate schema, viết test với các input cố định và trả model_version để đối chiếu.

> [!check]- Rubric chấm (5 ý)
> - [ ] Debug từ input/schema đến preprocessing/model.
> - [ ] Có ví dụ lỗi cụ thể.
> - [ ] Kiểm tra feature order/type.
> - [ ] Đóng gói preprocessing nhất quán.
> - [ ] Có regression test/model version.

*Tags:* `api` `debugging` `preprocessing` `essay`

#### 33. Mô hình để phân loại ticket lỗi hay câu hỏi sử dụng chạy đúng trong notebook nhưng API xử lý khoảng 160 request/phút lại cho nhiều dự đoán sai bất thường. Ràng buộc: - API vẫn trả HTTP 200. - Một số trường JSON có kiểu dữ liệu khác lúc train. - Có khả năng preprocessing ở API không giống notebook. Hãy nêu: (1) thứ tự debug; (2) một ví dụ lỗi preprocessing/schema; (3) cách ngăn lỗi tương tự khi deploy lại.
**8 điểm** · Module C · `L3-L4` · `N26E12-C10` (Khóa mới 2026 · Đề 12)

> [!tip] Gợi ý
> - So sánh schema, kiểu dữ liệu và thứ tự feature giữa notebook với API.
> - Kiểm tra bước điền thiếu, mã hóa và scaling có dùng cùng quy tắc không.
> - Nêu một input cụ thể bị sai và cách log tối thiểu để tìm lỗi.

> [!example]- Đáp án mẫu
> So sánh cùng một input qua notebook và API, kiểm tra schema/kiểu dữ liệu, thứ tự feature, missing value, chuẩn hóa và version model.
> Ví dụ lúc train tuổi là số nhưng API nhận chuỗi, hoặc scaler không được dùng giống lúc train.
> Đóng gói preprocessing cùng model, validate schema, viết test với các input cố định và trả model_version để đối chiếu.

> [!check]- Rubric chấm (5 ý)
> - [ ] Debug từ input/schema đến preprocessing/model.
> - [ ] Có ví dụ lỗi cụ thể.
> - [ ] Kiểm tra feature order/type.
> - [ ] Đóng gói preprocessing nhất quán.
> - [ ] Có regression test/model version.

*Tags:* `api` `debugging` `preprocessing` `essay`

---

### API, tích hợp & debug

#### 34. Một mô hình dùng để phân loại ticket lỗi hay câu hỏi sử dụng đã đạt kết quả chấp nhận được trên test. Hãy đưa nó thành API thử nghiệm cho nhân viên. Ràng buộc: - Input JSON có vài trường bắt buộc. - Phản hồi cần dưới 2 giây. - Không log dữ liệu nhạy cảm thô. - Nếu phiên bản mới kém hơn phải quay lại bản cũ. Hãy nêu: (1) flow request → prediction; (2) ví dụ request/response; (3) các kiểm tra trước và sau deploy.
**8 điểm** · Module C · `L3-L4` · `N26E02-C10` (Khóa mới 2026 · Đề 02)

> [!example]- Đáp án mẫu
> API nhận JSON, validate schema, chạy đúng preprocessing rồi gọi model và trả label/score/model_version.
> Ví dụ request chứa các đặc trưng cho phép, response có label và score.
> Trước deploy cần test preprocessing, schema, mẫu dự đoán chuẩn và latency.
> Sau deploy theo dõi error rate, latency và chất lượng khi có nhãn; giữ model version cũ để rollback.
> Không ghi raw PII vào log.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có schema validation.
> - [ ] Preprocessing nhất quán với lúc train.
> - [ ] Có ví dụ request/response.
> - [ ] Có test latency/chất lượng.
> - [ ] Có version và rollback.

*Tags:* `deployment` `api` `essay`

#### 35. Một mô hình dùng để phân loại lỗi mức thấp hay mức cao đã đạt kết quả chấp nhận được trên test. Hãy đưa nó thành API thử nghiệm cho thành viên dự án. Ràng buộc: - Input JSON có vài trường bắt buộc. - Phản hồi cần dưới 2 giây. - Không log dữ liệu nhạy cảm thô. - Nếu phiên bản mới kém hơn phải quay lại bản cũ. Hãy nêu: (1) flow request → prediction; (2) ví dụ request/response; (3) các kiểm tra trước và sau deploy.
**8 điểm** · Module C · `L3-L4` · `N26E05-C11` (Khóa mới 2026 · Đề 05)

> [!example]- Đáp án mẫu
> API nhận JSON, validate schema, chạy đúng preprocessing rồi gọi model và trả label/score/model_version.
> Ví dụ request chứa các đặc trưng cho phép, response có label và score.
> Trước deploy cần test preprocessing, schema, mẫu dự đoán chuẩn và latency.
> Sau deploy theo dõi error rate, latency và chất lượng khi có nhãn; giữ model version cũ để rollback.
> Không ghi raw PII vào log.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có schema validation.
> - [ ] Preprocessing nhất quán với lúc train.
> - [ ] Có ví dụ request/response.
> - [ ] Có test latency/chất lượng.
> - [ ] Có version và rollback.

*Tags:* `deployment` `api` `essay`

#### 36. Một mô hình dùng để phân loại yêu cầu hỗ trợ khẩn cấp hay thông thường đã đạt kết quả chấp nhận được trên test. Hãy đưa nó thành API thử nghiệm cho học viên. Ràng buộc: - Input JSON có vài trường bắt buộc. - Phản hồi cần dưới 2 giây. - Không log dữ liệu nhạy cảm thô. - Nếu phiên bản mới kém hơn phải quay lại bản cũ. Hãy nêu: (1) flow request → prediction; (2) ví dụ request/response; (3) các kiểm tra trước và sau deploy.
**8 điểm** · Module C · `L3-L4` · `N26E11-C12` (Khóa mới 2026 · Đề 11)

> [!tip] Gợi ý
> - Nêu flow JSON input → validation → preprocessing → model → response.
> - Response nên có label, score và model_version.
> - Đừng quên test, latency, log an toàn và cách quay lại bản cũ.

> [!example]- Đáp án mẫu
> API nhận JSON, validate schema, chạy đúng preprocessing rồi gọi model và trả label/score/model_version.
> Ví dụ request chứa các đặc trưng cho phép, response có label và score.
> Trước deploy cần test preprocessing, schema, mẫu dự đoán chuẩn và latency.
> Sau deploy theo dõi error rate, latency và chất lượng khi có nhãn; giữ model version cũ để rollback.
> Không ghi raw PII vào log.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có schema validation.
> - [ ] Preprocessing nhất quán với lúc train.
> - [ ] Có ví dụ request/response.
> - [ ] Có test latency/chất lượng.
> - [ ] Có version và rollback.

*Tags:* `deployment` `api` `essay`

#### 37. Một mô hình dùng để phân loại câu hỏi theo chủ đề đã đạt kết quả chấp nhận được trên test. Hãy đưa nó thành API thử nghiệm cho bạn đọc. Ràng buộc: - Input JSON có vài trường bắt buộc. - Phản hồi cần dưới 2 giây. - Không log dữ liệu nhạy cảm thô. - Nếu phiên bản mới kém hơn phải quay lại bản cũ. Hãy nêu: (1) flow request → prediction; (2) ví dụ request/response; (3) các kiểm tra trước và sau deploy.
**8 điểm** · Module C · `L3-L4` · `N26E13-C12` (Khóa mới 2026 · Đề 13)

> [!tip] Gợi ý
> - Nêu flow JSON input → validation → preprocessing → model → response.
> - Response nên có label, score và model_version.
> - Đừng quên test, latency, log an toàn và cách quay lại bản cũ.

> [!example]- Đáp án mẫu
> API nhận JSON, validate schema, chạy đúng preprocessing rồi gọi model và trả label/score/model_version.
> Ví dụ request chứa các đặc trưng cho phép, response có label và score.
> Trước deploy cần test preprocessing, schema, mẫu dự đoán chuẩn và latency.
> Sau deploy theo dõi error rate, latency và chất lượng khi có nhãn; giữ model version cũ để rollback.
> Không ghi raw PII vào log.

> [!check]- Rubric chấm (5 ý)
> - [ ] Có schema validation.
> - [ ] Preprocessing nhất quán với lúc train.
> - [ ] Có ví dụ request/response.
> - [ ] Có test latency/chất lượng.
> - [ ] Có version và rollback.

*Tags:* `deployment` `api` `essay`

---

### Responsible AI: privacy, fairness, oversight

#### 38. Công ty muốn dùng AI để hỗ trợ xử lý hồ sơ vay trong banking. Trả lời theo 6 mục: Privacy, Fairness/Bias, Transparency, Security, Human oversight, Accountability.
**6 điểm** · Module D · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `E01-D08`, `E06-D08`

> [!example]- Đáp án mẫu
> Privacy: chỉ dùng dữ liệu cần thiết, phân quyền và mã hóa.
> Fairness: kiểm tra tỷ lệ từ chối/chấp thuận theo nhóm, sửa feature/ngưỡng nếu lệch.
> Transparency: thông báo AI tham gia và nêu lý do ở mức phù hợp.
> Security: bảo vệ dữ liệu tài chính/định danh và audit log.
> Human oversight: hồ sơ sát ngưỡng, thiếu dữ liệu hoặc khiếu nại cần người duyệt.
> Accountability: bộ phận rủi ro/sản phẩm chịu trách nhiệm và có quy trình khiếu nại/sửa sai.

> [!check]- Rubric chấm (6 ý)
> - [ ] Nêu privacy/data minimization.
> - [ ] Nêu fairness/bias.
> - [ ] Nêu transparency/giải thích.
> - [ ] Nêu security/audit/logging.
> - [ ] Nêu human oversight.
> - [ ] Nêu accountability/khiếu nại/sửa sai.

*Tags:* `privacy` `fairness` `banking`

#### 39. Đề xuất quy trình an toàn khi dùng AI tự động khóa người bán nghi lừa đảo trên marketplace.
**6 điểm** · Module D · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `E02-D08`, `E07-D08`

> [!example]- Đáp án mẫu
> Không nên khóa tự động mọi trường hợp; nên dùng risk score, ngưỡng cao mới hạn chế tạm thời, ca sát ngưỡng cho review.
> Cần bảo vệ dữ liệu chat/giao dịch, kiểm tra bias với người bán mới/nhỏ, thông báo lý do phù hợp, cho khiếu nại, lưu log và có team chịu trách nhiệm.

> [!check]- Rubric chấm (6 ý)
> - [ ] Nêu privacy/data minimization.
> - [ ] Nêu fairness/bias.
> - [ ] Nêu transparency/giải thích.
> - [ ] Nêu security/audit/logging.
> - [ ] Nêu human oversight.
> - [ ] Nêu accountability/khiếu nại/sửa sai.

*Tags:* `marketplace` `safety`

#### 40. Công ty muốn dùng AI sàng lọc CV ứng viên. Nêu các kiểm soát đạo đức và vận hành cần có.
**6 điểm** · Module D · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `E03-D08`, `E08-D08`

> [!example]- Đáp án mẫu
> Cần giới hạn dữ liệu liên quan công việc, tránh feature nhạy cảm/đại diện, kiểm tra bias theo nhóm, minh bạch rằng AI chỉ hỗ trợ, giữ người tuyển dụng quyết định cuối, có audit log và quy trình ứng viên phản hồi/khiếu nại.

> [!check]- Rubric chấm (6 ý)
> - [ ] Nêu privacy/data minimization.
> - [ ] Nêu fairness/bias.
> - [ ] Nêu transparency/giải thích.
> - [ ] Nêu security/audit/logging.
> - [ ] Nêu human oversight.
> - [ ] Nêu accountability/khiếu nại/sửa sai.

*Tags:* `hiring` `fairness`

#### 41. Triển khai AI gợi ý chẩn đoán sơ bộ trong y tế cần đảm bảo gì?
**6 điểm** · Module D · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `E04-D08`, `E09-D08`

> [!example]- Đáp án mẫu
> AI chỉ hỗ trợ bác sĩ, không thay quyết định chuyên môn.
> Cần kiểm định chất lượng, bảo mật dữ liệu sức khỏe, giải thích/cảnh báo giới hạn, xử lý ca không chắc chắn, lưu audit, theo dõi sai sót và quy định rõ trách nhiệm.

> [!check]- Rubric chấm (6 ý)
> - [ ] Nêu privacy/data minimization.
> - [ ] Nêu fairness/bias.
> - [ ] Nêu transparency/giải thích.
> - [ ] Nêu security/audit/logging.
> - [ ] Nêu human oversight.
> - [ ] Nêu accountability/khiếu nại/sửa sai.

*Tags:* `healthcare` `safety`

#### 42. Dùng AI chấm điểm rủi ro học sinh/sinh viên cần lưu ý gì?
**6 điểm** · Module D · 🔁 **xuất hiện 2 lần** (chỉ khác số liệu): `E05-D08`, `E10-D08`

> [!example]- Đáp án mẫu
> Cần dùng dữ liệu cần thiết, tránh nhãn gây kỳ thị, kiểm tra bias theo hoàn cảnh, minh bạch mục đích hỗ trợ chứ không trừng phạt, có giáo viên/cố vấn xem lại, có đường khiếu nại và bảo vệ dữ liệu học tập cá nhân.

> [!check]- Rubric chấm (6 ý)
> - [ ] Nêu privacy/data minimization.
> - [ ] Nêu fairness/bias.
> - [ ] Nêu transparency/giải thích.
> - [ ] Nêu security/audit/logging.
> - [ ] Nêu human oversight.
> - [ ] Nêu accountability/khiếu nại/sửa sai.

*Tags:* `education` `privacy`

---

## 💻 Phần 2 — Câu code (46 câu, Module B)

Toàn bộ câu code nằm ở Module B. Đáp án mẫu là code chạy được, rubric chấm theo bước.

### Euclid / GCD / số học

#### C1. Viết hàm Python `gcd(a,b)` bằng thuật toán Euclid dùng vòng lặp. Hàm xử lý số âm bằng trị tuyệt đối. Giải thích ngắn với ví dụ gcd(252,105).
**5 điểm** · 🔁 **5 lần**: `N26E01-B19`, `N26E04-B19`, `N26E06-B19`, `N26E09-B19`, `N26E13-B19`

> [!example]- Đáp án mẫu
> ```python
> ```python
> def gcd(a: int, b: int) -> int:
>     a, b = abs(a), abs(b)
>     while b != 0:
>         a, b = b, a % b
>     return a
> 
> print(gcd(252, 105))  # 21
> ```
> Mỗi vòng thay (a,b) bằng (b,a%b). Khi b=0, a là GCD.
> ```

> [!check]- Rubric chấm
> - [ ] Có abs cho số âm.
> - [ ] Lặp đến khi b=0.
> - [ ] Cập nhật đúng a,b=b,a%b.
> - [ ] Ví dụ trả 21.

#### C2. Đoạn code sau sai: ```python def gcd(a,b): while b == 0: a, b = a % b, b return b ``` Hãy sửa thành hàm Euclid đúng, xử lý số âm và giải thích ba lỗi chính. Kiểm tra với (84,30).
**5 điểm** · 🔁 **5 lần**: `N26E02-B19`, `N26E05-B19`, `N26E07-B19`, `N26E10-B19`, `N26E11-B19`

> [!example]- Đáp án mẫu
> ```python
> ```python
> def gcd(a,b):
>     a, b = abs(a), abs(b)
>     while b != 0:
>         a, b = b, a % b
>     return a
> ```
> Ba lỗi: điều kiện vòng lặp bị đảo, phép cập nhật sai thứ tự, và phải trả a khi b=0. Kết quả là 6.
> ```

> [!check]- Rubric chấm
> - [ ] Sửa while b != 0.
> - [ ] Sửa a,b=b,a%b.
> - [ ] Trả a.
> - [ ] Có abs và ví dụ đúng.

#### C3. Không cần chạy máy, hãy ghi từng cặp (a,b) của thuật toán Euclid khi bắt đầu từ (48,18) cho đến khi dừng; sau đó viết hàm Python tương ứng.
**5 điểm** · 🔁 **3 lần**: `N26E03-B19`, `N26E08-B19`, `N26E12-B19`

> [!example]- Đáp án mẫu
> ```python
> Các phép chia: 48=2×18+12; 18=1×12+6; 12=2×6+0. Kết quả GCD=6.
> ```python
> def gcd(a,b):
>     a,b=abs(a),abs(b)
>     while b:
>         a,b=b,a%b
>     return a
> ```
> ```

> [!check]- Rubric chấm
> - [ ] Theo dõi đúng các bước.
> - [ ] Kết luận GCD=6.
> - [ ] Code vòng lặp đúng.
> - [ ] Giải thích điều kiện dừng.

#### C4. Viết hàm `safe_mean(arr)` trả về trung bình của list số; nếu list rỗng thì trả về 0.
**2.5 điểm** · 🔁 **2 lần**: `E05-B22`, `E08-B21`

> [!example]- Đáp án mẫu
> ```python
> def safe_mean(arr):
>     if len(arr) == 0:
>         return 0
>     return sum(arr) / len(arr)
> ```

> [!check]- Rubric chấm
> - [ ] Xử lý list rỗng.
> - [ ] Dùng sum/len đúng.
> - [ ] Return giá trị số.
> - [ ] Code ngắn, rõ.

---

### NumPy

#### C5. Viết hàm `fetch_average(url, token)`: gọi GET bằng Requests, gửi Bearer token trong header, timeout 5 giây, phát hiện HTTP error, kiểm tra JSON có danh sách số không rỗng ở trường `scores`, rồi dùng NumPy trả trung bình dạng float. Schema sai phải raise ValueError.
**5 điểm** · 🔁 **3 lần**: `N26E02-B20`, `N26E06-B20`, `N26E13-B20`

> [!example]- Đáp án mẫu
> ```python
> ```python
> import requests
> import numpy as np
> 
> def fetch_average(url, token):
>     response=requests.get(url, headers={'Authorization': f'Bearer {token}'}, timeout=5)
>     response.raise_for_status()
>     payload=response.json()
>     scores=payload.get('scores') if isinstance(payload, dict) else None
>     if not isinstance(scores, list) or not scores or any(isinstance(v,bool) or not isinstance(v,(int,float)) for v in scores):
>         raise ValueError('scores must be a non-empty numeric list')
>     return float(np.asarray(scores,dtype=float).mean())
> ```
> ```

> [!check]- Rubric chấm
> - [ ] GET, header và timeout đúng.
> - [ ] Có raise_for_status và response.json.
> - [ ] Kiểm tra schema/dữ liệu số.
> - [ ] Dùng NumPy và trả float.
> - [ ] Không log token.

#### C6. Không chạy code, hãy nêu giá trị và shape: ```python import numpy as np x=np.arange(12).reshape(3,4) a=x[:,2] b=x[:,2:3] c=x.mean(axis=1) ``` Giải thích vì sao a và b chứa cùng cột nhưng shape khác nhau.
**5 điểm** · 🔁 **3 lần**: `N26E03-B20`, `N26E10-B20`, `N26E12-B20`

> [!example]- Đáp án mẫu
> ```python
> x=[[0,1,2,3],[4,5,6,7],[8,9,10,11]], shape (3,4). a=[2,6,10], shape (3,). b=[[2],[6],[10]], shape (3,1). c=[1.5,5.5,9.5], shape (3,). Chỉ số nguyên bỏ chiều cột, slice giữ chiều.
> ```

> [!check]- Rubric chấm
> - [ ] Đúng x.
> - [ ] Đúng a và shape.
> - [ ] Đúng b và shape.
> - [ ] Đúng c và giải thích axis=1.
> - [ ] Giải thích integer index và slice.

#### C7. Giải thích giá trị và shape của x, y, z, m mà không chạy code: ```python import numpy as np x=np.array([[1,2,3],[5,6,7]]) y=x[:,1:] z=y.mean(axis=0) m=x[x%2==0] ```
**5 điểm** · 🔁 **2 lần**: `N26E01-B20`, `N26E07-B20`

> [!example]- Đáp án mẫu
> ```python
> x shape (2,3). y lấy mọi hàng và hai cột cuối, shape (2,2). z là trung bình theo cột của y, shape (2,). m lấy các phần tử chẵn bằng boolean indexing và trở thành mảng 1 chiều.
> ```

> [!check]- Rubric chấm
> - [ ] Đúng shape x.
> - [ ] Đúng giá trị/shape y.
> - [ ] Giải thích axis=0 của z.
> - [ ] Giải thích boolean indexing tạo mảng 1 chiều.

#### C8. Viết hàm `fetch_pass_rate(url)`: GET API với timeout 5 giây; JSON dạng `{"scores":[...] }`; kiểm tra danh sách số không rỗng; dùng NumPy tính tỷ lệ phần tử >=50 và trả float trong [0,1]. Nêu một lỗi có thể xảy ra và cách xử lý.
**5 điểm** · 🔁 **2 lần**: `N26E05-B20`, `N26E09-B20`

> [!example]- Đáp án mẫu
> ```python
> ```python
> import requests
> import numpy as np
> 
> def fetch_pass_rate(url):
>     r=requests.get(url, timeout=5)
>     r.raise_for_status()
>     payload=r.json()
>     scores=payload.get('scores') if isinstance(payload,dict) else None
>     if not isinstance(scores,list) or not scores or any(isinstance(v,bool) or not isinstance(v,(int,float)) for v in scores):
>         raise ValueError('invalid scores')
>     values=np.asarray(scores,dtype=float)
>     return float((values>=50).mean())
> ```
> Có thể bắt requests.RequestException ở tầng gọi hoặc chuyển thành lỗi ứng dụng rõ ràng.
> ```

> [!check]- Rubric chấm
> - [ ] GET và timeout.
> - [ ] Status/JSON/schema validation.
> - [ ] Dùng boolean mask NumPy.
> - [ ] Trả float đúng.
> - [ ] Nêu lỗi và cách xử lý.

---

### Gọi API / Requests

#### C9. Sửa đoạn code sau và giải thích lỗi: ```python def get_score(url): r=requests.get(url) data=eval(r.text) return data['score'] ``` Yêu cầu: timeout, phát hiện HTTP error, đọc JSON an toàn, kiểm tra score là số và xử lý lỗi Requests ở mức cơ bản.
**5 điểm** · 🔁 **3 lần**: `N26E04-B20`, `N26E08-B20`, `N26E11-B20`

> [!example]- Đáp án mẫu
> ```python
> ```python
> import requests
> 
> def get_score(url):
>     try:
>         r=requests.get(url, timeout=5)
>         r.raise_for_status()
>         data=r.json()
>     except requests.RequestException as exc:
>         raise RuntimeError('API request failed') from exc
>     score=data.get('score') if isinstance(data,dict) else None
>     if isinstance(score,bool) or not isinstance(score,(int,float)):
>         raise ValueError('invalid score')
>     return float(score)
> ```
> Không dùng eval với dữ liệu mạng; thêm timeout, status check và schema validation.
> ```

> [!check]- Rubric chấm
> - [ ] Có timeout.
> - [ ] Có raise_for_status.
> - [ ] Không dùng eval.
> - [ ] Bắt RequestException.
> - [ ] Kiểm tra score là số.

---

### Xử lý chuỗi & dict

#### C10. Viết hàm `count_words(text)` trả về dict đếm số lần xuất hiện của từng từ, tách theo khoảng trắng. Ví dụ: `'a b a'` → `{'a': 2, 'b': 1}`.
**2.5 điểm** · 🔁 **2 lần**: `E01-B21`, `E08-B22`

> [!example]- Đáp án mẫu
> ```python
> def count_words(text):
>     counts = {}
>     for word in text.split():
>         counts[word] = counts.get(word, 0) + 1
>     return counts
> ```

> [!check]- Rubric chấm
> - [ ] Dùng `split()` để tách từ.
> - [ ] Dùng dict để đếm.
> - [ ] Cập nhật count đúng khi từ lặp lại.
> - [ ] Return dict kết quả.

#### C11. Viết hàm `dedupe_preserve_order(arr)` trả về list mới chỉ giữ lần xuất hiện đầu tiên và giữ nguyên thứ tự. Ví dụ `[3,1,3,2,1]` → `[3,1,2]`.
**2.5 điểm** · 🔁 **2 lần**: `E02-B21`, `E09-B22`

> [!example]- Đáp án mẫu
> ```python
> def dedupe_preserve_order(arr):
>     seen = set()
>     result = []
>     for x in arr:
>         if x not in seen:
>             seen.add(x)
>             result.append(x)
>     return result
> ```

> [!check]- Rubric chấm
> - [ ] Dùng `seen` để nhớ phần tử đã gặp.
> - [ ] Không làm mất thứ tự ban đầu.
> - [ ] Không thêm phần tử trùng.
> - [ ] Return list mới.

#### C12. Viết hàm `build_user_total(records)` nhận list dict có `user` và `amount`, trả về dict tổng amount theo user.
**2.5 điểm** · 🔁 **2 lần**: `E03-B22`, `E06-B21`

> [!example]- Đáp án mẫu
> ```python
> def build_user_total(records):
>     totals = {}
>     for row in records:
>         user = row['user']
>         totals[user] = totals.get(user, 0) + row['amount']
>     return totals
> ```

> [!check]- Rubric chấm
> - [ ] Duyệt list record.
> - [ ] Lấy đúng user/amount.
> - [ ] Cộng dồn theo key user.
> - [ ] Return dict tổng.

#### C13. Viết hàm `filter_non_empty(strings)` trả về các chuỗi không rỗng sau khi strip khoảng trắng.
**2.5 điểm** · 🔁 **2 lần**: `E04-B22`, `E07-B21`

> [!example]- Đáp án mẫu
> ```python
> def filter_non_empty(strings):
>     result = []
>     for s in strings:
>         cleaned = s.strip()
>         if cleaned:
>             result.append(cleaned)
>     return result
> ```

> [!check]- Rubric chấm
> - [ ] Dùng `strip()`.
> - [ ] Bỏ chuỗi rỗng sau strip.
> - [ ] Giữ chuỗi đã làm sạch.
> - [ ] Return list.

#### C14. Viết hàm `token_count_simple(text)` đếm số token đơn giản bằng cách tách theo khoảng trắng sau khi strip.
**2.5 điểm** · 🔁 **2 lần**: `E07-B22`, `E10-B21`

> [!example]- Đáp án mẫu
> ```python
> def token_count_simple(text):
>     text = text.strip()
>     if not text:
>         return 0
>     return len(text.split())
> ```

> [!check]- Rubric chấm
> - [ ] Strip đầu/cuối.
> - [ ] Xử lý chuỗi rỗng.
> - [ ] Dùng split để đếm từ/token đơn giản.
> - [ ] Return số nguyên.

---

### Khác

#### C15. Viết hàm `min_max_scale(arr)` scale list số về khoảng 0..1. Nếu mọi giá trị bằng nhau, trả về list toàn 0.
**2.5 điểm** · 🔁 **2 lần**: `E01-B22`, `E04-B21`

> [!example]- Đáp án mẫu
> ```python
> def min_max_scale(arr):
>     mn = min(arr)
>     mx = max(arr)
>     if mx == mn:
>         return [0 for _ in arr]
>     return [(x - mn) / (mx - mn) for x in arr]
> ```

> [!check]- Rubric chấm
> - [ ] Tính min/max đúng.
> - [ ] Xử lý trường hợp max bằng min.
> - [ ] Áp dụng công thức `(x-min)/(max-min)`.
> - [ ] Return list cùng độ dài.

#### C16. Viết hàm `top_k_scores(items, k)` nhận list tuple `(name, score)` và trả về k phần tử có score cao nhất.
**2.5 điểm** · 🔁 **2 lần**: `E02-B22`, `E05-B21`

> [!example]- Đáp án mẫu
> ```python
> def top_k_scores(items, k):
>     return sorted(items, key=lambda x: x[1], reverse=True)[:k]
> ```

> [!check]- Rubric chấm
> - [ ] Sắp xếp theo score.
> - [ ] Sắp xếp giảm dần.
> - [ ] Cắt đúng k phần tử.
> - [ ] Không cần thay đổi input gốc.

#### C17. Viết hàm `sum_even(arr)` trả về tổng các số chẵn trong list số nguyên.
**2.5 điểm** · 🔁 **2 lần**: `E03-B21`, `E10-B22`

> [!example]- Đáp án mẫu
> ```python
> def sum_even(arr):
>     total = 0
>     for x in arr:
>         if x % 2 == 0:
>             total += x
>     return total
> ```

> [!check]- Rubric chấm
> - [ ] Duyệt từng phần tử.
> - [ ] Kiểm tra chẵn bằng `% 2 == 0`.
> - [ ] Cộng đúng vào tổng.
> - [ ] Return tổng.

#### C18. Viết hàm `label_by_threshold(scores, threshold)` trả về list 0/1, score >= threshold thì 1, ngược lại 0.
**2.5 điểm** · 🔁 **2 lần**: `E06-B22`, `E09-B21`

> [!example]- Đáp án mẫu
> ```python
> def label_by_threshold(scores, threshold):
>     return [1 if s >= threshold else 0 for s in scores]
> ```

> [!check]- Rubric chấm
> - [ ] Duyệt toàn bộ scores.
> - [ ] So sánh với threshold.
> - [ ] Trả về 1/0 đúng.
> - [ ] Return list cùng độ dài.

---

**Xem thêm:** [[AI Test - Kien thuc can nho]]
