from pathlib import Path

name = "nu_trung_audio_text"
train_path = f"filelists/{name}_train.txt"
val_path = f"filelists/{name}_val.txt"
test_path = f"filelists/{name}_test.txt"

train_pitch_path = f"filelists/{name}_pitch_train.txt"
val_pitch_path = f"filelists/{name}_pitch_val.txt"
test_pitch_path = f"filelists/{name}_pitch_test.txt"

def write_pitch(text_path, text_pitch_path):
    new_lines = []
    with open(text_path, "r") as f:
        for line in f:
            part = line.strip().split("|")
            audio_path, text = part[0], part[1]
            pitch_path = Path(audio_path).with_suffix(".pt").name

            new_lines.append(f"{audio_path}|pitch/{pitch_path}|{text}\n")

    with open(text_pitch_path, "w") as f:
        for line in new_lines:
            f.write(line)

write_pitch(train_path, train_pitch_path)
write_pitch(val_path, val_pitch_path)
write_pitch(test_path, test_pitch_path)
