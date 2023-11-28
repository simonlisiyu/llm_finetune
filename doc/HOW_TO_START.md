
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

   修改配置文件 `config/trainer.yaml`，按需修改配置文件 `config/model_info.json`

3. 修改配置
   > vi config/trainer.yaml

   注意：

    1. 将 `$IP` 替换为本机ip；（如192.168.1.100）
    2. 将 `$BASE_DIR` 替换为本机llm_finetune绝对路径；（如/opt/llm_finetune）

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
   2. 将 `$MODEL_DIR` 替换为基于BASE_DIR的模型路径；（如ChatGLM2-6B）
   3. 将 `$TEMPLATE` 和 `$SIZE` 和 `$DATETIME` 替换为对应的内容；

   ```
   {
     "$MODEL_NAME": {
       "model_path": llm/"$MODEL_DIR",
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
     }，
     "chatglm3-6b": {
       "model_path": "llm/ChatGLM3-6B",
       "template": "chatglm3",
       "size": "6",
       "update_at": "2023-07-06_15:56:28"
     }
   }
   ```

5. 启动服务
   "Usage: run.sh [start|stop|restart] [llm_dir]"
   llm_dir为选填（会自动软链接ln）
   > sh bin/run.sh start /data/LLMs
   or 
   > sh bin/run.sh start

7. 查看页面
   http://$IP:8000
