# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** 2A202602723 – 2A202602437 **Thành viên:** Lê Anh Duy (2A202602723), Vũ Đức Thiện (2A202602437)

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | botsort | 0.3 | 0.7 | Người gần và cỡ vừa có hộp, còn nhiều người nhỏ ở xa không có hộp (DetRe chỉ 19 %). Lỗi chính nằm ở phát hiện, không ở ghép ID (AssA 49). 55 ID cho 62 người thật trong nhãn. | `bytetrack` 0.3/0.5: ít đổi ID nhất (IDSW 12) nhưng bỏ sót nhiều hơn, HOTA 26.9. `botsort` conf 0.5: mất thêm người, HOTA 27.2. `ocsort` conf 0.15: hộp điểm thấp mở track mới liên tục, IDSW 165. |
| video_2 (phố đêm, tĩnh, rất đông) | botsort | 0.15 | 0.5 | Phố đủ đèn; người cỡ vừa ở giữa ảnh đều có hộp, chỉ 4 ID sống dưới 10 frame trên cả 1050 frame. Đám đông nhỏ ở xa phía trên vẫn bị sót. Không có hộp trên xe, cọc giao thông, cột đèn. | `botsort` conf 0.3: ít hộp hơn (11.7 so với 13.1 hộp/frame) và nhiều ID mọc giữa ảnh hơn. `strongsort` 0.3: track đứt nhiều nhất (8.3 ID mới giữa ảnh / 1000 hộp). `bytetrack` 0.3: ít ID nhưng mất ~16 % số hộp. |
| video_3 (camera di động, ảnh nhỏ) | ocsort | 0.3 | 0.5 | Người to, đi sát camera và che nhau liên tục; số ID tăng rất nhanh — 137 ID trên 837 frame, đến frame 700 ID đã lên ~165 — tức track bị đứt và mở lại nhiều lần. Đây là video khó nhất cho mọi tracker. | `botsort` / `strongsort` 0.3: 55 ID trong 300 frame đầu so với 50 của `ocsort`, nhiều track đứt hơn; Re-ID không giúp trên ảnh 640×480 mờ. `bytetrack`: ít hộp nhất (4.5 hộp/frame). |
| video_4 (trong nhà, camera di chuyển) | deepocsort | 0.3 | 0.5 | Sàn bóng và lan can kính phản chiếu người nhưng không bị nhận là người ở conf 0.3. Người trong hành lang, kể cả người bị che một phần, đều có hộp. | `deepocsort` conf 0.5: bỏ người bị che một phần (hộp thật chỉ 0.37 điểm), track đứt nhiều hơn. `ocsort` 0.3: 30 ID so với 26. `strongsort`: track đứt nhiều nhất. |
| video_5 (trên xe bus, giao lộ đông) | botsort | 0.15 | 0.5 | Người đi bộ rất nhỏ ở xa; chỉ người gần vỉa hè có hộp (4.4 hộp/frame). Không thấy hộp trên xe, cột đèn, biển báo. Conf thấp bắt thêm người nhỏ mà số ID gần như không đổi. | `botsort` conf 0.3: ít hộp hơn ~10 %. `strongsort` 0.3: 54 ID / 300 frame, đứt nhiều nhất. `bytetrack` 0.3: mất ~1/3 số hộp. |

Số liệu của mọi lần chạy thử (36 lần: 5 tracker × các mức `conf` / `iou`) nằm trong `runs/khaosat/tong_hop.csv`, file kết quả từng lần trong `runs/khaosat/<video>/`. Video 2–5 thử trên 300 frame đầu; bản nộp ở `runs/nop_bai/` chạy đủ frame.

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```
HOTA: nhom_2A202602723_2A202602437_video1-pedestrianHOTA      DetA      AssA      DetRe     DetPr     AssRe     AssPr     LocA      OWTA      HOTA(0)   LocA(0)   HOTALocA(0)
video_1                            29.969    18.408    49.061    19.176    74.385    52.38     80.959    83.019    30.624    37.181    76.409    28.409
COMBINED                           29.969    18.408    49.061    19.176    74.385    52.38     80.959    83.019    30.624    37.181    76.409    28.409
CLEAR: nhom_2A202602723_2A202602437_video1-pedestrianMOTA      MOTP      MODA      CLR_Re    CLR_Pr    MTR       PTR       MLR       sMOTA     CLR_TP    CLR_FN    CLR_FP    IDSW      MT        PT        ML        Frag
video_1                            19.025    80.817    19.202    22.491    87.244    14.516    17.742    67.742    14.71     4179      14402     611       33        9         11        42        105
COMBINED                           19.025    80.817    19.202    22.491    87.244    14.516    17.742    67.742    14.71     4179      14402     611       33        9         11        42        105
Identity: nhom_2A202602723_2A202602437_video1-pedestrianIDF1      IDR       IDP       IDTP      IDFN      IDFP
video_1                            29.703    18.68     72.463    3471      15110     1319
COMBINED                           29.703    18.68     72.463    3471      15110     1319
Count: nhom_2A202602723_2A202602437_video1-pedestrianDets      GT_Dets   IDs       GT_IDs
video_1                            4790      18581     55        62
COMBINED                           4790      18581     55        62

[nhom_2A202602723_2A202602437_video1] HOTA=29.97  MOTA=19.02  IDF1=29.70  IDSW=33
```

Các cấu hình đã chấm trên `video_1` (đủ 600 frame):

