import pickle
from lxml import etree
from rbn_classes import LE

# load resource
cornetto_path = 'resources/final/cornettoLMF2.11.xml'
doc = etree.parse(cornetto_path)
print(f'loaded: {cornetto_path}')

# load resource into classes
verbose = 1
le_objs = []
for le_xml_obj in doc.xpath('Lexicon/LexicalEntry'):
    id_ = le_xml_obj.get('id')

    mw = '-mwe-' in id_

    le_obj = LE(id_, le_xml_obj, mw, verbose=verbose)
    key = (le_obj.lemma, le_obj.pos)

    if le_obj.lemma.startswith('-'):
        continue

    le_objs.append(le_obj)

output_path = 'output/rbn.p'
with open(output_path, 'wb') as outfile:
    pickle.dump(le_objs, outfile)
print(f'writting output to: {output_path}')










