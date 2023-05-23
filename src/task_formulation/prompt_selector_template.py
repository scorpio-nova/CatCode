import argparse
import jsonlines

def select_prompt(task, *variables):
    prompts = {
        "task1": "Prompt for task 1 with variable 1: {0}",
        "task2": "Prompt for task 2 with variable 1: {0}, variable 2: {1}",
        "task3": "Prompt for task 3 with variable 1: {0}, variable 2: {1}, variable 3: {2}",
        # Add more tasks and prompts as needed
    }

    # Check if the task exists in the prompts dictionary
    if task in prompts:
        prompt = prompts[task]
        # Replace variable placeholders with actual values
        prompt = prompt.format(*variables)
        print("prompt:",prompt)
        return prompt
    else:
        # Raise an error if the task is not found
        raise ValueError(f"No prompt defined for task '{task}'. Please define a prompt for this task or choose a different task.")

#
# # Parse command-line arguments
# parser = argparse.ArgumentParser(description="Prompt Selector")
# parser.add_argument("--task", required=True, help="Task name")
# parser.add_argument("--variable_file", required=True, help="Path to JSONL file containing variables")
# parser.add_argument("--keys", required=True, nargs="*", help="Keys of the variables in the file")
#
# args = parser.parse_args()
#
# # Get the task from the command-line arguments
# task = args.task
# keys = args.keys
#
# # Read the JSONL file and extract the variables
# variables = []
# with jsonlines.open(args.variables_file) as reader:
#     for item in reader:
#         for key in keys:
#             variable = item.get(key)
#             prompt = select_prompt(task, *variable)
#             # Generate the prompt
#             print(prompt)



def test_select_prompt():
    # Test case 1: Task with one variable
    task = "task1"
    variables = ["Variable 1"]
    expected_prompt = "Prompt for task 1 with variable 1: Variable 1"
    assert select_prompt(task, *variables) == expected_prompt

    # Test case 2: Task with two variables
    task = "task2"
    variables = ["Variable 1", "Variable 2"]
    expected_prompt = "Prompt for task 2 with variable 1: Variable 1, variable 2: Variable 2"
    assert select_prompt(task, *variables) == expected_prompt

    # Test case 3: Task with three variables
    task = "task3"
    variables = ["Variable 1", "Variable 2", "Variable 3"]
    expected_prompt = "Prompt for task 3 with variable 1: Variable 1, variable 2: Variable 2, variable 3: Variable 3"
    assert select_prompt(task, *variables) == expected_prompt


    print("All test cases passed!")

# Run the test cases
test_select_prompt()

