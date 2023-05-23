import os
import json

### todo: refactor read_file and write_file fucntion (use jsonl to replace json may be better)
def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def merge_files(source,current_dir,transform_types):
    result = {}
    source_dir = f"{current_dir}/../../data/categorical_data/morphism_output/{source}/NoTransform"
    for idx in os.listdir(source_dir):
        idx = idx.split(".")[0].split("_")[0]
        file_data = {"NoTransform": read_file(f"{source_dir}/{idx}_1.java")}
        for transform_type in transform_types:
            file_data[transform_type] = {}
            transformed_file_path = f"{current_dir}/../../data/categorical_data/morphism_output/{source}/{transform_type}"
            if os.path.exists(transformed_file_path):
                for file_name in os.listdir(transformed_file_path):
                    if file_name.startswith(f"{idx}_") and file_name.endswith(".java"):
                        k = file_name.split("_")[1].split(".")[0]
                        transformed_file_name = f"{transformed_file_path}/{file_name}"
                        print(transformed_file_name)
                        file_data[transform_type][k] = read_file(transformed_file_name)
        result[f"{source}-{idx}"] = file_data
    return result

if __name__ == '__main__':
    source_files = ["humaneval_java", "mathqa_java", "mbxp_java"]
    current_path = os.path.dirname(os.path.realpath(__file__))
    transform_types = ["BooleanExchange", "LoopExchange", "ModifyCondition", "PermuteStatement", "RemoveElse", "ReorderCondition", "SwitchToIf", "UnusedStatement", "VariableRenaming"]
    output_folder = f"{current_path}/../../data/categorical_data/morphism_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for source in source_files:
        merged_data = {}
        merged_data.update(merge_files(source, current_path, transform_types))
        write_file(f"{output_folder}/{source}.json", json.dumps(merged_data, indent=4))