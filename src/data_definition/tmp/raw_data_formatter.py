'''
Raw Data Formatter

1. the original data may be in different format, we want to organize them into jsonl
e.g. humaneval.jsonl, code_contest.parquet

2. the original data may be in different languages, we want the code of same language organized in the same file
e.g. code_contest has 4 languages, we want to organize them into 4 files

'''
import os
from typing import List, Dict, Any
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.JsonlUtils import read_jsonl_file, write_jsonl_file


def mxeval_merge_jsonl_files(problem_file: str, completion_file: str, merged_file: str) -> List[Dict[str, Any]]:

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