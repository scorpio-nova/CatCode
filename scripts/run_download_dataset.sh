#!/bin/bash

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# create the plugins dir if it doesn't exist
if [ ! -d "$DIR/../plugins" ]; then
  mkdir "$DIR/../plugins" || exit 1
fi

# Download mxeval benchmark & datasets (mbxp, humaneval, mathqa)
if [ ! -d "$DIR/../plugins/mxeval" ]; then
  # Clone mxeval repository if it doesn't exist
  git clone https://github.com/amazon-science/mxeval.git || exit 1
  mv mxeval "$DIR/../plugins" || exit 1
fi

# Copy data from mxeval to datasets
cp -r "$DIR/../plugins/mxeval/data" "$DIR/../data" || exit 1
#
## Rename the data directory to raw_data
mv "$DIR/../data/data" "$DIR/../data/raw_data" || exit 1

# Download humaneval-x dataset split of java
if [ ! -f "$DIR/../data/raw_data/humanevalx_java.json" ]; then
  wget https://huggingface.co/datasets/THUDM/humaneval-x/raw/main/data/java/data/humaneval.jsonl -P "$DIR/../data/raw_data"
  mv "$DIR/../data/raw_data/humaneval.jsonl" "$DIR/../data/raw_data/humanevalx_java.jsonl" || exit 1
fi

# Download code_contest dataset
if [ ! -d "$DIR/../data/raw_data/code_contest" ]; then
  mkdir "$DIR/../data/raw_data/code_contest" || exit 1
  wget "https://huggingface.co/datasets/deepmind/code_contests/blob/main/data/test-00000-of-00001-9c49eeff30aacaa8.parquet" -P "$DIR/../data/raw_data/code_contest" || exit 1
fi

## All steps completed successfully
echo "Finished! All datasets have been downloaded successfully."
