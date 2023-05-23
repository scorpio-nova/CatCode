import json
import requests
import os
from typing import List

'''
Code Translation
'''
API_KEY = ""  # Get from Tianqi console. 从控制台获取
API_SECRET = ""  # Get from Tianqi console. 从控制台获取

SRC_LANG = "Java"
DST_LANG = "Python"
request_url = "https://tianqi.aminer.cn/api/v2/"
api = 'multilingual_code_translate'

# 指定请求参数格式为json
headers = {'Content-Type': 'application/json'}
request_url = request_url + api

valid_eq_types = ["BooleanExchange", "LoopExchange", "PermuteStatement", "ReorderCondition", "SwitchToIf", "UnusedStatement", "VariableRenaming"]
valid_uneq_types = ["ModifyCondition", "RemoveElse"]

def read_json(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = json.load(f)
    return data



def get_valid_pairs(types: List[str]):
    source_type = "NoTransform"
    eq_types = [t for t in types if t in valid_eq_types]
    uneq_types = [t for t in types if t in valid_uneq_types]
    source_eq_pairs = [(source_type, t) for t in eq_types]
    source_uneq_pairs = [(source_type, t) for t in uneq_types]
    eq_eq_pairs = [(eq_types[i], eq_types[j]) for i in range(len(eq_types)) for j in range(i+1, len(eq_types))]
    return source_eq_pairs + source_uneq_pairs + eq_eq_pairs

def call_model_api(prompt, model):
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        print(response.json())
    return response.json()

def main():
    # create a dictionary to store all data
    output_data_dict = {}
    try:
        # select dataset and prompt type
        config = read_json(os.path.join(os.path.dirname(__file__)+"/../../../../", "config/config.json"))
        print("config: ", config)

        # read configs
        datasets = config['datasets']
        functorInputPath = config['functorInputPath']
        dataset_sizes = config['dataset_sizes']
        sourceType = config['sourceType']

        # read input data
        for i in range(0,2):
            dataset = datasets[i]
            dataset_size = dataset_sizes[i]
            for j in range(0,dataset_size):## humaneval-160-prompt length exceeds limit     ?
                sourcePath = f'../../{functorInputPath}/{dataset}/{sourceType}/{j}_1.java'
                print("sourcePath:", sourcePath)
                if os.path.exists(sourcePath):
                    with open(sourcePath, 'r') as f:
                        PROMPT = f.read()
                        print("PROMPT:", PROMPT)
                    data = {
                        "apikey": API_KEY,
                        "apisecret": API_SECRET,
                        "prompt": PROMPT,
                        "src_lang": SRC_LANG,
                        "dst_lang": DST_LANG
                    }
                    res = requests.post(request_url, headers=headers, data=json.dumps(data))
                    res_json = res.json()
                    print(res_json)
                    generated = res_json['result']['output']['code'][0]
                    if res is not None:
                        with open(fr'../../model_response/translation-functor/codegeex/{dataset}/{SRC_LANG}-{DST_LANG}-{j}_0.txt', 'w') as f:
                            f.write(generated)
    except Exception as e:
        print(e)
    finally:
        # output the dictionary to a json file
        with open("tmp/dict.json", "w") as f:
            json.dump(output_data_dict, f)


if __name__ == "__main__":
    main()

