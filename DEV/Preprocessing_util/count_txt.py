import os
 
unlabel_path = ""
label_path = ""

unlabel_count = sum([len(files) for r, d, files in os.walk(unlabel_path)])
label_count = sum([len(files) for r, d, files in os.walk(label_path)])
print(unlabel_count)
print(label_count)