| Tracker | conf | iou | HOTA | MOTA | IDF1 | IDSW |
|---|---|---|---|---|---|---|
| **botsort** | **0.3** | **0.7** | **29.97** | 19.02 | 29.70 | 33 |
| botsort | 0.3 | 0.5 | 29.46 | 19.81 | 29.35 | 25 |
| botsort | 0.15 | 0.5 | 29.34 | 20.73 | 29.56 | 27 |
| botsort | 0.3 | 0.4 | 29.32 | 19.47 | 29.82 | 19 |
| strongsort | 0.15 | 0.5 | 29.19 | 19.91 | 32.57 | 110 |
| strongsort | 0.3 | 0.5 | 28.66 | 19.70 | 29.85 | 41 |
| ocsort | 0.3 | 0.5 | 27.45 | 19.81 | 28.73 | 42 |
| deepocsort | 0.3 | 0.5 | 27.38 | 19.76 | 27.80 | 51 |
| bytetrack | 0.15 | 0.5 | 27.31 | 18.31 | 26.99 | 13 |
| botsort | 0.5 | 0.5 | 27.17 | 15.25 | 24.56 | 10 |
| bytetrack | 0.3 | 0.5 | 26.91 | 17.29 | 25.71 | 12 |
| ocsort | 0.15 | 0.5 | 25.93 | 19.50 | 29.18 | 165 |
| deepocsort | 0.15 | 0.5 | 25.25 | 19.37 | 28.15 | 195 |

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

Với **ít nhất hai video** (nên gồm một video bạn chỉ đánh giá bằng mắt), viết 3–5 câu:

- Tracker đã chọn giữ ID tốt hơn, hay ít hộp giả hơn, ở điểm nào bạn nhìn thấy?
- Cảnh đó (đứng yên / chuyển động, đông / thưa, sáng / tối, trong nhà / ngoài trời) khiến tracker này hợp hơn tracker kia như thế nào?

**video_1 (camera tĩnh, ban ngày, có nhãn).** BoT-SORT có HOTA cao nhất (29.97) vì cân bằng được cả hai phía: nó bắt nhiều người hơn ByteTrack (DetA cao hơn) mà không mở track mới bừa bãi như OCSORT / DeepOCSORT khi hạ conf. ByteTrack đổi ID ít nhất (IDSW 12) nhưng chỉ mở track cho hộp điểm cao, nên bỏ sót nhiều người và HOTA thấp hơn 3 điểm — đúng kiểu "ít lỗi danh tính nhưng thiếu người". Hạ conf xuống 0.15 làm OCSORT / DeepOCSORT đổi ID 165–195 lần vì mỗi hộp điểm thấp nhấp nháy thành một track mới, trong khi BoT-SORT gần như không đổi nhờ ngưỡng mở track riêng. Giới hạn chung là detector: DetRe chỉ 19 % vì người nhỏ ở ảnh 1920×1080 thu về 640 px bị sót, nên mọi tracker đều dừng quanh HOTA 25–30.

**video_2 (camera tĩnh, ban đêm, rất đông — chỉ xem bằng mắt).** Camera đứng yên nên chuyển động của người gần tuyến tính, và tracker nào cũng ghép được phần lớn; khác biệt nằm ở số người bắt được và số lần track bị đứt. BoT-SORT với conf 0.15 vừa bắt thêm người (13.1 so với 11.7 hộp/frame) vừa có ít ID mọc ra giữa ảnh nhất trong nhóm bắt đủ người (3.1 / 1000 hộp), tức hạ conf ở đây cứu được người trong vùng tối mà không sinh hộp rác. StrongSORT tệ nhất (8.3 / 1000 hộp): ánh sáng đèn đường làm đặc trưng ngoại hình kém ổn định, nên dựa nhiều vào Re-ID lại gây đứt track.

**video_4 (trong nhà, camera tiến tới, kính phản chiếu — chỉ xem bằng mắt).** Lo ngại chính là bóng phản chiếu trên sàn và lan can kính bị nhận là người, nhưng ở conf 0.3 detector không vẽ hộp nào lên các bóng đó; nâng lên 0.5 lại bỏ cả người thật bị che một phần (hộp 0.37 điểm). DeepOCSORT giữ ID tốt nhất (26 ID, 7.0 ID mọc giữa ảnh / 1000 hộp) vì kết hợp chuyển động với ngoại hình: khi camera tiến tới, người to dần và dịch chuyển không đều, ngoại hình giúp nối lại track mà chỉ chuyển động (OCSORT, 30 ID) dễ đứt.

**video_5 (trên xe bus, rung lắc — chỉ xem bằng mắt).** Cả khung hình xê dịch khi xe rung, nên tracker chỉ dựa vào chuyển động dự đoán sai vị trí. BoT-SORT có bù chuyển động camera (`sparseOptFlow`), và nó có ít ID nhất trong nhóm bắt đủ người (42 so với 48–54 trong 300 frame đầu), phù hợp với việc ít bị đứt track khi khung hình giật. Người đi bộ ở xa rất nhỏ, nên conf 0.15 giúp bắt thêm ~10 % hộp mà số ID gần như giữ nguyên.

## 4. Nếu có thêm thời gian

Xem kỹ các frame của `video_3` nơi người ra khỏi khung rồi quay lại để biết ID mới do Re-ID thất bại hay do FPS thấp, và thử một Re-ID mạnh hơn trong phần mở rộng. Quét conf mịn hơn (0.2 / 0.25) cho BoT-SORT trên `video_2`, `video_5`, và thử `iou` 0.7 cho cảnh đông vì trên `video_1` nó tăng HOTA thêm 0.5.
