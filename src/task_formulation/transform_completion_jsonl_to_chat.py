import argparse
import jsonlines


def transform_completion_jsonl_to_chat(jsonl_file, output_jsonl_file):
    transformed_data = []
    with jsonlines.open(jsonl_file) as jsonl_file:
        for row in jsonl_file:
            input_text = row['prompt']
            # Append the input text as a new message in the transformed object
            row['messages'] = [{'role': 'user', 'content': input_text}]
            # use chatgpt model
            row['model'] = 'gpt-3.5-turbo-0301'
            # delete the prompt field
            del row['prompt']
            # Append the transformed object to the result list
            transformed_data.append(row)

    # write to a new jsonl file in the ChatGPT API format
    with jsonlines.open(output_jsonl_file, 'w') as outfile:
        for row in transformed_data:
            outfile.write(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_jsonl_file', help='Input JSONL file path')
    parser.add_argument('--output_jsonl_file', help='Output JSONL file path')
    args = parser.parse_args()

    transform_completion_jsonl_to_chat(args.input_jsonl_file, args.output_jsonl_file)
