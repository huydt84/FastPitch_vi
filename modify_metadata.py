from pathlib import Path

metadata_path = "nu_trung_nichi/metadata.csv"
filelist_path = "filelists/nu_trung_audio_text.txt"

new_line = []
with open(metadata_path, "r") as f:
    for line in f:
        part = line.strip().split("|")
        path, text = part[0], part[1]

        name = Path(path).stem
        new_line.append(f"wavs/{path}.wav|{text}\n")

with open(filelist_path, "w") as f:
    for line in new_line:
        f.write(line)
