#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$SCRIPT_DIR/.."

if [ ! -d "$ROOT_DIR/data/categorical_data/formatted_data" ]; then
  mkdir "$ROOT_DIR/data/categorical_data/formatted_data" || exit 1
fi

### Mxeval Dataset ###
# preprocess for python, java, javascript
python ../src/data_definition/reformat_mxeval.py --language python || exit 1
python ../src/data_definition/reformat_mxeval.py --language java || exit 1
python ../src/data_definition/reformat_mxeval.py --language javascript || exit 1

### HumanEval-X Dataset ###
# preprocess for java
cp "../data/raw_data/humanevalx_java.jsonl" "../data/categorical_data/formatted_data/humanevalx_extracted_java.jsonl"

### Code Contest Dataset ###
python ../src/data_definition/reformat_code_contest.py
