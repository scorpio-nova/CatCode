import jsonlines
from typing import List, Dict, Any, Union
import json
import os


def read_jsonl_file(file_path: str) -> List[Dict[str, Any]]:
    with jsonlines.open(file_path) as reader:
        print(f"Reading {file_path}...")
        records = [record for record in reader]
    return records


def write_jsonl_file(records: List[Dict[str, Any]], file_path: str) -> None:
    with jsonlines.open(file_path, mode='w') as writer:
        writer.write_all(records)


def create_program_file_from_jsonl(input_file, output_file):
    # read jsonl line by line and extract "prompt" and "canonical_solution" fields
    with open(input_file, "r") as f:
        for idx, line in enumerate(f, start=0):
            data = json.loads(line)
            prompt = data["prompt"]
            canonical_solution = data["canonical_solution"]
            print(prompt)
            print(canonical_solution)
            # create a python file with the prompt as the file name and the canonical solution as the content
            with open(os.path.join(output_file, "solution-" + str(idx) + ".java"), "a") as f:
                f.write(prompt)
                f.write(canonical_solution)
                f.write("\n")


def get_function_header(headers, task_id: str) -> Union[str, None]:
    for header in headers:
        if header['task_id'] == task_id:
            return header['function_header']
    return None


def merge_jsonl_files(file1, file2, output_file, key_map):
    # 读取第一个 JSONL 文件
    with jsonlines.open(file1) as reader1:
        data1 = list(reader1)

    # 读取第二个 JSONL 文件
    with jsonlines.open(file2) as reader2:
        data2 = list(reader2)

    # 合并数据并根据 key map 修改 key 值
    merged_data = []
    for item1 in data1:
        merged_item = {key_map.get(key, key): value for key, value in item1.items()}
        merged_data.append(merged_item)
    for item2 in data2:
        merged_item = {key_map.get(key, key): value for key, value in item2.items()}
        merged_data.append(merged_item)

    # 输出到第三个 JSON 文件
    with jsonlines.open(output_file, 'w') as writer:
        writer.write_all(merged_data)

