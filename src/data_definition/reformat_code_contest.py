import pandas as pd
import json
import numpy as np
import sys
import os
from tqdm import tqdm

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.CodeUtils import remove_python_comments, remove_java_comments


def convert_ndarray_to_list(d):
    for key, value in d.items():
        if isinstance(value, dict):
            convert_ndarray_to_list(value)  # 递归调用自身
        elif isinstance(value, np.ndarray):
            d[key] = value.tolist()  # 将 NumPy 数组转换为 Python 列表
    return d

def extract_python_java_code(solutions, max_code_num=2,max_code_length=500):
    '''
    extract python3 and java code, corresponding to language == '3' and language == '4'
    '''
    language = solutions['language']
    code = solutions['solution']
    extracted_code = {'python': [],'java': []}
    for l,co in zip(language, code):
        if l == 3:
            c = remove_python_comments(co)
            if len(c) > max_code_length or len(extracted_code['python']) >= max_code_num:
                continue
            extracted_code['python'].append(c)
        elif l == 4:
            c = remove_java_comments(co)
            if len(c) > max_code_length or len(extracted_code['java']) >= max_code_num:
                continue
            extracted_code['java'].append(c)
    return extracted_code

if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))

    code_source_path = os.path.join(current_path, '..', '..', 'data', 'raw_data')
    merged_dataset_path = os.path.join(current_path, '..', '..', 'data', 'categorical_data','formatted_data')

    df = pd.read_parquet(f'{code_source_path}/code_contest/test-00000-of-00001-9c49eeff30aacaa8.parquet')

    with open(f'{merged_dataset_path}/code_contest_extracted.jsonl', 'w') as f:
        id = 0
        for row in tqdm(df.to_dict('records')):
            json_row = convert_ndarray_to_list(row)
            name = json_row['name']
            solutions = json_row['solutions']
            incorrect_solutions = json_row['incorrect_solutions']
            extracted_solutions = extract_python_java_code(solutions)
            extracted_incorrect_solutions = extract_python_java_code(incorrect_solutions)

            extracted_data = {
                'id': id,
                'task_id': name,
                'canonical_solutions': extracted_solutions,
                'incorrect_solutions': extracted_incorrect_solutions,
            }
            jsonRow = convert_ndarray_to_list(extracted_data)
            f.write(json.dumps(jsonRow) + '\n')
            id += 1
