"""
Load RBN as python classes

Usage:
  main.py --input_path=<input_path> --output_path=<output_path> --namespace=<namespace> --short_namespace=<short_namespace>

Options:
    --input_path=<input_path> 'resources/final/cornettoLMF2.11.xml'
    --output_path=<output_path> 'output/rbn.p'
    --namespace=<namespace> the RDF namespace, e.g., http://premon.fbk.eu/resource/
    --short_namespace=<short_namespace> e.g., pm

Example:
    python main.py --input_path="resources/final/cornettoLMF2.11.xml" --output_path="output/rbn.p" --namespace="http://premon.fbk.eu/resource/" --short_namespace="pm"
"""
import pickle
from docopt import docopt
from lxml import etree
from rbn_classes import LE


# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS:')
print(arguments)

# load resource
input_path = arguments['--input_path']
doc = etree.parse(input_path)
print(f'loaded: {input_path}')

# load resource into classes
verbose = 1
le_objs = []
for le_xml_obj in doc.xpath('Lexicon/LexicalEntry'):
    id_ = le_xml_obj.get('id')

    mw = '-mwe-' in id_

    le_obj = LE(id_,
                le_xml_obj,
                mw,
                arguments['--namespace'],
                arguments['--short_namespace'],
                verbose=verbose)

    if le_obj.lemma.startswith('-'):
        continue
    le_objs.append(le_obj)

output_path = arguments['--output_path']
with open(output_path, 'wb') as outfile:
    pickle.dump(le_objs, outfile)
print(f'writting output to: {output_path}')










