import jsonlines
import json


def convert_to_json(input_file, output_file):
    with jsonlines.open(input_file) as reader:
        with open(output_file, 'w') as f:
            json.dump(list(reader), f)
