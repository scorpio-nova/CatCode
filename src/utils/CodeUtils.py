import re

def extract_code_block(file_contents, targetLanguage):
    if targetLanguage.lower() == "python":
        return extract_code_block_python(file_contents)
    elif targetLanguage.lower() == "javascript":
        return extract_code_block_javascript(file_contents)
    elif targetLanguage.lower() == "java":
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
    return "\n".join(code_block)

def extract_function_body(file_contents, target_language):
    extractors = {
        "python": extract_function_body_python,
        "javascript": extract_function_body_javascript,
        "java": extract_function_body_java
    }
    extractor = extractors.get(target_language.lower())
    if extractor:
        return extractor(file_contents)
    return ''


def extract_function_body_java(code_block):
    # Find the function definition (could be public xxx except for public class xxx)
    pattern = r'(?:public|private|protected|static)?(?:\s+abstract)?\s+(?:\w+\s+)*\w+\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{([^}]+)\}'
    match = re.search(pattern, code_block, re.MULTILINE | re.DOTALL)
    if match:
        return code_block[match.regs[1][0]:]
    else:
        return ''

def extract_function_body_python(code_block):
    # Find the function definition
    start_match = re.search(r'def ', code_block, flags=re.MULTILINE)
    if not start_match:
        return ''
    start_line_break = re.search('\n', code_block[start_match.end():], flags=re.MULTILINE)
    start_idx = start_match.end() + start_line_break.end() + 1
    # Extract the function body
    function_body = code_block[start_idx:]
    return ' '+function_body

def extract_function_body_javascript(code_block):
    pattern = r'(?:function\s*(?:\w+\s*)?\([^)]*\)|const\s*\w+\s*=\s*function\s*\([^)]*\)|const\s*\w+\s*=\s*\([^)]*\)\s*=>)\s*{([^}]+)}'
    match = re.search(pattern, code_block)
    if match:
        return code_block[match.regs[1][0]:]
    else:
        return ''


def remove_python_comments(code: str):
    """去除 Python 代码中的注释"""
    in_string = False  # 标记是否在字符串中
    in_comment = False  # 标记是否在注释中
    new_code = []  # 去除注释后的代码
    for i in range(len(code)):
        # 检查是否在字符串中
        if i > 0 and code[i-1:i+1] != '\'\'' and code[i] == '\'' and code[i-1] != '\\':
            in_string = not in_string
        # 检查是否在注释中
        elif not in_string and code[i:i+1] == '#':
            in_comment = True
        # 如果不在注释中，则将该字符添加到去除注释后的代码中
        elif not in_comment:
            new_code.append(code[i])
        # 如果在注释中，则忽略该行剩余部分
        elif in_comment and code[i] == '\n':
            in_comment = False
            new_code.append(code[i])
    return ''.join(new_code)

def remove_java_comments(code: str):
    """去除 Java 代码中的注释"""
    in_string = False  # 标记是否在字符串中
    in_comment = False  # 标记是否在注释中
    new_code = []  # 去除注释后的代码
    i = 0
    while i < len(code):
        # 检查是否在字符串中
        if i > 0 and code[i-1:i+1] != '\'\'' and code[i] == '\'' and code[i-1] != '\\':
            in_string = not in_string
        # 检查是否在注释中
        elif not in_string and code[i:i+2] == '/*':
            in_comment = True
        # 如果不在注释中，则将该字符添加到去除注释后的代码中
        elif not in_comment:
            new_code.append(code[i])
        # 如果在注释中，则忽略该行剩余部分
        elif in_comment and code[i:i+2] == '*/':
            in_comment = False
            new_code.append(' ')
            i += 1
        i += 1
    return ''.join(new_code)

def extract_function_headers(json_data, language:str):
    """
    used to generate src/task_formulation/function_headers
    """
    headers = []
    if language.lower() == 'java':
        for line in json_data['prompt'].split('\n'):
            if line.startswith('public') or line.startswith('private') or line.startswith('protected'):
                function_header = line.strip()
                headers.append({'task_id': json_data['task_id'], 'function_header': function_header})

    elif language.lower() == 'python':
        for line in json_data['prompt'].split('\n'):
            if line.startswith('def'):
                function_header = line.strip()
                headers.append({'task_id': json_data['task_id'], 'function_header': function_header})
    elif language.lower() == 'javascript':
        for line in json_data['prompt'].split('\n'):
            javascript_regex = r"function\s+(\w+)\s*\((.*)\)\s*{"
            if re.match(javascript_regex, line):
                function_header = line.strip()
                headers.append({'task_id': json_data['task_id'], 'function_header': function_header})
    return headers