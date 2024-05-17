#!/usr/bin/env bash

export OMP_NUM_THREADS=1

: ${NUM_GPUS:=1}
: ${BATCH_SIZE:=16}
: ${GRAD_ACCUMULATION:=8}
: ${OUTPUT_DIR:="./output_multi"}
: ${LOG_FILE:=$OUTPUT_DIR/nvlog.json}
: ${DATASET_PATH:=nam_bac_nsut-ha-phuong}
: ${TRAIN_FILELIST:=filelists/nam_bac_audio_text_pitch_train.txt}
: ${VAL_FILELIST:=filelists/nam_bac_audio_text_pitch_val.txt}
: ${AMP:=true}
: ${SEED:=""}

: ${LEARNING_RATE:=0.01}

# Adjust these when the amount of data changes
: ${EPOCHS:=100}
: ${EPOCHS_PER_CHECKPOINT:=2}
: ${WARMUP_STEPS:=1000}
: ${KL_LOSS_WARMUP:=100}

# Train a mixed phoneme/grapheme model
: ${PHONE:=true}
# Enable energy conditioning
: ${ENERGY:=true}
: ${TEXT_CLEANERS:=vietnamese_cleaner}
# Add dummy space prefix/suffix is audio is not precisely trimmed
: ${APPEND_SPACES:=false}

: ${LOAD_PITCH_FROM_DISK:=true}
: ${LOAD_MEL_FROM_DISK:=false}

# For multispeaker models, add speaker ID = {0, 1, ...} as the last filelist column
: ${NSPEAKERS:=5}
: ${SAMPLING_RATE:=22050}

# Adjust env variables to maintain the global batch size: NUM_GPUS x BATCH_SIZE x GRAD_ACCUMULATION = 256.
GBS=$(($NUM_GPUS * $BATCH_SIZE * $GRAD_ACCUMULATION))
[ $GBS -ne 256 ] && echo -e "\nWARNING: Global batch size changed from 256 to ${GBS}."
echo -e "\nAMP=$AMP, ${NUM_GPUS}x${BATCH_SIZE}x${GRAD_ACCUMULATION}" \
        "(global batch size ${GBS})\n"

# ARGS=""
ARGS+=" --cuda"
ARGS+=" -o $OUTPUT_DIR"
ARGS+=" --log-file $LOG_FILE"

ARGS+=" --dataset-path0 nam_bac_nsut-ha-phuong"
ARGS+=" --training-files0 filelists/nam_bac_audio_text_pitch_train.txt"
ARGS+=" --validation-files0 filelists/nam_bac_audio_text_pitch_val.txt"

ARGS+=" --dataset-path1 nam_nam_vu-quang-hung"
ARGS+=" --training-files1 filelists/nam_nam_audio_text_pitch_train.txt"
ARGS+=" --validation-files1 filelists/nam_nam_audio_text_pitch_val.txt"

ARGS+=" --dataset-path2 nu_bac_nsut-hoang-yen"
ARGS+=" --training-files2 filelists/nu_bac_audio_text_pitch_train.txt"
ARGS+=" --validation-files2 filelists/nu_bac_audio_text_pitch_val.txt"

ARGS+=" --dataset-path3 nu_nam_kenh-co-trinh"
ARGS+=" --training-files3 filelists/nu_nam_audio_text_pitch_train.txt"
ARGS+=" --validation-files3 filelists/nu_nam_audio_text_pitch_val.txt"

ARGS+=" --dataset-path4 nu_trung_nichi"
ARGS+=" --training-files4 filelists/nu_trung_audio_text_pitch_train.txt"
ARGS+=" --validation-files4 filelists/nu_trung_audio_text_pitch_val.txt"

ARGS+=" -bs $BATCH_SIZE"
ARGS+=" --grad-accumulation $GRAD_ACCUMULATION"
ARGS+=" --optimizer adamw"
ARGS+=" --epochs $EPOCHS"
ARGS+=" --epochs-per-checkpoint $EPOCHS_PER_CHECKPOINT"

ARGS+=" --warmup-steps $WARMUP_STEPS"
ARGS+=" -lr $LEARNING_RATE"
ARGS+=" --weight-decay 1e-6"
ARGS+=" --grad-clip-thresh 1000.0"
ARGS+=" --dur-predictor-loss-scale 0.1"
ARGS+=" --pitch-predictor-loss-scale 0.1"
ARGS+=" --trainloader-repeats 100"
ARGS+=" --validation-freq 1"

# Autoalign & new features
ARGS+=" --kl-loss-start-epoch 0"
ARGS+=" --kl-loss-warmup-epochs $KL_LOSS_WARMUP"
ARGS+=" --text-cleaners $TEXT_CLEANERS"
ARGS+=" --n-speakers $NSPEAKERS"
# ARGS+=" --checkpoint-path $CHECKPOINT"

# Pitch mean and std
ARGS+=" --pitch-mean0 124.157947"
ARGS+=" --pitch-std0 33.519135"

ARGS+=" --pitch-mean1 173.203161"
ARGS+=" --pitch-std1 45.219384"

ARGS+=" --pitch-mean2 189.114275"
ARGS+=" --pitch-std2 59.541185"

ARGS+=" --pitch-mean3 209.345993"
ARGS+=" --pitch-std3 49.83871"

ARGS+=" --pitch-mean4 236.933387"
ARGS+=" --pitch-std4 44.720869"

[ "$AMP" = "true" ]                    && ARGS+=" --amp"
[ "$PHONE" = "true" ]                  && ARGS+=" --p-arpabet 1.0"
[ "$ENERGY" = "true" ]                 && ARGS+=" --energy-conditioning"
[ "$SEED" != "" ]                      && ARGS+=" --seed $SEED"
[ "$LOAD_MEL_FROM_DISK" = true ]       && ARGS+=" --load-mel-from-disk"
[ "$LOAD_PITCH_FROM_DISK" = true ]     && ARGS+=" --load-pitch-from-disk"
[ "$PITCH_ONLINE_DIR" != "" ]          && ARGS+=" --pitch-online-dir $PITCH_ONLINE_DIR"  # e.g., /dev/shm/pitch
[ "$PITCH_ONLINE_METHOD" != "" ]       && ARGS+=" --pitch-online-method $PITCH_ONLINE_METHOD"
[ "$APPEND_SPACES" = true ]            && ARGS+=" --prepend-space-to-text"
[ "$APPEND_SPACES" = true ]            && ARGS+=" --append-space-to-text"
[[ "$ARGS" != *"--checkpoint-path"* ]] && ARGS+=" --resume"

if [ "$SAMPLING_RATE" == "44100" ]; then
  ARGS+=" --sampling-rate 44100"
  ARGS+=" --filter-length 2048"
  ARGS+=" --hop-length 512"
  ARGS+=" --win-length 2048"
  ARGS+=" --mel-fmin 0.0"
  ARGS+=" --mel-fmax 22050.0"

elif [ "$SAMPLING_RATE" != "22050" ]; then
  echo "Unknown sampling rate $SAMPLING_RATE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

: ${DISTRIBUTED:="-m torch.distributed.launch --nproc_per_node $NUM_GPUS"}
python $DISTRIBUTED train_vi_multi.py $ARGS "$@"
