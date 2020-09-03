import os

from .utils import load_orbn

# load sense_id to RBN sense object
package_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(package_dir, 'output/orbn.p')
senseid_to_sense_obj = load_orbn(path,
                                 package_dir)
print(f'loaded {len(senseid_to_sense_obj)} RBN senses')

from .lexicon_utils import get_verb_to_phrasal_entries
verb_to_phrasal_entries = get_verb_to_phrasal_entries(orbn_sense_id_to_obj=senseid_to_sense_obj,
                                                      verbose=2)
