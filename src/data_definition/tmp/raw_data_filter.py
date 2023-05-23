'''
keys
e.g. humaneval.jsonl: data_source, task_id, prompt, canonical_solution, language
e.g. code_contest: id, language, code, code_tokens, code_tokens_str, code_nl, code_nl_tokens, code_nl_tokens_str, code_nl_ast, code_nl_ast_tokens, code_n

the target format is jsonl with keys data_source, task_id, prompt, completion, language
For Example:
{
"data_source":"HumanEval"
"task_id": "test/0",
"language": "Python",
"prompt": "def return1(): *** this is a function...***\n",
"completion": "    return 1", // this may be wrong
"canonical_solutions": ["    return 1"]
"incorrect_solutions" (can be empty): ["    return 2","    return 3"]
"test" (str/None): "def check(candidate):\n    assert candidate() == 1"
}
'''
