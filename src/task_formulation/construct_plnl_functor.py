import json
import glob
import os

def construct_plnl_functor(input_folder, sourceLanguage):
    jsonl_data = []

    # Read all .java files in the input_folder
    for file_path in glob.glob(os.path.join(input_folder, "*.java")):
        with open(file_path, "r") as f:
            code = f.read()
            task_id = int(file_path.split('/')[-1].split('.')[0].split('_')[0])
            prompt = f"Please describe the following code written in {sourceLanguage} using natural language. " \
                     "Your description should include the exact function name, its arguments, and the return type. " \
                     "Additionally, provide enough details such as variable initialization to allow someone to reproduce the code based on your explanation."\
                     f"\n'''\n{code}\n'''"
            data = {
                "task_id": task_id,
                "prompt": prompt,
                "model": model,
                "max_tokens": 500,
            }
            jsonl_data.append(data)
    jsonl_data = sorted(jsonl_data, key=lambda x: x['task_id'])
    return jsonl_data


if __name__ == '__main__':
    datasets = ['humaneval','mathqa','mbxp']
    sourceLanguage = "java"
    current_path = os.path.dirname(os.path.abspath(__file__))
    model = "text-davinci-003"
    for dataset in datasets:
        input_path = f'{current_path}/../../data/categorical_data/morphism_output/{dataset}_{sourceLanguage}/NoTransform'
        jsonl_data = construct_plnl_functor(input_path, sourceLanguage)
        output_file = f'{current_path}/../../data/task_input/explanation-functor/davinci/{dataset}_java_nl.jsonl'
        # Write the JSONL file
        with open(output_file, "w") as f:
            for data in jsonl_data:
                f.write(json.dumps(data))
                f.write("\n")
        print(f"constructed plnl functor for {dataset}")