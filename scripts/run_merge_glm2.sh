#!/bin/bash

if [ $# -lt 3 ]; then
    echo "wrong params"
    exit 1
fi

base_model=$1
checkpoint_dir=$2
output_dir=$3

base_model=/app/original-weights/$base_model
checkpoint_path=/app/original-weights/$checkpoint_dir
output_path=/app/original-weights/$output_dir

template=chatglm2

cd scripts && python src/export_model.py \
    --model_name_or_path "${base_model}" \
    --template ${template} \
    --finetuning_type lora \
    --checkpoint_dir "${checkpoint_path}" \
    --output_dir "${output_path}"
