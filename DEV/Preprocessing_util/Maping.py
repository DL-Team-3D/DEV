import os
import glob
import cv2

base_name = "R_435_40_M_06_M0_G0_C0_11"

label_dir = "경로"
image_root = "경로"
save_dir = "경로"

os.makedirs(save_dir, exist_ok=True)

txt_path = os.path.join(label_dir, base_name + ".txt")

if not os.path.exists(txt_path):
    raise FileNotFoundError(f"라벨 파일이 없습니다: {txt_path}")

# === 1. 이미지 먼저 찾기 ===
img_path = None
for ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]:
    pattern = os.path.join(image_root, "**", base_name + ext)
    matches = glob.glob(pattern, recursive=True)
    if matches:
        img_path = matches[0]
        break

if img_path is None:
    raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {base_name}")

img = cv2.imread(img_path)
if img is None:
    raise RuntimeError(f"이미지를 읽을 수 없습니다: {img_path}")

img_h, img_w = img.shape[:2]

# === 2. TXT의 모든 라인 처리 ===
with open(txt_path, "r") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

for line in lines:
    parts = line.split()
    if len(parts) != 5:
        print(f"[무시] 형식 이상: {line}")
        continue

    cls_id = int(parts[0])
    cx, cy, w, h = map(float, parts[1:])

    # YOLO → 절대좌표
    x_center = cx * img_w
    y_center = cy * img_h
    box_w = w * img_w
    box_h = h * img_h

    x1 = int(x_center - box_w / 2)
    y1 = int(y_center - box_h / 2)
    x2 = int(x_center + box_w / 2)
    y2 = int(y_center + box_h / 2)

    color = (0, 255, 0)  # 초록박스
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    label_text = f"{cls_id}"
    cv2.putText(
        img,
        label_text,
        (x1, max(0, y1 - 5)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA
    )

out_path = os.path.join(save_dir, base_name + "_vis.jpg")
cv2.imwrite(out_path, img)

print(f"저장 완료: {out_path}")
print(f"→ {len(lines)}개의 박스가 그려졌어 (원래 txt 줄 수)")