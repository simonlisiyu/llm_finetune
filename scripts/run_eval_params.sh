#!/bin/bash

if [ $# -lt 3 ]; then
    echo "wrong params"
    exit 1
fi

echo

model_dir=$1
dataset_name=$2
output_path=$3
template=$4
finetuning_type=$5
gpus=$6
per_device_eval_batch_size=$7
max_samples=$8
task_id=$9

echo CUDA_VISIBLE_DEVICES=$gpus python src/train_bash.py \
                               --task_id ${task_id} \
                               --stage sft \
                               --model_name_or_path ${model_dir} \
                               --do_eval \
                               --dataset ${dataset_name} \
                               --template ${template} \
                               --finetuning_type ${finetuning_type} \
                               --output_dir ${output_path} \
                               --per_device_eval_batch_size ${per_device_eval_batch_size} \
                               --max_samples ${max_samples} \
                               --predict_with_generate

cd scripts && CUDA_VISIBLE_DEVICES=$gpus python src/train_bash.py \
                          --task_id ${task_id} \
                          --stage sft \
                          --model_name_or_path ${model_dir} \
                          --do_eval \
                          --dataset ${dataset_name} \
                          --template ${template} \
                          --finetuning_type ${finetuning_type} \
                          --output_dir ${output_path} \
                          --per_device_eval_batch_size ${per_device_eval_batch_size} \
                          --max_samples ${max_samples} \
                          --predict_with_generate
