import json
import re
import sys
sys.setrecursionlimit(1000000)

def deal_json_invaild(text):
    if type(text) != str:
        raise Exception("参数接受的是字符串类型")
    # text = re.search(r"\{.*\}", text).group()
    text = re.sub(r"\n|\t|\r|\r\n|\n\r|\x08|\\", "", text)
    try:
        json.loads(text)
    except json.decoder.JSONDecodeError as err:
        temp_pos = int(re.search(r"\(char (\d+)\)", str(err)).group(1))
        temp_list = list(text)
        while True:
            if temp_list[temp_pos] == "\"" or "}":
                if temp_list[temp_pos - 1] == "{":
                    break
                elif temp_list[temp_pos - 1] == (":" or "{") and temp_list[temp_pos - 2] == ("\"" or ":" or "["):
                    break
                elif temp_list[temp_pos] == "|\n|\t|\r|\r\n|\n\r| ":
                    temp_list[temp_pos] = re.sub(temp_list[temp_pos], "", temp_list[temp_pos])
                    text = "".join(temp_list)
                elif temp_list[temp_pos] == "\"":
                    temp_list[temp_pos] = re.sub(temp_list[temp_pos], "“", temp_list[temp_pos])
                    text = "".join(temp_list)
                elif temp_list[temp_pos] == "}":
                    temp_list[temp_pos - 1] = re.sub(temp_list[temp_pos], "\"", temp_list[temp_pos])
                    text = "".join(temp_list)
                    temp_pos -= 1
            temp_pos -= 1
        return deal_json_invaild(text)
    else:
        return text


for i in range(0, 164):
    with open(f'/Users/serena/Desktop/THU/02-博一下/test/Java-Python-{i}_0.txt', 'r') as f:
        # read the string and convert it to json
        string = str(f.read())
        new_str = deal_json_invaild(string)
        data = json.loads(new_str)
        generated = data['result']['output']['code_dict'][0]['generated']
        print(generated)

    with open(f'/Users/serena/Desktop/THU/01-博一上/AI-Code/cat-code-eval/model_response/functor-translate/codegeex/humaneval/Java-Python-{i}_0.txt', 'w') as f:
        json.dump(generated, f)
