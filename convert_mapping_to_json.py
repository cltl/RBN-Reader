"""
Filtering and printing a text file based on sentence length.

Usage:
  convert_mapping_to_json.py --path_to_excel=<path_to_excel> --json_output_path=<json_output_path>

Example:
    python convert_mapping_to_json.py --path_to_excel="mapping_to_fn/Mapping.xlsx" --json_output_path="mapping_to_fn/mapping.json"
"""
import pandas
import os
import json
from docopt import docopt

arguments = arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS')
print(arguments)

excel_path = arguments['--path_to_excel']
assert os.path.exists(excel_path), f'{excel_path} does not exist'


df = pandas.read_excel(excel_path, sheet_name='the_mapping')

feature_set2top_frames = dict()

for index, row in df.iterrows():
    feature_set = row['RBN feature set']
    frames = row['English FrameNet frames']
    frames = frames.split(',')
    feature_set2top_frames[feature_set] = frames


with open(arguments['--json_output_path'], 'w') as outfile:
    json.dump(feature_set2top_frames, outfile)
