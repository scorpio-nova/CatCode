#!/bin/bash

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
TASK_FORMULATION_DIR="$DIR/../src/task_formulation/"
MODEL_INPUT_DIR="$DIR/../data/task_input"

datasets=('humaneval' 'mathqa' 'mbxp')
tasks=('translation' 'translation' 'explanation')
task_suffixes=('_javascript' '_python' '_nl')
source_language='java'

#### construct input for openai models ####
## text-davinci-003 ##
# identify local morphism
#python "$TASK_FORMULATION_DIR/construct_local_morphism.py" ## todo: refactor
# identify global morphism
python "$TASK_FORMULATION_DIR/construct_global_morphism.py"
# translation functor
python "$TASK_FORMULATION_DIR/construct_plpl_functor.py"
# explanation functor
python "$TASK_FORMULATION_DIR/construct_plnl_functor.py"

## gpt-turbo-3.5 ##

# identify local morphism
#python "$TASK_FORMULATION_DIR/construct_local_morphism.py" ## todo: refactor
# global morphism
python "$TASK_FORMULATION_DIR/transform_completion_jsonl_to_chat.py" \
      --input_jsonl_file "$MODEL_INPUT_DIR/morphism-identify/davinci/code_contest.jsonl" \
      --output_jsonl_file "$MODEL_INPUT_DIR/morphism-identify/chatgpt/code_contest.jsonl" || exit 1

for dataset in "${datasets[@]}"
do
    for ((i=1; i<=${#tasks[@]}; i++))
    do
        task="${tasks[$i]}"
        suffix="${task_suffixes[$i]}"
        python "$TASK_FORMULATION_DIR/transform_completion_jsonl_to_chat.py" \
        --input_jsonl_file "$MODEL_INPUT_DIR/${task}-functor/davinci/${dataset}_${source_language}${suffix}.jsonl" \
        --output_jsonl_file "$MODEL_INPUT_DIR/${task}-functor/chatgpt/${dataset}_${source_language}${suffix}.jsonl" || exit 1
    done
done


# reproduction functor
python "$TASK_FORMULATION_DIR/construct_nlpl_functor.py" --model_name chatgpt || exit 1
python "$TASK_FORMULATION_DIR/construct_nlpl_functor.py" --model_name davinci || exit 1


