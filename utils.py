import pandas
import pickle
import sys
from collections import defaultdict, Counter

def load_orbn(path, package_dir):
    sys.path.append(package_dir)
    sense_id_to_sense_obj = pickle.load(open(path, 'rb'))
    sys.path.remove(package_dir)
    return sense_id_to_sense_obj

def split_morphostructure(morphostructure, lemma, verbose=0):
    parts = []

    if morphostructure is not None:
        morphostructure = morphostructure.replace('*', '')
        morphostructure = morphostructure.replace(']', '[')
        morphostructure = morphostructure.replace('<', '[')
        morphostructure = morphostructure.replace('>', '[')
        splitted = morphostructure.split('[')

        parts = []
        for split in splitted:
            if split:
                parts.append(split)

        if ''.join(parts) != lemma:
            parts = []
            if verbose >= 4:
                print(f'splits {splitted} do not join into original lemma {lemma}')

    return parts

def compute_stats_about(le_objs, attributes, verbose=0):
    """
    compute stats about the provided attributes
    
    :param list le_objs: list of rbn_classes.LE object
    :param set attributes: set of attributes to use in descriptive statistics
    :param
    :rtype: dict
    :return: {
     'count': number of observations
     '# of unique observations' : number of unique observations,
     'freq_dist': frequency distribution,
     'freq_dist_df' : frequency distribution as pandas dataframe
    }
    """
    observations = []
    
    for le_obj in le_objs.values():
        observation = [getattr(le_obj, attr)
                       for attr in attributes]
        observations.append(tuple(observation))
        

    
    freq_dist = Counter(observations)
    
    headers = ['-'.join(attributes), 
               'frequency']
    list_of_lists = [[key, freq]
                     for key, freq  in freq_dist.items()]
    df = pandas.DataFrame(list_of_lists, columns=headers)
    
    
    if verbose:
        print(f'chosen attributes: {attributes}')

        
    stats = {
        'count' : len(observations),
        '# of unique observations' : len(set(observations)),
        'freq_dist' : freq_dist,
        'freq_dist_df' : df.sort_values('frequency', ascending=False)
    }
    return stats


def load_mapping(path):
    
    df = pandas.read_excel(path, sheet_name='the_mapping')
    
    rbn_featureset2frames = dict()
    for index, row in df.iterrows():
        rbn_info = row['RBN feature set']
        frames = row['English FrameNet frames']
        frames = frames.split(',')

        rbn_featureset2frames[rbn_info] = frames

    return rbn_featureset2frames


def get_translations_from_wiktionary(path, verbose=0):
    """
    path to translations in csv
    (resources/wiktionary/translations.tsv)

    :param str path: the path to translations

    :rtype: tuple
    :return: (en to nl, nl to en)
    """
    path = 'resources/wiktionary/translations.tsv'
    df = pandas.read_csv(path, sep='\t', usecols=['ID', 'Concept_ID', 'Concept', 'Languoid', 'Language_name', 'Form'])

    if verbose:
        print()
        print(f'number of available languages: {len(set(df.Language_name))}')

    if verbose:
        print()
        print('languages that have Dutch in the name')
        for language in set(df.Language_name):
            if 'Dutch' in language:
                print(language)
        print('we use only: "Dutch; Flemish"')

    df = df[df.Language_name == 'Dutch; Flemish']

    english_lemmas = []
    english_definitions = []

    for index, row in df.iterrows():
        concept = row['Concept']
        lemma, *definitions = concept.split('/')
        english_lemmas.append(lemma)
        english_definitions.append('/'.join(definitions))
    df['English_lemma'] = english_lemmas

    dutch2english = defaultdict(set)
    english2dutch = defaultdict(set)

    for index, row in df.iterrows():
        english_lemma = row['English_lemma']
        dutch_lemma = row['Form']
        dutch2english[dutch_lemma].add(english_lemma)
        english2dutch[english_lemma].add(dutch_lemma)

    return dutch2english, english2dutch


def load_polysemy_info(le_objs, pos={'noun', 
                                     'verb', 
                                     'adjective',
                                     'adverb',
                                     'other'}):
    """
    """
    lemma_pos2le_ids = defaultdict(set)
    for le_obj in le_objs.values():
        if le_obj.rbn_pos in pos:
            key = (le_obj.lemma, le_obj.fn_pos)
            value = le_obj.sense_id
            lemma_pos2le_ids[key].add(value)

    list_of_lists = []
    headers = ['lemma_pos', 'polysemy', 'LU ids']
    
    le_id2polysemy_of_lemma = dict()
    for lemma_pos, le_ids in lemma_pos2le_ids.items():
        one_row = [lemma_pos, len(le_ids), le_ids]
        list_of_lists.append(one_row)
        
        for le_id in le_ids:
            le_id2polysemy_of_lemma[le_id] = len(le_ids)

    df = pandas.DataFrame(list_of_lists, columns=headers)
        
    freq_dict = Counter(df['polysemy'])
    total = sum(freq_dict.values())
    list_of_lists = []
    headers = ['Polysemy class', 'Freq', '%']
    for key, value in sorted(freq_dict.items()):
        one_row = [key, value, round((100 * (value / total)),2)]
        list_of_lists.append(one_row)
        
    
    distr_df = pandas.DataFrame(list_of_lists, columns=headers)
    
    return df, distr_df, lemma_pos2le_ids


def get_inconsistent_senseranks(rbn_objs, verbose=0):
    inconsistent_ids = set()

    lemma_pos2sense_ranks = defaultdict(list)
    for le_obj in rbn_objs.values():

        key = (le_obj.lemma, le_obj.rbn_pos)
        value = int(le_obj.c_seq_nr)

        if key not in lemma_pos2sense_ranks:
            lemma_pos2sense_ranks[key] = {
                'sense_ids': [],
                'senseranks': []

            }
        if key in lemma_pos2sense_ranks:
            lemma_pos2sense_ranks[key]['sense_ids'].append(le_obj.sense_id)
            lemma_pos2sense_ranks[key]['senseranks'].append(value)

    for (lemma, pos), info in lemma_pos2sense_ranks.items():

        senseranks = info['senseranks']
        if len(senseranks) != len(set(senseranks)):

            inconsistent_ids.update(info['sense_ids'])
            if verbose:
                print(f'inconsistent sense ids for: {lemma} {pos}')
                print(senseranks)
    return inconsistent_ids