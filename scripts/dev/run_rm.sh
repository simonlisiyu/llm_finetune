#!/bin/bash

model_dir=ChatGLM2-6B
dataset_name=self_cognition
num_train_epochs=10
output_dir=ChatGLM2-6B-self-checkpoint-rm
nnodes=1
nproc=1
master_addr=192.168.1.171
master_port=9910

pretrained_model=/app/original-weights/$model_dir
output_path=/app/original-weights/${output_dir}

stage=rm
template=default
finetuning_type=lora
lora_target="query_key_value"

lr=3e-4
per_device_train_batch_size=1
gradient_accumulation_steps=1
logging_steps=10
save_steps=1000

deepspeed_config_file=dev/ds_config.json

cd /app/scripts && torchrun --nnodes ${nnodes} --nproc_per_node ${nproc} --master_addr ${master_addr} --master_port ${master_port} src/train_bash.py \
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
    --lr_scheduler_type cosine \
    --logging_steps ${logging_steps} \
    --save_steps ${save_steps} \
    --learning_rate ${lr} \
    --num_train_epochs ${num_train_epochs} \
    --plot_loss \
    --fp16
