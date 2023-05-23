import os
import jsonlines
import json

from typing import List, Dict

def read_json(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

class SolutionPair:
    def __init__(self, language: str, solutionA: str, solutionB: str, equivalence: bool):
        self.language = language
        self.solutionA = solutionA
        self.solutionB = solutionB
        self.equivalence = equivalence

class SolutionRecord:
    def __init__(self, id: int, solutions: Dict[str, List[str]], incorrect_solutions: Dict[str, List[str]]):
        self.id = id
        self.solutions = solutions
        self.incorrect_solutions = incorrect_solutions

def readJsonlFile(filename: str) -> List[List[SolutionPair]]:
    solutions = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)

            languages = list(record['solutions'].keys())

            for language in languages:
                languageSolutions = []
                correctSolutions = record['solutions'][language]
                incorrectSolutions = record['incorrect_solutions'][language]

                if not correctSolutions or not incorrectSolutions:
                    continue

                # correct-correct pairs
                for i in range(len(correctSolutions)):
                    for j in range(i + 1, len(correctSolutions)):
                        solutionPair = SolutionPair(language, correctSolutions[i], correctSolutions[j], True)
                        languageSolutions.append(solutionPair)

                # correct-incorrect pairs
                for correctSolution in correctSolutions:
                    for incorrectSolution in incorrectSolutions:
                        solutionPair = SolutionPair(language, correctSolution, incorrectSolution, False)
                        languageSolutions.append(solutionPair)

                solutions.append(languageSolutions)
    return solutions



if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    config = read_json(f"{current_path}/../../config/config.json")
    print("config: ", config)
    # read configs
    dataset = config['global_dataset']
    dataset_size = 164

    try:
        # read input data
        solutions = readJsonlFile(f"{current_path}/../../data/categorical_data/sampled_data/{dataset}.jsonl")
        outputs = []

        # config api and prompts
        promptText = "Do code A and code B have the same output for each valid input?\n" + \
        "Answer \"True\" or \"False\"."
        # loop for each data
        for i in range(len(solutions)):
            s = solutions[i]
            for pair_id in range(len(s)):
                language = s[pair_id].language
                referenceCode = s[pair_id].solutionA
                comparedCode = s[pair_id].solutionB
                equivalence = s[pair_id].equivalence
                prompt = f'code A:\n{referenceCode}\n code B:\n{comparedCode}\n{promptText}'
                data = {
                    "model": "text-davinci-003",
                    "prompt": prompt,
                    "source": f"code_contest/{language}-{i}-{equivalence}_{pair_id}"
                }
                outputs.append(data)
        with jsonlines.open(f"{current_path}/../../data/task_input/morphism-identify/davinci/code_contest.jsonl", mode='w') as writer:
            for output in outputs:
                writer.write(output)

    except Exception as e:
        print(e)

