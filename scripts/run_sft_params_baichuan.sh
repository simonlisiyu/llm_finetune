#!/bin/bash

echo $#
echo $1
if [ $# -lt 9 ]; then
    echo "wrong params"
    exit 1
fi

# params
model_dir=$1
pretrained_model=/app/original-weights/$model_dir
dataset_name=$2
num_train_epochs=$3
output_dir=$4
output_path=/app/original-weights/${output_dir}
stage=sft
template=baichuan
finetuning_type=lora
lora_target="W_pack"
logging_steps=10
save_steps=1000

# default params
nnodes=$5
if [ -z "$nnodes" ]; then
  nnodes=1
fi
nproc=$6
if [ -z "$nproc" ]; then
  nproc=1
fi
master_addr=$7
master_port=${8}
gpus=${9}
if [ -z "$gpus" ]; then
  gpus=0
fi
lr=${10}
if [ -z "$lr" ]; then
  lr=3e-4
fi
per_device_train_batch_size=${11}
if [ -z "$per_device_train_batch_size" ]; then
  per_device_train_batch_size=1
fi
gradient_accumulation_steps=${12}
if [ -z "$gradient_accumulation_steps" ]; then
  gradient_accumulation_steps=1
fi
lr_scheduler_type=${13}
if [ -z "$lr_scheduler_type" ]; then
  lr_scheduler_type=cosine
fi

# additional params
quantization_bit=${14}
if [ -n "$quantization_bit" ]; then
  quantization_bit="--quantization_bit 4"
fi
max_source_length=${15}
if [ -n "$max_source_length" ]; then
  max_source_length="--max_source_length 512"
fi
max_target_length=${16}
if [ -n "$max_target_length" ]; then
  max_target_length="--max_target_length 512"
fi
max_samples=${17}
if [ -n "$max_samples" ]; then
  max_samples="--max_samples 512"
fi

deepspeed_config_file=ds_zero2_no_offload.json

cd /app/scripts && CUDA_VISIBLE_DEVICES=$gpus torchrun --nnodes ${nnodes} --nproc_per_node ${nproc} --master_addr ${master_addr} --master_port ${master_port} src/train_bash.py \
    --deepspeed ${deepspeed_config_file} \
    --stage ${stage} \
    --model_name_or_path ${pretrained_model} \
    --do_train \
    --dataset ${dataset_name} \
    --template ${template} \
    --finetuning_type ${finetuning_type} \
    --lora_target ${lora_target} \
    --output_dir ${output_path} \
    --overwrite_output_dir \
    --overwrite_cache \
    --per_device_train_batch_size ${per_device_train_batch_size} \
    --gradient_accumulation_steps ${gradient_accumulation_steps} \
    --lr_scheduler_type ${lr_scheduler_type} \
    --logging_steps ${logging_steps} \
    --save_steps ${save_steps} \
    --learning_rate ${lr} \
    --num_train_epochs ${num_train_epochs} \
    --plot_loss \
    ${quantization_bit} \
    ${max_source_length} \
    ${max_target_length} \
    ${max_samples} \
    --fp16