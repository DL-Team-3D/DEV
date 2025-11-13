import os

TRAIN_DIR = ""
VAL_DIR = ""

# 확장자 제거한 파일 이름만 추출
train_stems = {os.path.splitext(f)[0] for f in os.listdir(TRAIN_DIR) if f.lower().endswith(".jpg")}
val_stems   = {os.path.splitext(f)[0] for f in os.listdir(VAL_DIR) if f.lower().endswith(".jpg")}

print(f"🔍 train_image 파일 개수: {len(train_stems)}")
print(f"🔍 val_image 파일 개수:   {len(val_stems)}")