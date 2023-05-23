#!/bin/bash

python ../src/data_definition/jsonl_to_programs.py

# use java transformer to transform the dataset
sh ../plugins/JavaTransformer/run.sh || exit 1
# collect raw and transformed data
python ../src/data_definition/merge_raw_and_transformed.py || exit 1
# sample data
python ../src/data_definition/sample_transformed_programs.py || exit 1