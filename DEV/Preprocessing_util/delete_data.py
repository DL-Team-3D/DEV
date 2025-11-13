import os

IMAGE_ROOT = "경로"
LABEL_ROOT = "경로"

def collect_stems(root, exts):
    stems = set()
    for dirpath, _, files in os.walk(root):
        for f in files:
            if any(f.lower().endswith(ext) for ext in exts):
                stems.add(os.path.splitext(f)[0])
    return stems

def delete_unmatched():
    # 1) 이미지 / 라벨 이름 수집
    image_stems = collect_stems(IMAGE_ROOT, [".jpg", ".jpeg", ".png"])
    label_stems = collect_stems(LABEL_ROOT, [".txt"])

    only_image = image_stems - label_stems   # 라벨 없는 이미지
    only_label = label_stems - image_stems   # 이미지 없는 라벨

    print(f"이미지 개수: {len(image_stems)}")
    print(f"라벨 개수: {len(label_stems)}")
    print(f"라벨 없는 이미지: {len(only_image)}개")
    print(f"이미지 없는 라벨: {len(only_label)}개\n")

    # 2) 라벨 없는 이미지 삭제
    deleted_imgs = 0
    for dirpath, _, files in os.walk(IMAGE_ROOT):
        for f in files:
            stem, ext = os.path.splitext(f)
            if stem in only_image and ext.lower() in [".jpg", ".jpeg", ".png"]:
                full_path = os.path.join(dirpath, f)
                try:
                    os.remove(full_path)
                    deleted_imgs += 1
                    # print(f"[DEL IMG] {full_path}")
                except Exception as e:
                    print(f"[IMG ERROR] {full_path} 삭제 실패: {e}")

    # 3) 이미지 없는 라벨 삭제
    deleted_labels = 0
    for dirpath, _, files in os.walk(LABEL_ROOT):
        for f in files:
            stem, ext = os.path.splitext(f)
            if stem in only_label and ext.lower() == ".txt":
                full_path = os.path.join(dirpath, f)
                try:
                    os.remove(full_path)
                    deleted_labels += 1
                    # print(f"[DEL LAB] {full_path}")
                except Exception as e:
                    print(f"[LAB ERROR] {full_path} 삭제 실패: {e}")

    print(f"\n[RESULT] 삭제된 이미지: {deleted_imgs}개")
    print(f"[RESULT] 삭제된 라벨: {deleted_labels}개")

if __name__ == "__main__":
    delete_unmatched()