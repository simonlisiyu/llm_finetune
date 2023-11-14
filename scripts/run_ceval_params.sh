#!/bin/bash

if [ $# -lt 3 ]; then
    echo "wrong params"
    exit 1
fi

echo

gpus=$1
task_id=$2
model_dir=$3
finetuning_type=$4
template=$5
eval_type=$6
data_split=$7
lang=$8
n_shot=${9}
batch_size=${10}


echo CUDA_VISIBLE_DEVICES=$gpus python src/evaluate.py \
                       --task_id ${task_id} \
                       --model_name_or_path ${model_dir} \
                       --finetuning_type ${finetuning_type} \
                       --template ${template} \
                       --task ${eval_type} \
                       --split ${data_split} \
                       --lang ${lang} \
                       --n_shot ${n_shot} \
                       --batch_size ${batch_size}

cd scripts && CUDA_VISIBLE_DEVICES=$gpus python src/evaluate.py \
                  --task_id ${task_id} \
                  --model_name_or_path ${model_dir} \
                  --finetuning_type ${finetuning_type} \
                  --template ${template} \
                  --task ${eval_type} \
                  --split ${data_split} \
                  --lang ${lang} \
                  --n_shot ${n_shot} \
                  --batch_size ${batch_size}
