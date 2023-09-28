CUDA_VISIBLE_DEVICES=1 python -m fastedit.editor \
    --data example.json \
    --model /data0/LLMs/Chinese-Alpaca-2-7B \
    --config llama-7b \
    --template default \
    --output /data0/LLMs/Chinese-Alpaca-2-7B-edit