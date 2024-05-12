#!/usr/bin/env bash

set -e

: ${DATA_DIR:=nu_trung_nichi}
: ${ARGS="--extract-mels"}

python3 prepare_dataset.py \
    --wav-text-filelists filelists/nu_trung_audio_text.txt \
    --n-workers 2 \
    --batch-size 1 \
    --dataset-path $DATA_DIR \
    --extract-pitch \
    --f0-method pyin \
    $ARGS