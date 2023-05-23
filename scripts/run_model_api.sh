#!/bin/bash

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
MODEL_API_DIR="$DIR/../src/modelAPI"
MODEL_INPUT_DIR="$DIR/../data/task_input"
MODEL_OUTPUT_DIR="$DIR/../data/task_output"


datasets=('humaneval' 'mathqa' 'mbxp')
tasks=('translation' 'translation' 'explanation' 'reproduction')
task_prefixes=('' '' '' 'nl_')
task_suffixes=('_javascript' '_python' '_nl' '')
source_language='java'

# openai api
## ** OPENAI_API_KEY IS NEEDED **
for dataset in "${datasets[@]}"
do
    for ((i=1; i<=${#tasks[@]}; i++))
    do
        task="${tasks[$i]}"
        prefix="${task_prefixes[$i]}"
        suffix="${task_suffixes[$i]}"
        echo $task
        ## chatgpt api
        python "$MODEL_API_DIR/openai-api/api_request_parallel_processor.py" \
        --requests_filepath "$MODEL_INPUT_DIR/${task}-functor/chatgpt/${dataset}_${prefix}${source_language}${suffix}.jsonl" \
        --save_filepath "$MODEL_OUTPUT_DIR/${task}-functor/chatgpt/${dataset}_${prefix}${source_language}${suffix}_results.jsonl" \
        --request_url "https://api.openai.com/v1/chat/completions" || exit 1
        ## davinci api
        python "$MODEL_API_DIR/openai-api/api_request_parallel_processor.py" \
        --requests_filepath "$MODEL_INPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}.jsonl" \
        --save_filepath "$MODEL_OUTPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}_results.jsonl" \
        --request_url "https://api.openai.com/v1/completions"|| exit 1
    done
done


## codegeex
## ** CODEGEEX_API_KEY IS NEEDED **
python "$MODEL_API_DIR/codegeex-api/api_request_translation_functor.py"  ## todo: refactor
