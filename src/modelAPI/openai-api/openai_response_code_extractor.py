import sys
import os
import jsonlines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.CodeUtils import extract_code_block,extract_function_body
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract code from response')
    parser.add_argument('--input_file', type=str, help='input file path')
    parser.add_argument('--output_file', type=str, help='output file path')
    parser.add_argument('--language', type=str, help='programming language')
    parser.add_argument('--dataset', type=str, help='dataset')
    args = parser.parse_args()

    if not args.input_file:
        raise ValueError("Invalid input: input_file argument not provided")
    if not args.output_file:
        raise ValueError("Invalid input: output_file argument not provided")
    if not args.language:
        raise ValueError("Invalid input: language argument not provided")
    if not args.dataset:
        raise ValueError("Invalid input: dataset argument not provided")

    input_file = args.input_file
    output_file = args.output_file
    language = args.language
    dataset = args.dataset


    with jsonlines.open(input_file, 'r') as reader:
        json_list = list(reader)
        with jsonlines.open(output_file, mode='w') as writer:
            code_dict_list = []
            for json_dict in json_list:
                if isinstance(json_dict, dict):
                    task_id = json_dict['task_id']
                    text = json_dict['completion']
                elif isinstance(json_dict,list):
                    task_id = json_dict[0]['task_id']
                    first_response = json_dict[1]['choices'][0]
                    if 'text' in first_response:
                        text = first_response['text']
                    else:
                        text = first_response['message']['content']
                code_block = extract_code_block(text, language)
                function_body = extract_function_body(text, language)
                code_dict = dict(task_id=f"{dataset}/{task_id}", language=language,
                                 completion=function_body)
                code_dict_list.append(code_dict)
                # reorder by task_id
            code_dict_list = sorted(code_dict_list, key=lambda x: x['task_id'])
            writer.write_all(code_dict_list)


