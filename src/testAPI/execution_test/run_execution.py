import jsonlines

def calculate_PRF1(TP, FP, TN, FN):
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    F1 = 2 * precision * recall / (precision + recall)
    return precision, recall, F1

def calculate_metrics(jsonl_data):
    TP = FP = TN = FN = 0

    for row in jsonl_data:
        prediction = None
        true_value = None

        choice = row['choices']
        if choice and isinstance(choice, str):
            prediction = choice.strip()

        source = row['source']
        if source and isinstance(source, str):
            parts = source.split('-')
            if len(parts) > 2:
                true_value = parts[2].split('_')[0]

        if prediction and true_value:
            if prediction.lower() == "true" and true_value.lower() == "true":
                TP += 1
            elif prediction.lower() == "true" and true_value.lower() == "false":
                FP += 1
            elif prediction.lower() == "false" and true_value.lower() == "true":
                FN += 1
            elif prediction.lower() == "false" and true_value.lower() == "false":
                TN += 1

    return TP, FP, TN, FN

# Read the merged JSONL file
with jsonlines.open('../../model_response_collector/codecontest_eval_file.jsonl') as jsonl_file:
    jsonl_data = list(jsonl_file)

# Calculate metrics
TP, FP, TN, FN = calculate_metrics(jsonl_data)

print("True Positive (TP):", TP)
print("False Positive (FP):", FP)
print("True Negative (TN):", TN)
print("False Negative (FN):", FN)
print("PRF1", calculate_PRF1(TP, FP, TN, FN))
