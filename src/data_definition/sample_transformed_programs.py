import json
import random
import os

def sample_value(subdict):
    subkeys = [k for k in subdict.keys() if k != "NoTransform"]
    subkey = random.choice(subkeys)
    sampled_value = subdict[subkey]
    return sampled_value


def process_data(data,eq_transform_types,uneq_transform_types,threshold):
    new_data = {}
    for mainKey, subdict in data.items():
        data_piece = {}
        eq_keys = [k for k in subdict.keys() if k in eq_transform_types and len(subdict[k]) != 0]
        # print("eq_keys", eq_keys)
        selected_eq_keys = random.sample(eq_keys, min(len(eq_keys), threshold))
        uneq_keys = [k for k in subdict.keys() if k in uneq_transform_types and len(subdict[k]) != 0]
        # print("uneq_keys", uneq_keys)
        selected_uneq_keys = random.sample(uneq_keys, min(len(uneq_keys), threshold))
        for key, value in subdict.items():
            if key == "NoTransform":
                data_piece[key] = value
            elif key in selected_eq_keys or key in selected_uneq_keys:
                data_piece[key] = sample_value(value)
        new_data[mainKey] = data_piece
    return new_data


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # todo: refactor, following 3 lines read from config; input and output dir rename and read from config
    source_files = ["humaneval_java", "mathqa_java", "mbxp_java"]
    eq_transform_types = ["BooleanExchange", "LoopExchange", "PermuteStatement", "ReorderCondition", "SwitchToIf", "UnusedStatement", "VariableRenaming"]
    uneq_transform_types = ["ModifyCondition", "RemoveElse"]
    output_folder = f"{current_dir}/../../data/categorical_data/sampled_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for source in source_files:
        with open(f"{current_dir}/../../data/categorical_data/morphism_output/{source}.json", "r") as f:
            data = json.load(f)
            new_data = process_data(data,eq_transform_types,uneq_transform_types,threshold=2)
        with open(f"{output_folder}/{source}.json", "w") as f:
            json.dump(new_data, f, indent=4)
