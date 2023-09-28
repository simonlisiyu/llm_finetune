# LLaMA Efficient Tuning

[![GitHub Code License](https://img.shields.io/github/license/hiyouga/LLaMA-Efficient-Tuning)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/hiyouga/LLaMA-Efficient-Tuning)](https://github.com/hiyouga/LLaMA-Efficient-Tuning/commits/main)

👋 加我的[微信](assets/wechat.jpg)。

## 更新日志

[23/09/28]
支持baichuan、llama2、llama、glm2等大模型，支持QLoRA；
支持gpu预览、大模型微调训练、模型合并、部署服务（测试中）；
支持api方式，微调训练、模型合并、模型发布；
增加数据管理，支持上传excel文件；
增加训练脚本管理，支持自定义脚本编辑和训练，支持pt/sft/rm/ppo/dpo训练阶段，支持train/eval/predict任务；
增加模型快速编辑能力，能够编辑指定问题的回答；


## 模型

| 模型名                                                   | 模型大小                     | 默认模块           | Template  |
| -------------------------------------------------------- | --------------------------- | ----------------- | --------- |
| [LLaMA](https://github.com/facebookresearch/llama)       | 7B/13B/33B/65B              | q_proj,v_proj     | -         |
| [LLaMA-2](https://huggingface.co/meta-llama)             | 7B/13B/70B                  | q_proj,v_proj     | llama2    |
| [BLOOM](https://huggingface.co/bigscience/bloom)         | 560M/1.1B/1.7B/3B/7.1B/176B | query_key_value   | -         |
| [BLOOMZ](https://huggingface.co/bigscience/bloomz)       | 560M/1.1B/1.7B/3B/7.1B/176B | query_key_value   | -         |
| [Falcon](https://huggingface.co/tiiuae/falcon-7b)        | 7B/40B                      | query_key_value   | -         |
| [Baichuan](https://github.com/baichuan-inc/Baichuan-13B) | 7B/13B                      | W_pack            | baichuan  |
| [Baichuan2](https://github.com/baichuan-inc/Baichuan2)   | 7B/13B                      | W_pack            | baichuan2 |
| [InternLM](https://github.com/InternLM/InternLM)         | 7B/20B                      | q_proj,v_proj     | intern    |
| [Qwen](https://github.com/QwenLM/Qwen-7B)                | 7B/14B                      | c_attn            | chatml    |
| [XVERSE](https://github.com/xverse-ai/XVERSE-13B)        | 13B                         | q_proj,v_proj     | xverse    |
| [ChatGLM2](https://github.com/THUDM/ChatGLM2-6B)         | 6B                          | query_key_value   | chatglm2  |
| [Phi-1.5](https://huggingface.co/microsoft/phi-1_5)      | 1.3B                        | Wqkv              | -         |



## 软件依赖

- Python 3.10 和 PyTorch 1.13.1
- 🤗Transformers, Datasets, Accelerate, PEFT 和 TRL
- sentencepiece, protobuf 和 tiktoken
- jieba, rouge-chinese 和 nltk (用于评估)
- gradio 和 matplotlib (用于网页端交互)
- uvicorn, fastapi 和 sse-starlette (用于 API)


## 目录说明
- run_server.py              # 启动程序
- main.py              # FastAPI应用程序
- apis/                 # API接口
- config/                 # 配置文件
- docs/                 # 说明文档
- logs/                # 日志目录
- peft-xxx/              # peft
- scripts/             # 训练等脚本
- templates/              # html模板
- test/                # 测试用例



## 项目启动
> python run_server.py

## docker
### 构建镜像
> docker build -t docker.li.com/llm_finetune .
### 运行容器
> docker run --gpus all --network host --ipc host --name llm_finetune -d \
--ulimit memlock=-1 --ulimit stack=67108864 \
-v /data0/service/llm_finetune/config/171.env.yaml:/app/config/env.yaml \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /data0/LLMs:/app/original-weights \
-v /data0/service/llm_finetune/logs:/app/logs \
-v /data0/service/llm_finetune/data:/app/data \
--security-opt seccomp=unconfined \
docker.li.com/llm_finetune

## 服务验证
### web服务
> http://localhost:8088/docs

### 首页
> http://localhost:8088

### 离线项目环境
```shell
docker save docker.li.com/llm_finetune -o ./llm_finetune.img
tar -czvf llm_finetune.img.tgz llm_finetune.img

tar -zxvf llm_finetune.img.tgz
docker load --input llm_finetune.img
docker images
```


### 浏览器测试

```bash
python src/web_demo.py \
    --model_name_or_path path_to_llama_model \
    --template default \
    --finetuning_type lora \
    --checkpoint_dir path_to_checkpoint
```



## 协议

本仓库的代码依照 [Apache-2.0](LICENSE) 协议开源。

使用模型权重时，请遵循对应的模型协议：

- [LLaMA](https://github.com/facebookresearch/llama/blob/main/MODEL_CARD.md)
- [LLaMA-2](https://ai.meta.com/llama/license/)
- [BLOOM](https://huggingface.co/spaces/bigscience/license)
- [Falcon](LICENSE)
- [Baichuan](https://huggingface.co/baichuan-inc/baichuan-7B/resolve/main/baichuan-7B%20%E6%A8%A1%E5%9E%8B%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf)
- [Baichuan2](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base/resolve/main/Baichuan%202%E6%A8%A1%E5%9E%8B%E7%A4%BE%E5%8C%BA%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf)
- [InternLM](https://github.com/InternLM/InternLM#open-source-license)
- [Qwen](https://huggingface.co/Qwen/Qwen-7B-Chat/blob/main/LICENSE)
- [XVERSE](https://github.com/xverse-ai/XVERSE-13B/blob/main/MODEL_LICENSE.pdf)
- [ChatGLM2](https://github.com/THUDM/ChatGLM2-6B/blob/main/MODEL_LICENSE)
- [Phi-1.5](https://huggingface.co/microsoft/phi-1_5/resolve/main/Research%20License.docx)

## 引用

如果您觉得此项目有帮助，请考虑以下列格式引用

```bibtex
@Misc{llama-efficient-tuning,
  title = {LLaMA Efficient Tuning},
  author = {hiyouga},
  howpublished = {\url{https://github.com/hiyouga/LLaMA-Efficient-Tuning}},
  year = {2023}
}
```

## 致谢

本项目受益于 [LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning)，感谢作者的付出。

