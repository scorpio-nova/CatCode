import argparse
import jsonlines

def select_prompt(task, *variables):
    prompts = {
        "EmptyPrompt": "",
        "IdentifyLocalMorphism": "If two pieces of code always have the same output for the same input, we say they have the " \
                                 "same function. Read code A and code B below, if they have the same function? Answer \"Ture.\" " \
                                 "or \"False.\"\ncode A:\n {0}\ncode B:\n{1}",
        "IdentifyGlobalMorphism": "code A:\n {0}\ncode B:\n{1}Do code A and code B have the same output for each valid input?\n" + \
                                  "Answer \"True\" or \"False\".",
        "CodeTranslation": "Translate the below {0} code to {1} code. The function header is {2}. You should only answer the {2} function body without further comments and explanations.\n{3}",
        "CodeExplanation": "Please describe the following code written in {0} using natural language. " \
                     "Your description should include the exact function name, its arguments, and the return type. " \
                     "Additionally, provide enough details such as variable initialization to allow someone to reproduce the code based on your explanation."\
                     "\n'''\n{0}\n'''",
        "CodeReproduction": "Translate the below code description to {0} code. {1}",
        # Add more tasks and prompts as needed
    }

    # Check if the task exists in the prompts dictionary
    if task in prompts:
        prompt = prompts[task]
        # Replace variable placeholders with actual values
        prompt = prompt.format(*variables)
        return prompt
    else:
        # Raise an error if the task is not found
        raise ValueError(f"No prompt defined for task '{task}'. Please define a prompt for this task or choose a different task.")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Prompt Selector")
parser.add_argument("--task", required=True, help="Task name")
parser.add_argument("--variable_file", required=True, help="Path to JSONL file containing variables")
parser.add_argument("--keys", required=True, nargs="*", help="Keys of the variables in the file")

args = parser.parse_args()

# Get the task from the command-line arguments
task = args.task
keys = args.keys

# Read the JSONL file and extract the variables
variables = []
with jsonlines.open(args.variables_file) as reader:
    for item in reader:
        for key in keys:
            variable = item.get(key)
            prompt = select_prompt(task, *variable)
            # Generate the prompt
            print(prompt)
