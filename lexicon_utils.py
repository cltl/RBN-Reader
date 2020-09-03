import pickle
from collections import defaultdict

def get_verb_to_phrasal_entries(orbn_sense_id_to_obj,
                                verbose=0):
    """

    :param dict orbn_sense_id_to_obj: dict mapping the sense_id to
    an instance of odwn_classes.LE

    :rtype: dict
    :return: mapping from
    verb -> lemma -> ids
    e.g.,
    "bieden" -> "aanbieden" -> set of ids
    """
    verb_to_lemma_to_ids = {}

    phrasal_entries = 0
    for sense_id, sense_obj in orbn_sense_id_to_obj.items():

        if all([sense_obj.morpho_type == 'phrasal',
                len(sense_obj.parts) == 2]):
            particle, verb = sense_obj.parts

            if verb not in verb_to_lemma_to_ids:
                verb_to_lemma_to_ids[verb] = defaultdict(set)

            verb_to_lemma_to_ids[verb][sense_obj.lemma].add(sense_id)
            phrasal_entries += 1


    if verbose >= 1:
        print()
        print(f'phrasal entries: {phrasal_entries}')
        print(f'number of verb heads: {len(verb_to_lemma_to_ids)}')

    return verb_to_lemma_to_ids



if __name__ == "__main__":
    sense_id_to_sense_obj = pickle.load(open('output/orbn.p', 'rb'))
    get_verb_to_phrasal_entries(orbn_sense_id_to_obj=sense_id_to_sense_obj,
                                verbose=1)
