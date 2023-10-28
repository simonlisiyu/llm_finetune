#!/bin/bash

echo $#
if [ $# -lt 4 ]; then
  echo 'Useage: sh localai_worker_start.sh $name $port $model $show_name'
  exit 1
fi

name=$1
port=$2
model=$3
model_name=$4
gpu=$5
int8=$6

if [ -z ${gpu} ]; then
  gpu=0
fi

if [ -n "${int8}" ]; then
  int8="--load-8bit"
fi

echo "docker run --gpus all -d --name ${name} -p ${port}:23621 -v /data0/LLMs:/LLMs/ docker.art.haizhi.com/dmc/alita poetry run python3 -m localai.worker --model-path /LLMs/${model} --model-names ${model_name} --worker http://192.168.1.171:${port} --controller http://192.168.1.171:23620 --gpus ${gpu} --limit-model-concurrency 1 ${int8}"