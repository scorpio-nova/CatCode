import glob
import os
import jsonlines
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.JsonlUtils import get_function_header,write_jsonl_file


def construct_translation_functor(dataset, headers, source_language, target_language):
    jsonl_data = []
    input_folder = f'{current_path}/../../data/categorical_data/morphism_output/{dataset}_{source_language}/NoTransform'
    # Read all .java files in the input_folder
    for file_path in glob.glob(os.path.join(input_folder, "*.java")):
        with open(file_path, "r") as f:
            code = f.read()
            task_id = int(file_path.split('/')[-1].split('.')[0].split('_')[0])
            if (dataset == 'humaneval' and task_id in [50,32,38]): ## TODO: this only applies to non-python spilt in humaneval dataset, whose multi-lingual humaneval dataset is missing those 3 indices
                continue
            header = get_function_header(headers, f"{dataset}/"+file_path.split('/')[-1].split('.')[0].split('_')[0])
            print('header: ', header)
            promptText = f"Translate the below {source_language} code to {target_language} code. The function header is {header}. You should only answer the {target_language} function body without further comments and explanations. "
            prompt = promptText + code
            # Create a dictionary with the prompt and canonical_solution
            data = {
                "task_id": task_id,
                "prompt": prompt,
                "model":  model,
                "max_tokens": 500,
            }
            jsonl_data.append(data)
    # sort by task_id
    jsonl_data = sorted(jsonl_data, key=lambda x: x['task_id'])
    # Write the JSONL file
    return jsonl_data

if __name__ == '__main__':
    source_language = "java"
    target_languages = ["python","javascript"]
    datasets = ['humaneval','mathqa','mbxp']
    current_path = os.path.dirname(os.path.abspath(__file__))
    model = 'text-davinci-003'

    for target_language in target_languages:
        for dataset in datasets:
            headerFile = f"{current_path}/../../data/supportive_data/function_headers/" + f"{target_language}_function_headers.jsonl"
            with jsonlines.open(headerFile, 'r') as reader:
                headers = list(reader)
            jsonl_data = construct_translation_functor(dataset, headers, source_language, target_language)
            write_jsonl_file(jsonl_data, f'{current_path}/../../data/task_input/translation-functor/davinci/{dataset}_{source_language}_{target_language}.jsonl')



