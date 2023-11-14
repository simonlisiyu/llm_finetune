import json
from transformers import TrainerCallback
from llmtuner.tuner.client.redis_tools import RedisSingleton
from llmtuner.llmtuner_settings import Settings

llmtuner_settings = Settings()


class MetricCallback(TrainerCallback):
    "A callback that prints a message at the beginning of training"
    def __init__(self, task_id, stage):
        self.task_id = task_id
        self.stage = stage
        redis_instance = RedisSingleton(host=llmtuner_settings.redis_ip,
                                        port=llmtuner_settings.redis_port,
                                        db=llmtuner_settings.redis_db,
                                        password=llmtuner_settings.redis_password)
        self.redis = redis_instance.get_redis()

    def on_log(self, args, state, control, logs=None, **kwargs):
        _ = logs.pop("total_flos", None)
        print("111111111111111111111111state。", state)
        percent_radio = 100 if state.max_steps == 0 else state.global_step * 100 / state.max_steps
        if state.is_local_process_zero:
            metric_data = dict()
            metric_data["task_id"] = self.task_id
            metric_data["train_action"] = self.stage
            metric_data["status"] = 1
            metric_data["percentage"] = percent_radio
            metric_data["metrics"] = logs

            if percent_radio == 100:
                metric_data["status"] = 2

            try:
                self.redis.xadd(llmtuner_settings.ALL_TASK_METRIC_MQ, {metric_data['task_id']: json.dumps(metric_data)})
                print("success xadd to ", llmtuner_settings.ALL_TASK_METRIC_MQ, metric_data)
            except Exception as e:
                print("failed xadd to ",llmtuner_settings.ALL_TASK_METRIC_MQ, e)
