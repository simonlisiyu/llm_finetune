# LLM Finetune 网页格式一键式的全流程平台，包括数据上传、微调训练、模型合并、模型部署服务等，无需python和shell开发


[![GitHub Code License](https://img.shields.io/github/license/simonlisiyu/llm_finetune)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/simonlisiyu/llm_finetune)](https://github.com/simonlisiyu/llm_finetune/commits/main)

👋 加我的[微信](wechat.jpg)。

## 更新日志

[23/11/14]
配置进一步精简，基本0配置启动；
支持chatglm3, qwen, intern, xverse, mistral；
支持大模型评估，支持C-EVAL、MMLU、CMMLU；
训练和合并支持指定checkpoint路径；
系统监控增加gpu进程和docker匹配；

[23/10/28]
代码重构，支持整体代码整合到alita-trainer里；
yaml配置文件精简规整，多模型的训练、合并脚本合并统一；
模型部署服务bug修复；
支持大模型评估，支持BLEU-4、ROUGE-1/2/L；
支持微调训练后的大模型作为训练模型再训练；
系统监控除gpu，支持cpu、mem和disk监控；

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
| [Baichuan](https://github.com/baichuan-inc/Baichuan-13B) | 7B/13B                      | W_pack            | baichuan  |
| [Baichuan2](https://github.com/baichuan-inc/Baichuan2)   | 7B/13B                      | W_pack            | baichuan2 |
| [BLOOM](https://huggingface.co/bigscience/bloom)         | 560M/1.1B/1.7B/3B/7.1B/176B | query_key_value   | -         |
| [BLOOMZ](https://huggingface.co/bigscience/bloomz)       | 560M/1.1B/1.7B/3B/7.1B/176B | query_key_value   | -         |
| [ChatGLM3](https://github.com/THUDM/ChatGLM3)            | 6B                          | query_key_value   | chatglm3  |
| [Falcon](https://huggingface.co/tiiuae/falcon-7b)        | 7B/40B/180B                 | query_key_value   | falcon    |
| [InternLM](https://github.com/InternLM/InternLM)         | 7B/20B                      | q_proj,v_proj     | intern    |
| [LLaMA](https://github.com/facebookresearch/llama)       | 7B/13B/33B/65B              | q_proj,v_proj     | -         |
| [LLaMA-2](https://huggingface.co/meta-llama)             | 7B/13B/70B                  | q_proj,v_proj     | llama2    |
| [Mistral](https://huggingface.co/mistralai)              | 7B                          | q_proj,v_proj     | mistral   |
| [Phi-1.5](https://huggingface.co/microsoft/phi-1_5)      | 1.3B                        | Wqkv              | -         |
| [Qwen](https://github.com/QwenLM/Qwen)                   | 7B/14B                      | c_attn            | qwen      |
| [XVERSE](https://github.com/xverse-ai)                   | 7B/13B/65B                  | q_proj,v_proj     | xverse    |



## 软件依赖

- Python 3.10 和 PyTorch 1.13.1
- 🤗Transformers, Datasets, Accelerate, PEFT 和 TRL
- sentencepiece, protobuf 和 tiktoken
- jieba, rouge-chinese 和 nltk (用于评估)
- gradio 和 matplotlib (用于网页端交互)
- uvicorn, fastapi 和 sse-starlette (用于 API)


## 目录说明
- main.py              # FastAPI应用程序
- bin/                 # 程序脚本
- config/                 # 配置文件
- data                 # 数据文件
- doc/                 # 文档
- lib/                 # 额外依赖
- llm/                 # 大模型权重
- logs/                # 日志目录
- scripts/             # 训练脚本
- templates/           # html模板
- trainer/                # 应用代码
    - api/                 # api
    - model/                 # 对象
    - service/                 #服务
    - settings.py                 #配置


## 项目启动

https://github.com/simonlisiyu/llm_finetune/blob/main/doc/HOW_TO_START.md

## 项目使用

https://github.com/simonlisiyu/llm_finetune/blob/main/doc/HOW_TO_USE.md

## 配置文件
- config/trainer.yaml  # 服务配置文件
- scripts/src/llmtuner/llmtuner_settings # 训练脚本配置文件
- config/model_info.json  # 模型配置文件
- data/dataset_info.json  # 数据集配置文件

### 配置文件注意：base_dir等修改正确。
### 环境注意：启动会依赖环境，目录及文件需要提前创建好。

## docker
待测试后补充


## 服务验证
### web服务
> http://localhost:8000/docs

### 首页
> http://localhost:8000




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


## 致谢

本项目受益于 [LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning)，感谢作者的付出。

