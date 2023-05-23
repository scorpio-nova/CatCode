import jsonlines
from typing import Union, Dict, List
import argparse
import os

def process_obj(obj: Union[Dict, List], model: str, sourceLanguage: str, model_name: str) -> Dict:
    if isinstance(obj, list):
        task_id = obj[0]['task_id']
        first_response = obj[1]['choices'][0]
        if 'text' in first_response:
            text = first_response['text']
        else:
            text = first_response['message']['content']
    elif isinstance(obj, dict):
        task_id = obj['request']['task_id']
        text = obj['response']['choices'][0]['text']
    prompt = f"Translate the below code description to {sourceLanguage} code: \n{text}\n"
    if model == 'text-davinci-003':
        data = {'task_id': task_id, 'prompt': prompt, 'model': model, 'max_tokens': 500}
    elif model == 'gpt-3.5-turbo-0301': # chatgpt
        data = {'task_id': task_id, 'messages': [{'role': 'user', 'content': prompt}], 'model': model, 'max_tokens': 500}
    else: raise ValueError("unknown model:",model)
    return data

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='Name of the model, supported: davinci, chatgpt')
    args = parser.parse_args()
    if not args.model_name:
        parser.error('The --model_name argument is required.')
    model_name = args.model_name
    datasets = ['mathqa', 'mbxp', 'humaneval']
    sourceLanguage = "Java"
    models = {'davinci':'text-davinci-003', 'chatgpt':'gpt-3.5-turbo-0301'}
    exact_model_name = models[model_name]

    current_path = os.path.dirname(os.path.abspath(__file__))
    for dataset in datasets:
        file_path = f"{current_path}/../../data/task_output/explanation-functor/{model_name}/{dataset}_java_nl_results.jsonl"
        output_path = f"{current_path}/../../data/task_input/reproduction-functor/{model_name}/{dataset}_nl_java.jsonl"
        with jsonlines.open(file_path) as reader:
            with jsonlines.open(output_path, 'w') as writer:
                for obj in reader:
                    data = process_obj(obj, exact_model_name, sourceLanguage, model_name)
                    writer.write(data)

if __name__ == '__main__':
    main()
