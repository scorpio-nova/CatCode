import json
import os.path
import sys
from tqdm import tqdm
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""
This script extracts code from a JSONL file and generates separate program files for each code snippet.
Functions:
    create_program_file_from_jsonl(input_file, output_folder): Reads a JSONL file and creates program files for each code snippet.
"""

### used by humaneval, mathqa and mbxp
def create_program_file_from_jsonl(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # read jsonl line by line and extract "prompt" and "canonical_solution" fields
    with open(input_file, "r") as f:
          for line in tqdm(f):
                data = json.loads(line)
                task_id = data["task_id"]
                id = task_id.split("/")[1]
                prompt = data["prompt"].lstrip('\n')
                if data["canonical_solution"]:
                    completion = data["canonical_solution"]
                else: completion = data["completion"]
                # create a python file with the prompt as the file name and the canonical solution as the content
                with open(os.path.join(output_folder,  str(id) + ".java"), "w") as f:
                        f.write(prompt)
                        f.write(completion)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    create_program_file_from_jsonl(f'{current_path}/../../data/categorical_data/formatted_data/humanevalx_extracted_java.jsonl',f'{current_path}/../../data/categorical_data/morphism_input/humaneval_java')
    create_program_file_from_jsonl(f'{current_path}/../../data/categorical_data/formatted_data/mathqa_extracted_java.jsonl',f'{current_path}/../../data/categorical_data/morphism_input/mathqa_java')
    create_program_file_from_jsonl(f'{current_path}/../../data/categorical_data/formatted_data/mbxp_extracted_java.jsonl',f'{current_path}/../../data/categorical_data/morphism_input/mbxp_java')

