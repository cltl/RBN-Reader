"""
Load RBN as python classes

Usage:
  main.py --orbn_path=<input_path> --odwn_path=<odwn_path> --output_folder=<output_folder> --allowed_prefixes=<allowed_prefixes> --exclude_sub_NUMBER=<include_sub_NUMBER> --namespace=<namespace> --short_namespace=<short_namespace>

Options:
    --orbn_path=<input_path> 'resources/orbn_n-v-a.xml'
    --odwn_path=<odwn_path> 'resources/odwn_orbn_gwg-LMF_1.3.xml'
    --output_folder=<output_path> 'output/'
    --allowed_prefixes=<allowed_prefixes> prefixes separated by +. options are r | c | o | t
    --exclude_sub_NUMBER=<include_sub_NUMBER> if True, identifiers that end with sub_NUMBER are not included
    --namespace=<namespace> the RDF namespace, e.g., http://premon.fbk.eu/resource/
    --short_namespace=<short_namespace> e.g., pm

Example:
    python main.py --orbn_path="resources/orbn_n-v-a.xml" --odwn_path="resources/odwn_orbn_gwg-LMF_1.3.xml" --output_folder="output" --allowed_prefixes="r+c" --exclude_sub_NUMBER="True" --namespace="http://premon.fbk.eu/resource/" --short_namespace="pm"
"""
import pickle
from docopt import docopt
from pathlib import Path
from lxml import etree
from odwn_classes import LE, Synset

import utils


# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS:')
print(arguments)

# load resource
orbn_path = arguments['--orbn_path']
odwn_path = arguments['--odwn_path']
orbn = etree.parse(orbn_path)
print(f'loaded: {orbn_path}')
odwn = etree.parse(odwn_path)
print(f'loaded: {odwn_path}')
allowed_prefixes = set(arguments['--allowed_prefixes'].split('+'))
exclude_sub_number_ids = arguments['--exclude_sub_NUMBER'] == 'True'

not_added = set()
# load orbn into classes
verbose = 1
sense_id2le_obj = dict()

for le_xml_obj in orbn.xpath('cdb_lu'):

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
        sense_id2le_obj[le_obj.sense_id] = le_obj
    else:
        not_added.add(le_obj.sense_id)

# inspect sense rankings
inconsistent_ids = utils.get_inconsistent_senseranks(sense_id2le_obj, verbose=verbose)
for inconsistent_id in inconsistent_ids:
    del sense_id2le_obj[inconsistent_id]

for inconsistent_id in inconsistent_ids:
    assert inconsistent_id not in sense_id2le_obj

# load synsets into classes
synset_id2synset_obj = dict()
for synset_xml_obj in odwn.xpath('Lexicon/Synset'):
    synset_obj = Synset(synset_xml_obj)
    synset_id2synset_obj[synset_obj.synset_id] = synset_obj


# load synset information about sense_id
sense_id2synset_info = dict()
for le_el in odwn.xpath('Lexicon/LexicalEntry'):
    sense_el = le_el.find('Sense')
    sense_id = sense_el.get('id')
    synset = sense_el.get('synset')
    if synset is not None:
        provenance_label = sense_el.get('provenance')
        provenance_set = set(provenance_label.split('+'))

        assert provenance_label
        assert provenance_set
        assert synset

        if synset == 'unknown_000':
            continue

        if synset in synset_id2synset_obj:
            sense_id2synset_info[sense_id] = {
                'synset_id': synset,
                'provenance_label': provenance_label,
                'provenance_set': provenance_set
            }
        else:
            if verbose:
                print(f'{synset} has no Synset xml element in LMF file')

# update both LE and Synset with relation between synonym and synset
for sense_id, synset_info in sense_id2synset_info.items():
    if sense_id in sense_id2le_obj:
        le_obj = sense_id2le_obj[sense_id]

        le_obj.provenance_label = synset_info['provenance_label']
        le_obj.provenance_set = synset_info['provenance_set']
        synset_id = synset_info['synset_id']
        le_obj.synset_id = synset_id

        if synset_id in synset_id2synset_obj:
            synset_obj = synset_id2synset_obj[synset_id]
            synset_obj.synonyms.append(le_obj)

output_dir = Path(arguments['--output_folder'])
orbn_out_path = str(output_dir / 'orbn.p')
with open(orbn_out_path, 'wb') as outfile:
    pickle.dump(sense_id2le_obj, outfile)
print(f'writting orbn information to: {orbn_path}')
print(f'# of ids not added due to settings or information not available: {len(not_added)}')
odwn_out_path = str(output_dir / 'odwn.p')
with open(odwn_out_path, 'wb') as outfile:
    pickle.dump(synset_id2synset_obj, outfile)
print(f'writting odwn information to: {odwn_out_path}')









