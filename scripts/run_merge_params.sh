#!/bin/bash

if [ $# -lt 3 ]; then
    echo "wrong params"
    exit 1
fi

base_model=$1
checkpoint_path=$2
output_path=$3
template=$4
finetuning_type=$5

cd scripts && python src/export_model.py \
    --model_name_or_path "${base_model}" \
    --template ${template} \
    --finetuning_type ${finetuning_type} \
    --checkpoint_dir "${checkpoint_path}" \
    --output_dir "${output_path}"
