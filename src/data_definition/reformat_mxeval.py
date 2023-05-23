import argparse
from typing import List, Dict, Any
import os
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.JsonlUtils import read_jsonl_file, write_jsonl_file

'''
Data format needed for applying morphism is jsonl with keys data_source, task_id, prompt, completion, language
For Example:
{
"data_source":"HumanEval"
"task_id": "test/0",
"prompt": "def return1(): *** this is a function...***\n",
"completion": "    return 1",
"language": "Python"
}
'''


def merge_jsonl_files(problem_file: str, completion_file: str, merged_file: str) -> List[Dict[str, Any]]:

    # Read records from file A and file B
    records_a = read_jsonl_file(problem_file)
    records_b = read_jsonl_file(completion_file)

    # Create a dictionary of records from file B
    records_b_dict = {record['task_id']: record['completion'] for record in records_b}

    # Merge the records from file A and file B
    merged_records = [merge_records(record_a, records_b_dict) for record_a in records_a if
                      record_a['task_id'] in records_b_dict]

    # Write the merged records to file C
    write_jsonl_file(merged_records, merged_file)

    return merged_records

def merge_records(record_a: Dict[str, Any], records_b_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {**record_a, 'completion': records_b_dict[record_a['task_id']]}

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))

    code_source_path = os.path.join(current_path, '..', '..', 'data', 'raw_data')
    merged_dataset_path = os.path.join(current_path, '..', '..', 'data', 'categorical_data','formatted_data')

    file_paths = {
        'mbxp_prob_path': {
            'java': os.path.join(code_source_path, 'mbxp', 'mbjp_release_v1.jsonl'),
            'python': os.path.join(code_source_path, 'mbxp', 'mbpp_release_v1.jsonl'),
            'javascript': os.path.join(code_source_path, 'mbxp', 'mbjsp_release_v1.jsonl')
        },
        'mbxp_solu_path': {
            'java': os.path.join(code_source_path, 'mbxp', 'examples', 'mbjp_samples.jsonl'),
            'python': os.path.join(code_source_path, 'mbxp', 'examples', 'mbpp_samples.jsonl'),
            'javascript': os.path.join(code_source_path, 'mbxp', 'examples', 'mbjsp_samples.jsonl')
        },
        'mbxp_merged_file': {
            'java': os.path.join(merged_dataset_path, 'mbxp_extracted_java.jsonl'),
            'python': os.path.join(merged_dataset_path, 'mbxp_extracted_python.jsonl'),
            'javascript': os.path.join(merged_dataset_path, 'mbxp_extracted_javascript.jsonl')
        },
        'mathqa_prob_path': {
            'java': os.path.join(code_source_path, 'multilingual_mathqa', 'mathqa-test-java_v1.jsonl'),
            'python': os.path.join(code_source_path, 'multilingual_mathqa', 'mathqa-test-python_v1.jsonl'),
            'javascript': os.path.join(code_source_path, 'multilingual_mathqa', 'mathqa-test-javascript_v1.jsonl')
        },
        'mathqa_solu_path': {
            'java': os.path.join(code_source_path, 'multilingual_mathqa', 'examples', 'java_samples.jsonl'),
            'python': os.path.join(code_source_path, 'multilingual_mathqa', 'examples', 'python_samples.jsonl'),
            'javascript': os.path.join(code_source_path, 'multilingual_mathqa', 'examples', 'javascript_samples.jsonl')
        },
        'mathqa_merged_file': {
            'java': os.path.join(merged_dataset_path, 'mathqa_extracted_java.jsonl'),
            'python': os.path.join(merged_dataset_path, 'mathqa_extracted_python.jsonl'),
            'javascript': os.path.join(merged_dataset_path, 'mathqa_extracted_javascript.jsonl')
        },
        'humaneval_path': {
            'java': os.path.join(code_source_path, 'humaneval', 'humaneval_java.jsonl'),
            'python': os.path.join(code_source_path, 'humaneval', 'humaneval_python.jsonl'),
            'javascript': os.path.join(code_source_path, 'humaneval', 'HumanEval_javascript_v1.1.jsonl')
        }
    }
    # read the language from command line as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str, default='java', help='language to process')
    args = parser.parse_args()
    language = args.language

    mbxp_prob_path = file_paths['mbxp_prob_path'][language]
    mbxp_solu_path = file_paths['mbxp_solu_path'][language]
    mbxp_merged_file = file_paths['mbxp_merged_file'][language]

    mathqa_prob_path = file_paths['mathqa_prob_path'][language]
    mathqa_solu_path = file_paths['mathqa_solu_path'][language]
    mathqa_merged_file = file_paths['mathqa_merged_file'][language]


    merged_records_mbxp = merge_jsonl_files(mbxp_prob_path, mbxp_solu_path, mbxp_merged_file)
    print(
        f"Merged {len(merged_records_mbxp)} records from {mbxp_prob_path} and {mbxp_solu_path} into {mbxp_merged_file}")
    merged_records_mathqa = merge_jsonl_files(mathqa_prob_path, mathqa_solu_path, mathqa_merged_file)
    print(
        f"Merged {len(merged_records_mathqa)} records from {mathqa_prob_path} and {mathqa_solu_path} into {mathqa_merged_file}")


if __name__ == '__main__':
    main()
