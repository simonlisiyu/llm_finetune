# 更新记录

## 2023.10
- update [data_args.py](llmtuner%2Fhparams%2Fdata_args.py)llmtuner/hparams/data_args.py
    ```
    dataset_dir: Optional[str] = field(
            default=llmtuner_settings.dataset_info_path,
            metadata={"help": "The name of the folder containing datasets."}
        )
    ```
- update [finetuning_args.py](llmtuner%2Fhparams%2Ffinetuning_args.py)
    ```
    task_id: Optional[str] = field(
            default="task_id123",
            metadata={"help": "Task ID for The Job Task"}
        )
    ```
- add [redis_tools.py](llmtuner%2Ftuner%2Fclient%2Fredis_tools.py)
- add [metric_callback.py](llmtuner%2Ftuner%2Fcore%2Fmetric_callback.py)
- update [workflow.py](llmtuner%2Ftuner%2Fsft%2Fworkflow.py)
    ```
        # Initialize our Trainer
        if training_args.do_train:
            callbacks = [MetricCallback(task_id=finetuning_args.task_id, stage=0)]
        if training_args.do_eval:
            callbacks = [MetricCallback(task_id=finetuning_args.task_id, stage=1)]
        if training_args.do_predict:
            callbacks = [MetricCallback(task_id=finetuning_args.task_id, stage=3)]
        trainer = CustomSeq2SeqTrainer(
            model=model,
            args=training_args,
            tokenizer=tokenizer,
            data_collator=data_collator,
            callbacks=callbacks,
            compute_metrics=ComputeMetrics(tokenizer) if training_args.predict_with_generate else None,
            **split_dataset(dataset, data_args, training_args)
        )
    ...
        
    
            try:
                r.hset(llmtuner_settings.TRAIN_TASK_RESULT_KEY, finetuning_args.task_id, str(train_result.metrics))
                print("success put hset ", llmtuner_settings.TRAIN_TASK_RESULT_KEY, finetuning_args.task_id)
            except Exception as e:
                print("failed put hset ", llmtuner_settings.TRAIN_TASK_RESULT_KEY, e)
                
    ...
    
            try:
                r.hset(llmtuner_settings.EVAL_TASK_RESULT_KEY, finetuning_args.task_id, str(metrics))
                print("success put hset ", llmtuner_settings.EVAL_TASK_RESULT_KEY, finetuning_args.task_id)
            except Exception as e:
                print("failed put hset ", llmtuner_settings.EVAL_TASK_RESULT_KEY, e)
    ```
- add [llmtuner.yaml](llmtuner%2Fllmtuner.yaml)
- add [llmtuner_settings.py](llmtuner%2Fllmtuner_settings.py)
- update [run_sft_params.sh](..%2Frun_sft_params.sh)
- update [run_merge_params.sh](..%2Frun_merge_params.sh)
- add [run_eval_params.sh](..%2Frun_eval_params.sh)

## 2023.9
- update llmtuner/hparams/data_args.py
```
dataset: Optional[str] = field(
default="self_cognition",
metadata={"help": "The name of provided dataset(s) to use. Use commas to separate multiple datasets."}
)
dataset_dir: Optional[str] = field(
default="/app/data",
metadata={"help": "The name of the folder containing datasets."}
)
```

- 2023.9.17 git pull
