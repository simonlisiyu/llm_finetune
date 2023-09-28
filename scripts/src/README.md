update llmtuner/hparams/data_args.py
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
