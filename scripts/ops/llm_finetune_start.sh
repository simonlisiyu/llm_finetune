docker run --gpus all --network host --ipc host --name llm_finetune -d \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -v /data0/service/llm_finetune/config/171.env.yaml:/app/config/env.yaml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /data0/LLMs:/app/original-weights \
  -v /data0/service/llm_finetune/logs:/app/logs \
  -v /data/lsy/Chinese-LLaMA-Alpaca-main/data:/app/data \
  --security-opt seccomp=unconfined \
  docker.li.com/llm_finetune