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
task_id=$6

echo python src/export_model.py \
         --task_id ${task_id} \
         --model_name_or_path "${base_model}" \
         --template ${template} \
         --finetuning_type ${finetuning_type} \
         --checkpoint_dir "${checkpoint_path}" \
         --export_dir "${output_path}"

cd scripts && python src/export_model.py \
    --task_id ${task_id} \
    --model_name_or_path "${base_model}" \
    --template ${template} \
    --finetuning_type ${finetuning_type} \
    --checkpoint_dir "${checkpoint_path}" \
    --export_dir "${output_path}"
