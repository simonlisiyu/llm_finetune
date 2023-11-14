
## llm_finetune服务，全新部署或历史版本升级

### 一、环境准备：
1. 代码
   > git clone https://github.com/simonlisiyu/llm_finetune.git
   > 
   > cd llm_finetune
   > 
   > pip install -r requirements.txt
2. 目录准备
   > cd llm_finetune

   创建配置目录`mkdir config`，生成配置文件 `touch config/trainer.yaml`，关联配置文件 `ln -s /opt/llm_finetune/config/trainer.yaml scripts/src/llmtuner/`

   关联数据目录： `ln -s /data data`

   关联大模型目录：`ln -s /llm llm`
3. 修改配置
   > vi config/trainer.yaml

   注意：

    1. 将 `$IP` 替换为本机ip；（如192.168.1.100）
    2. 将 `$BASE_DIR` 替换为本机llm_finetune路径；

   ``` 
   application: 
     ip: '$IP' 
     port: $PORT 
     log_level: 'info'
   trainer:
     base_dir: '$BASE_DIR'

   ``` 

   参考下面的例子：

   ``` 
   application:
     ip: '192.168.1.100'
     port: 8000
     log_level: 'info'
   trainer:
     base_dir: '/opt/llm_finetune/'

   ```

   > vi config/model_info.yaml

   注意：（初始化的大模型需要手动编辑model_info.yaml，后续训练的大模型会自动更新到此文件内，无需再手动编辑）

   1. 将 `$MODEL_NAME` 替换为模型名称；（如chatglm2-6b）
   2. 将 `$MODEL_DIR` 替换为基于BASE_DIR的模型相对路径；（如llm/ChatGLM2-6B）
   3. 将 `$TEMPLATE` 和 `$SIZE` 和 `$DATETIME` 替换为对应的内容；

   ```
   {
     "$MODEL_NAME": {
       "model_path": "$MODEL_DIR",
       "template": "$TEMPLATE",
       "size": "$SIZE",
       "update_at": "$DATETIME"
     }
   }
   ```

   参考下面的例子：

   ```
   {
     "chatglm2-6b": {
       "model_path": "llm/ChatGLM2-6B",
       "template": "chatglm2",
       "size": "6",
       "update_at": "2023-07-06_15:56:28"
     }
   }
   ```

5. 启动服务
   > python main.py

6. 查看页面
   http://127.0.0.1:8000
