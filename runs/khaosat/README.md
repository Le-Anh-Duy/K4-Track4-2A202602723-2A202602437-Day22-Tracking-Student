# Các lần chạy thử

Căn cứ cho cột *Đã thử nhưng loại* và phần phân tích trong `submission_template/BAO_CAO_mau.md`. Không phải file nộp chính — file nộp nằm ở `runs/nop_bai/`.

- `video_1/…_f600/`: chạy đủ 600 frame, chấm bằng `scripts/evaluate_practice.py`.
- `video_2/` … `video_5/`: 300 frame đầu, không có nhãn nên chỉ có chỉ số thô.
- Tên thư mục: `<tracker>_c<conf>_i<iou>_f<số frame>`.
- `tong_hop.csv`: gom mọi lần chạy. Với `video_1` có HOTA / MOTA / IDF1 / IDSW. Với mọi video có:
  - `hop_moi_frame`: số hộp trung bình mỗi frame — bắt được nhiều người hay ít.
  - `so_ID`, `ID_song_duoi_10_frame`: nhiều ID ngắn thường là hộp giả hoặc track bị đứt.
  - `ID_moi_giua_anh_moi_1000_hop`: ID mới xuất hiện giữa khung hình (không phải ở mép ảnh), chia cho số hộp — gợi ý track bị đứt rồi mở lại. **Không phải metric**, chỉ dùng để so các tracker trên cùng một video.
