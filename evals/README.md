
## Install Requirements

```
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

or build environment with make command in root


## Run Eval

```
# Download the dataset
python -m embedding.cli download --config config/embedding_eval.yaml

```
# Prepare the test data
```
python -m embedding.cli prepare --config config/embedding_eval.yaml
```

# Run the evaluation
```
python -m embedding.cli evaluate \
    --config config/embedding_eval.yaml \
    --output results/embedding_benchmarks/results.csv -v
```


```
pytest embedding/tests/ -v --cov=embedding
```