# blackjack
## install dependency
```bash
poetry config virtualenvs.in-project true
poetry shell
poetry install # according to poetry.lock not pyproject.toml
```
## poetry common usage
```bash
poetry add xxx
poetry add --dev xxx # add dev package
poetry remove
poetry lock # use it when pyproject.toml is manually updated
poetry export -f requirements.txt -o requirements.txt --without-hashes
poetry export -f requirements.txt -o requirements.txt --without-hashes --dev # toml to requirement with dev
```