from pathlib import Path
from sklearn.model_selection import train_test_split

name = "nu_trung_audio_text"
all_path = f"filelists/{name}.txt"
train_path = f"filelists/{name}_train.txt"
val_path = f"filelists/{name}_val.txt"
test_path = f"filelists/{name}_test.txt"

with open(all_path, "r") as f:
    datas = f.readlines()

train, val_test = train_test_split(datas, test_size=0.05)

val, test = train_test_split(val_test, test_size=0.8)

print(len(train), len(val), len(test))

with open(train_path, "w") as f:
    for line in train:
        f.write(line.strip())
        f.write("\n")

with open(val_path, "w") as f:
    for line in val:
        f.write(line.strip())
        f.write("\n")

with open(test_path, "w") as f:
    for line in val:
        f.write(line.strip())
        f.write("\n")

