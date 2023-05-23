#!/bin/bash

# Get the directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
MODEL_OUTPUT_DIR="$DIR/../data/task_output"
MODEL_API_DIR="$DIR/../src/modelAPI"
TEST_API_DIR="$DIR/../src/testAPI"



## process model's output
datasets=('humaneval' 'mathqa' 'mbxp')
tasks=('translation' 'translation'  'reproduction')
task_prefixes=('' '' 'nl_')
task_suffixes=('_javascript' '_python' '')
source_language='java'
target_languages=('javascript' 'python' 'java')

#
## openai response code extraction (e.g. text-davinci)
#for dataset in "${datasets[@]}"
#do
#    for ((i=1; i<=${#tasks[@]}; i++))
#    do
#        task="${tasks[$i]}"
#        prefix="${task_prefixes[$i]}"
#        suffix="${task_suffixes[$i]}"
#        language="${target_languages[$i]}"
#
#        echo "processing: $MODEL_OUTPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}_results.jsonl"
#        echo "output to:  $MODEL_OUTPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}_results_code.jsonl"
#        python "$MODEL_API_DIR/openai-api/openai_response_code_extractor.py" \
#        --input_file "$MODEL_OUTPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}_results.jsonl" \
#        --output_file "$MODEL_OUTPUT_DIR/${task}-functor/davinci/${dataset}_${prefix}${source_language}${suffix}_results_code.jsonl" \
#        --language "$language" \
#        --dataset "$dataset" || exit 1
#    done
#done
#

MXEVAL_SCRIPT_DIR="$DIR/../plugins/mbxp-exec-eval/mxeval"

## run tests （e.g.)
## it's suggested to run them
# translation task: codegeex python humaneval
#echo "python ${MXEVAL_SCRIPT_DIR}/evaluate_functional_correctness.py" "${MODEL_OUTPUT_DIR}/translation-functor/codegeex/humaneval_Java-Python.jsonl" --problem_file "${MXEVAL_SCRIPT_DIR}/../data/multilingual_humaneval/HumanEval.jsonl"
#python "${MXEVAL_SCRIPT_DIR}/evaluate_functional_correctness.py" "$MODEL_OUTPUT_DIR/translation-functor/codegeex/humaneval_Java-Python.jsonl" --problem_file "${MXEVAL_SCRIPT_DIR}/../data/multilingual_humaneval/HumanEval.jsonl"
## translation task: davinci javascript mathqa
python "${MXEVAL_SCRIPT_DIR}/evaluate_functional_correctness.py" "$MODEL_OUTPUT_DIR/translation-functor/davinci/mathqa_java_javascript_results_code.jsonl" --problem_file "${MXEVAL_SCRIPT_DIR}/../data/multilingual_mathqa/mathqa-test-javascript_v1.jsonl"
## reproduction task: chatgpt java mbxp
#python "${MXEVAL_SCRIPT_DIR}/evaluate_functional_correctness.py" "$MODEL_OUTPUT_DIR/reproduction-functor/chatgpt/mbxp_java_results_code.jsonl" --problem_file "${MXEVAL_SCRIPT_DIR}/../data/mbxp/mbjp_release_v1.jsonl"
