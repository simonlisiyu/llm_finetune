
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
    2. 将 `$Alita_IP` 替换为alita ip；（如192.168.1.100）
    3. 将 '$BASE_DIR' 替换为本机llm_finetune路径；

   ``` 
   application: 
     ip: '$IP' 
     port: $PORT 
     log_level: 'info'
   worker:
     model_dir: '$MODEL_DIR' 
   trainer:
     base_dir: '$BASE_DIR'

   ``` 

   参考下面的例子：

   ``` 
   application:
   ip: '192.168.1.100'
   port: 8002
   log_level: 'info'
   controller:
   ip: '192.168.1.100'
   port: 23620
   trainer:
   base_dir: '/opt/llm_finetune/'

   ``` 

4. 启动服务
   > python main.py

5. 查看页面
   http://127.0.0.1:8000
