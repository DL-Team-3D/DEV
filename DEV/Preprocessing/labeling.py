import os
import json

# ===== 경로 설정 =====
BASE_DOCS = "경로"
UNLABEL_ROOT = os.path.join(BASE_DOCS, "unlabel")   # bus, car, texi, truck 폴더들이 있는 곳
LABEL_ROOT = os.path.join(BASE_DOCS, "label")       # 결과 txt를 저장할 곳

os.makedirs(LABEL_ROOT, exist_ok=True)


# ===== YOLO 형식으로 bbox 변환 함수 =====
def get_object_params(i_width: int, i_height: int, xmin, ymin, xmax, ymax):
    image_width = float(i_width)
    image_height = float(i_height)

    center_x = xmin + 0.5 * (xmax - xmin)
    center_y = ymin + 0.5 * (ymax - ymin)

    absolute_width = xmax - xmin
    absolute_height = ymax - ymin

    l_x = center_x / image_width
    l_y = center_y / image_height
    l_width = absolute_width / image_width
    l_height = absolute_height / image_height

    return l_x, l_y, l_width, l_height


# ===== JSON 하나를 TXT로 변환 =====
def process_single_json(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 파일 이름, 이미지 크기
    file_name = data["FileInfo"]["FileName"]  # 예: R_062_60_M_01_M0_G0_C0_01.jpg
    img_w = int(data["FileInfo"]["Width"])
    img_h = int(data["FileInfo"]["Height"])

    bbox = data["ObjectInfo"]["BoundingBox"]

    lines = []

    # 두 눈을 차례대로 처리
    for eye_key in ["Leye", "Reye"]:
        eye_info = bbox.get(eye_key, {})

        # 눈이 보이지 않으면 스킵
        if not eye_info.get("isVisible", False):
            continue

        opened_flag = 1 if eye_info.get("Opened", False) else 0

        # [xmin, ymin, xmax, ymax] 위치 값
        exmin, eymin, exmax, eymax = map(float, eye_info["Position"])

        cx, cy, w, h = get_object_params(img_w, img_h, exmin, eymin, exmax, eymax)

        # 한 줄: open_flag center_x center_y width height
        line = f"{opened_flag} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"
        lines.append(line)

    # 눈 정보가 하나도 없으면 파일을 만들지 않음
    if not lines:
        return

    # 출력 파일 이름: 이미지 이름에서 확장자만 .txt로
    stem = os.path.splitext(file_name)[0]
    out_path = os.path.join(LABEL_ROOT, stem + ".txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved: {out_path}")


# ===== 전체 폴더 순회 =====
def main():
    # /home/linux1116/Documents/unlabel 아래의 모든 json 탐색 (bus, car, texi, truck 포함)
    for root, dirs, files in os.walk(UNLABEL_ROOT):
        for fname in files:
            if not fname.lower().endswith(".json"):
                continue
            json_path = os.path.join(root, fname)
            try:
                process_single_json(json_path)
            except Exception as e:
                print(f"[ERROR] {json_path} 처리 중 오류: {e}")


if __name__ == "__main__":
    main()