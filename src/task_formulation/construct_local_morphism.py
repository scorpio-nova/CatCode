import os
import json
import openai
from typing import List
from utils.JsonUtils import read_json


def read_json(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


valid_eq_types = ["BooleanExchange", "LoopExchange", "PermuteStatement", "ReorderCondition", "SwitchToIf", "UnusedStatement", "VariableRenaming"]
valid_uneq_types = ["ModifyCondition", "RemoveElse"]

def get_valid_pairs(types: List[str]):
    source_type = "NoTransform"
    eq_types = [t for t in types if t in valid_eq_types]
    uneq_types = [t for t in types if t in valid_uneq_types]
    source_eq_pairs = [(source_type, t) for t in eq_types]
    source_uneq_pairs = [(source_type, t) for t in uneq_types]
    eq_eq_pairs = [(eq_types[i], eq_types[j]) for i in range(len(eq_types)) for j in range(i+1, len(eq_types))]
    return source_eq_pairs + source_uneq_pairs + eq_eq_pairs

def call_model_api(prompt:str, model:str):
    if model == 'text-davinci-003':
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=0
        )
    elif model == 'gpt-3.5-turbo':
        response = openai.ChatCompletion.create(
            model=model,
            prompt=prompt,## todo: it should be messages here
            temperature=0
        )
    else: raise ValueError("model_undefined",model)
    return response

def main():
    # create a dictionary to store all data
    output_data_dict = {}
    model = 'text-davinci-003'
    try:
        # select dataset and prompt type
        dataset_idx = 2
        config = read_json(os.path.join(os.path.dirname(__file__)+"/../../", "config/config.json"))
        print("config: ", config)

        # read configs
        datasets = config['datasets']
        morphism_input_path = config['morphismInputPath']
        morphism_output_path = config['morphismOutputPath']

        # read input data
        dataset = datasets[dataset_idx]
        json_data = read_json(os.path.join(morphism_input_path, f"{dataset}.json"))
        data_keys = sorted(json_data.keys(), key=lambda x: int(x.split('-')[1]))
        print("data_keys: ", data_keys)

        # config api and prompts
        prompt_text = "If two pieces of code always have the same output for the same input, we say they have the " \
                      "same function. Read code A and code B below, if they have the same function? Answer \"Ture.\" " \
                      "or \"False.\"\n "
        openai.api_key = config['OPENAI_API_KEY'] or ""

        # loop for each data
        for data_key in data_keys:
            # code to be executed for each data
            print("processing data: ", data_key)
            idx = int(data_key.split('-')[1])
            data = json_data[data_key]
            keys = list(data.keys())
            pairs = get_valid_pairs(keys)
            print("pairs: ", pairs)
            for pair in pairs:
                for repeat in range(1):
                    reference_code = data[pair[0]]
                    compared_code = data[pair[1]]
                    prompt = prompt_text + 'code A:\n' + reference_code + 'code B:\n' + compared_code
                    response = call_model_api(prompt,model)
                    text = response['choices'][0]['text']
                    # create the file path
                    file_path = f"{morphism_output_path}/{dataset}/{idx}-{pair[0]}-{pair[1]}_{repeat}.txt"
                    # write the data to the file
                    with open(file_path, "w") as f:
                        f.write(text)
                    # add the data to the dictionary
                    output_data_dict[file_path] = data
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()


