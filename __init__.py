import os
from rdflib import Graph

from .utils import load_orbn
from .rdf_utils import convert_rbn_to_lemon, load_orbn_in_lemon, get_senseid_to_lu_uri

# load sense_id to RBN sense object
package_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(package_dir, 'output/orbn.p')
senseid_to_sense_obj = load_orbn(path,
                                 package_dir)
print(f'loaded {len(senseid_to_sense_obj)} RBN senses')

from .lexicon_utils import get_verb_to_phrasal_entries
verb_to_phrasal_entries = get_verb_to_phrasal_entries(orbn_sense_id_to_obj=senseid_to_sense_obj,
                                                      verbose=2)


orbn_lemon_path = os.path.join(package_dir, 'output', 'orbn_1.0.ttl')
if not os.path.exists(orbn_lemon_path):
    rbn_pos_to_lexinfo = {
      "adj" : "http://www.lexinfo.net/ontology/3.0/lexinfo#adjective",
      "noun" : "http://www.lexinfo.net/ontology/3.0/lexinfo#noun",
      "verb" : "http://www.lexinfo.net/ontology/3.0/lexinfo#verb"
    }
    lemon_ttl_path = os.path.join(package_dir, 'resources', 'lemon', 'lemon.ttl')
    lemon = Graph()
    lemon.parse(lemon_ttl_path, format='turtle')

    rbn_in_lemon = convert_rbn_to_lemon(senseid_to_senseobj=senseid_to_sense_obj,
                                        namespace='http://rdf.cltl.nl/rbn/',
                                        lemon=lemon,
                                        major_version=1,
                                        minor_version=0,
                                        rbn_pos_to_lexinfo=rbn_pos_to_lexinfo,
                                        language='nld',
                                        output_path=orbn_lemon_path,
                                        verbose=2)



