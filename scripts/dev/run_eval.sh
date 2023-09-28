#!/bin/bash

model_dir=ChatGLM2-6B
dataset_name=self_cognition
checkpoint_dir=ChatGLM2-6B-self-checkpoint_sft
output_dir=ChatGLM2-6B-self-0917-eval
nnodes=1
nproc=1
master_addr=192.168.1.171
master_port=9910

pretrained_model=/app/original-weights/$model_dir
checkpoint_path=/app/original-weights/${checkpoint_dir}
output_path=/app/original-weights/${output_dir}


stage=sft
template=default
finetuning_type=lora

per_device_eval_batch_size=1
max_samples=100

deepspeed_config_file=dev/ds_config.json

cd /app/scripts && torchrun --nnodes ${nnodes} --nproc_per_node ${nproc} --master_addr ${master_addr} --master_port ${master_port} src/train_bash.py \
    --deepspeed ${deepspeed_config_file} \
    --stage ${stage} \
    --model_name_or_path ${pretrained_model} \
    --do_eval \
    --dataset ${dataset_name} \
    --template ${template} \
    --finetuning_type ${finetuning_type} \
    --checkpoint_dir ${checkpoint_path} \
    --output_dir ${output_path} \
    --overwrite_output_dir \
    --overwrite_cache \
    --per_device_eval_batch_size ${per_device_eval_batch_size} \
    --max_samples ${max_samples} \
    --predict_with_generate
