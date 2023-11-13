
## llm_finetune服务，全新部署或历史版本升级

### 一、环境准备：
1. 代码
   > git clone https://github.com/simonlisiyu/llm_finetune.git
   > cd llm_finetune
   > pip install -r requirements.txt
2. 目录准备
   > cd llm_finetune

   创建目录`mkdir config`

   关联数据目录： `ln -s /opt/haizhi/common/data/dataset`

   关联大模型目录：`ln -s /opt/haizhi/common/data/llm`
3. 修改配置
   > vi config/trainer.yaml

   注意：

    1. 将 `$IP` 替换为本机ip；（如192.168.1.171）
    2. 将 `$Alita_IP` 替换为alita ip；（如192.168.1.171）
    3. 将 '$MODEL_DIR' 替换为本机大模型路径；
    4. 将 REDIS等在需要将监控metric上报时才需要填写；（不用则无需关注）

   ``` 
   application: 
     ip: '$IP' 
     port: $PORT 
     log_level: 'info' 
   controller:
     ip: '$Alita_IP' 
     port: $Alita_PORT 
   worker:
     model_dir: '$MODEL_DIR' 
   trainer: 
     ports: [9901, 9902, 9903, 9904, 9905, 9906, 9907, 9908, 9909, 9910] 
     base_dir: '/app' 
     data_dir: 'data/' 
     model_dir: 'llm/' 
     log_dir: 'logs/' 
     dev_script_dir: 'scripts/dev/' 
     data_file: "data/dataset_info.json" 
     model_file: "llm/model_info.json" 
     finetune_checkpoint: "sft_checkpoint" 
     max_node_num: '1' 
     max_process_num: '1' 
   redis: 
     ip: '$REDIS_IP' 
     port: $REDIS_PORT 
     password: '$REDIS_PASSWORD' 

   ``` 

   参考下面的例子：

   ``` 
   application:
     ip: '192.168.1.171'
     port: 8000
     log_level: 'info'
   controller:
     ip: '192.168.1.171'
     port: 23620
   worker:
     model_dir: '/data/s3/llm/'
   trainer:
     ports: [9901, 9902, 9903, 9904, 9905, 9906, 9907, 9908, 9909, 9910]
     base_dir: '/data/s3/'
     data_dir: 'data/'
     model_dir: 'llm/'
     log_dir: 'logs/'
     dev_script_dir: 'scripts/dev/'
     data_file: "data/dataset_info.json"
     model_file: "config/model_info.json"
     finetune_checkpoint: "sft_checkpoint"
     max_node_num: '1'
     max_process_num: '1'
   redis:
     ip: '192.168.1.167'
     port: 6679
     password: '123'

   ``` 

4. 启动服务
   > python main.py

5. 查看页面
   http://127.0.0.1:8000
