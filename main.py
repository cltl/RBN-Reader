"""
Load RBN as python classes

Usage:
  main.py --input_path=<input_path> --output_path=<output_path> --allowed_prefixes=<allowed_prefixes> --exclude_sub_NUMBER=<include_sub_NUMBER> --namespace=<namespace> --short_namespace=<short_namespace>

Options:
    --input_path=<input_path> 'resources/orbn_1.0.xml'
    --output_path=<output_path> 'output/orbn.p'
    --allowed_prefixes=<allowed_prefixes> prefixes separated by +. options are r | c | o | t
    --exclude_sub_NUMBER=<include_sub_NUMBER> if True, identifiers that end with sub_NUMBER are not included
    --namespace=<namespace> the RDF namespace, e.g., http://premon.fbk.eu/resource/
    --short_namespace=<short_namespace> e.g., pm

Example:
    python main.py --input_path="resources/orbn_1.0.xml" --output_path="output/orbn.p" --allowed_prefixes="r+c" --exclude_sub_NUMBER="True" --namespace="http://premon.fbk.eu/resource/" --short_namespace="pm"
"""
import pickle
from docopt import docopt
from lxml import etree
from odwn_classes import LE


# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS:')
print(arguments)

# load resource
input_path = arguments['--input_path']
doc = etree.parse(input_path)
print(f'loaded: {input_path}')
allowed_prefixes = set(arguments['--allowed_prefixes'].split('+'))
exclude_sub_number_ids = arguments['--exclude_sub_NUMBER'] == 'True'

not_added = set()
# load resource into classes
verbose = 1
le_objs = []

for le_xml_obj in doc.xpath('cdb_lu'):

    le_obj = LE(le_xml_obj,
                arguments['--namespace'],
                arguments['--short_namespace'],
                verbose=verbose)

    if le_obj.prefix not in allowed_prefixes:
        le_obj.add = False

    if all(['_sub_' in le_obj.sense_id,
            exclude_sub_number_ids]):
        le_obj.add = False

    if le_obj.add:
        le_objs.append(le_obj)
    else:
        not_added.add(le_obj.sense_id)

output_path = arguments['--output_path']
with open(output_path, 'wb') as outfile:
    pickle.dump(le_objs, outfile)
print(f'writting output to: {output_path}')
print(f'# of ids not added due to settings or information not available: {len(not_added)}')








