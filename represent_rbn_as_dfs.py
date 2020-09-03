"""
Represent Referentiebestand Nederlands based on
-lemma
-sense

Usage:
  represent_rbn_as_dfs.py\
   --path_to_pickled_orbn=<path_to_pickled_orbn>\
   --dataframe_folder=<dataframe_folder>

Options:
    --path_to_pickled_orbn=<path_to_pickled_orbn> path to pickled ORBN, probably at output/orbn.p
    --dataframe_folder=<dataframe_folder> where to store the dataframes



Example:
    python represent_rbn_as_dfs.py --path_to_pickled_orbn="output/orbn.p" --dataframe_folder="output/rbn_dataframes"
"""
from docopt import docopt
import pickle
from collections import defaultdict, Counter

import pandas

# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS')
print(arguments)
print()

senseid_to_sense_obj = pickle.load(open(arguments['--path_to_pickled_orbn'], 'rb'))

def get_lemma_df(id_to_senseobj):
    """

    :param id_to_senseobj:
    :return:
    """
    headers = ['lemma', 'pos', 'polysemy']
    list_of_lists = []

    lemma_pos_to_polysemy = defaultdict(int)

    for senseid, senseobj in id_to_senseobj.items():
        lemma_pos_to_polysemy[(senseobj.lemma,
                               senseobj.fn_pos)] += 1

    for (lemma, fn_pos), polysemy in lemma_pos_to_polysemy.items():
        one_row = [lemma, fn_pos, polysemy]
        list_of_lists.append(one_row)

    df = pandas.DataFrame(list_of_lists, columns=headers)
    return df

def get_sense_df(id_to_senseobj):
    """

    :param id_to_senseobj:
    :return:
    """


lemma_df = get_lemma_df(id_to_senseobj=senseid_to_sense_obj)
lemma_stats = lemma_df.describe()

print(lemma_df)