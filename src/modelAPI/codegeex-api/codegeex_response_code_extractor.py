import re
import jsonlines
import json



def extract_code_block(file_contents, targetLanguage):
    if targetLanguage == "Python":
        return extract_code_block_python(file_contents)
    elif targetLanguage == "JavaScript":
        return extract_code_block_javascript(file_contents)
    elif targetLanguage == "java":
        return extract_code_block_java(file_contents)

def extract_code_block_java(file_contents):
    # Find the first two occurrence of ``` and extract the lines between them
    lines = file_contents.splitlines()
    start_index = -1
    end_index = -1
    for i in range(len(lines)):
        if lines[i] == '```' or lines[i] == '```java':
            if start_index == -1:
                start_index = i
            else:
                end_index = i
                break
    if start_index == -1:
        return file_contents
    code_block = lines[start_index + 1:end_index]
    print("code_block:", code_block)
    return "\n".join(code_block)

def extract_code_block_python(file_contents):
    # Find the first two occurrence of ``` and extract the lines between them
    lines = file_contents.splitlines()
    start_index = -1
    end_index = -1
    for i in range(len(lines)):
        if lines[i] == '```' or lines[i] == '```python':
            if start_index == -1:
                start_index = i
            else:
                end_index = i
                break
    if start_index == -1:
        return file_contents
    code_block = lines[start_index + 1:end_index]
    # print("code_block:", code_block)
    return "\n".join(code_block).replace("\t", "    ")

def extract_code_block_javascript(file_contents):
    # Find the first two occurrence of ``` and extract the lines between them
    lines = file_contents.splitlines()
    start_index = -1
    end_index = -1
    for i in range(len(lines)):
        if lines[i] == '```' or lines[i] == '```javascript':
            if start_index == -1:
                start_index = i
            else:
                end_index = i
                break
    if start_index == -1:
        return file_contents
    code_block = lines[start_index + 1:end_index]
    # print("code_block:", code_block)
    return "\n".join(code_block)

def extract_function_body(file_contents, targetLanguage):
    if targetLanguage.lower() == "python":
        return extract_function_body_python(file_contents, targetLanguage)
    elif targetLanguage.lower() == "javascript":
        return extract_function_body_javascript(file_contents, targetLanguage)
    elif targetLanguage.lower() == "java":
        return extract_function_body_java(file_contents, targetLanguage)

def extract_function_body_java(code_block, targetLanguage):
    print(code_block)
    # Extract the code block
    # code_block = extract_code_block(code_block, targetLanguage)
    # Find the function definition (could be public xxx except for public class xxx)
    pattern = r'(?:public|private|protected|static)?(?:\s+abstract)?\s+(?:\w+\s+)*\w+\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{([^}]+)\}'
    match = re.search(pattern, code_block, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None

def extract_function_body_python(code_block, targetLanguage):
    # Extract the code block
    code_block = extract_code_block(code_block, targetLanguage)
    # Find the function definition
    start_match = re.search(r'def ', code_block, flags=re.MULTILINE)
    if not start_match:
        return ''
    start_line_break = re.search('\n', code_block[start_match.end():], flags=re.MULTILINE)
    start_idx = start_match.end() + start_line_break.end() + 1
    # Extract the function body
    function_body = code_block[start_idx:]
    return ' '+function_body

def extract_function_body_javascript(code_block, targetLanguage):
    # Extract the code block
    print("code_block:", code_block)
    code_block = extract_code_block(code_block, targetLanguage)
    pattern = r'(?:function\s*(?:\w+\s*)?\([^)]*\)|const\s*\w+\s*=\s*function\s*\([^)]*\)|const\s*\w+\s*=\s*\([^)]*\)\s*=>)\s*{([^}]+)}'
    match = re.search(pattern, code_block)
    if match:
        return code_block[match.regs[1][0]:]
    else:
        return None


if __name__ == '__main__':
    sourceLanguage = 'Java'
    targetLanguage = 'Python'
    fileRoot = f'model_response/reproduction-functor/humaneval_java_results.jsonl'
    datasets = ['humaneval', 'mathqa', 'mbxp']
    task_prefix = {'humaneval':'HumanEval','mathqa':'MathQA','mbxp':'MBJP'}
    dataset_sizes = [164, 1884, 974]
    for dataset, size in zip(datasets, dataset_sizes):
        with jsonlines.open(fr'{fileRoot}/{dataset}_{sourceLanguage}-{targetLanguage}.jsonl', mode='w') as writer:
            json_list = []
            for i in range(size):
                file = f'{fileRoot}/{dataset}/{sourceLanguage}-{targetLanguage}-{i}_0.txt'
                print("processing file:", file)
                try:
                    with open(file, 'r') as f:
                        file_contents = f.read()
                        print("file_contents:\n", file_contents)
                        function_body = extract_function_body(file_contents, targetLanguage)
                        print("function_body:\n", function_body)
                        code_dict = dict(task_id=f"{task_prefix[dataset]}/{i}", language=fr"{targetLanguage}",
                             completion=function_body)
                        writer.write(code_dict)
                        json_list.append(code_dict)
                except FileNotFoundError:
                    print("File not found, skipping...")
