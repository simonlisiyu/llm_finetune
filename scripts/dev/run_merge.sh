#!/bin/bash

base_model=ChatGLM2-6B
checkpoint_dir=ChatGLM2-6B-self-checkpoint_sft
output_dir=ChatGLM2-6B-self-0917

base_model=/app/original-weights/$base_model
checkpoint_path=/app/original-weights/$checkpoint_dir
output_path=/app/original-weights/$output_dir

template=default

cd /app/scripts && python src/export_model.py \
    --model_name_or_path "${base_model}" \
    --template ${template} \
    --finetuning_type lora \
    --checkpoint_dir "${checkpoint_path}" \
    --output_dir "${output_path}"
