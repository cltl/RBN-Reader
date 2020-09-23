
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

def extract_attribute_value_if_el_is_not_none(els, attribute_label, verbose=0):
    """
    given xml element.
    1. if el is None -> return None
    2. if el is not None -> extract attribute value

    :param list el: list of xml elements (of type lxml.etree._Element)
    :param str attribute_label: label attribute, e.g., 'id'

    :rtype: str
    :return: empty string or values concatenated with '-'
    """
    if not els:
        if verbose >= 1:
            print('no elements found')
        return ''

    values = set()
    for el in els:
        value = el.get(attribute_label)
        values.add(value)

        assert value is not None

    if els:
        assert values, 'values can not be empty since there are xml elements found'

    return '-'.join(values)


class Synset:
    """

    """

    def __init__(self, synset_xml_obj):
        self.ili = self.get_ili(synset_xml_obj)
        self.synset_id = self.get_synset_id(synset_xml_obj)
        self.definition = self.get_definition(synset_xml_obj)

        self.synonyms = []

    def get_hover_info(self):
        return {
            'synset identifier': self.synset_id,
            'definition': self.definition,
            'synonyms' : {rbn_obj.short_rdf_uri
                          for rbn_obj in self.synonyms}
        }

    def get_ili(self, synset_xml_obj):
        return synset_xml_obj.get('ili')

    def get_synset_id(self, synset_xml_obj):
        return synset_xml_obj.get('id')

    def get_definition(self, synset_xml_obj):
        def_el = synset_xml_obj.find('Definitions/Definition')
        if def_el is not None:
            return synset_xml_obj.find('Definitions/Definition').get('gloss')
        else:
            return ""



class LE:
    """

    """
    def __init__(self,
                 le_xml_obj,
                 namespace,
                 abbreviated_namespace,
                 verbose=0):

        self.add = True # if set to False, sense will not be used
        self.namespace = namespace
        self.abbreviated_namespace = abbreviated_namespace

        self.sense_id = le_xml_obj.get('c_lu_id')
        self.prefix = self.sense_id[0]
        self.c_seq_nr = le_xml_obj.get('c_seq_nr')
        assert self.sense_id

        self.verbose = verbose

        self.lemma = self.get_lemma(le_xml_obj)
        self.article = None
        self.parts = []

        self.sense_label = None
        self.definition = None
        self.rbn_pos = None
        self.simple_pos = None
        self.morpho_type = None
        self.lu_type = None
        self.morpho_structure = None
        self.fn_pos = None
        self.rbn_type = None
        self.rbn_feature_set = None
        self.separable = None
        self.provenance_set = None
        self.provenance_label = None # how the synonym was added to a synset
        self.synset_id = None # synset id to which it belongs in ODWN

        self.canonical_forms = self.get_canonical_forms(le_xml_obj)

        self.rbn_pos = self.get_rbn_pos(le_xml_obj)
        if self.rbn_pos is not None:
            self.article = self.get_article(le_xml_obj)
            self.simple_pos = self.get_simple_pos()
            self.definition = self.get_definition(le_xml_obj)
            self.fn_pos = self.get_fn_pos()
            self.sense_label = f'{self.lemma}-{self.simple_pos}-{self.c_seq_nr}'
            self.morpho_type = self.get_morpho_type(le_xml_obj)
            self.lu_type = self.get_lu_type()
            self.sem_type = self.get_sem_type(le_xml_obj)
            self.morpho_structure = self.get_morpho_structure(le_xml_obj)
            self.parts = split_morphostructure(morphostructure=self.morpho_structure,
                                               lemma=self.lemma)

            self.full_rdf_uri = f'{self.namespace}RBN-{self.sense_label}'
            self.short_rdf_uri = f'({self.abbreviated_namespace})RBN-{self.sense_label}'

        if self.simple_pos == 'v':
            self.rbn_feature_set = self.get_rbn_feature_set(le_xml_obj)
            #self.separable = self.get_separable(le_xml_obj)

    def __str__(self):
        return str(self.get_hover_info())


    def get_hover_info(self):
        return {
            'pos' : self.fn_pos,
            'lemma' : self.lemma,
            'sense_label' : self.sense_label,
            'sense_id' : self.sense_id,
            'rbn_type' : self.rbn_type,
            'rbn_feature_set' : self.rbn_feature_set,
            'definition' : self.definition,
            'canonical_forms' : ';'.join(self.canonical_forms.values()),
            'synset_id' : self.synset_id
        }

    def get_fn_nltk_format(self,
                           frame,
                           lu_name,
                           provenance,
                           status="Created",
                           incorporated_fe=None,
                           timestamp=None,
                           optional_lu_attrs={}):

        attributes_to_annotate = set()

        lexemes, complete = self.get_lexemes()

        if self.lu_type is None:
            complete = False
            attributes_to_annotate.add('lu_type')

        lu = {
            "lexemes" : lexemes,
            "definition" : self.definition,
            "lu_name" : lu_name,
            "lu_type" : self.lu_type,
            "status" : status,
            "POS" : self.fn_pos,
            "frame" : frame,
            "provenance" : provenance,
            "incorporated_fe" : incorporated_fe,
            "timestamp" : timestamp,
            "optional_lu_attrs" : optional_lu_attrs
        }

        if not complete:
            attributes_to_annotate.add('lexemes')

        for attr in ['definition',
                     'status',
                     'POS',
                     'frame',
                     'provenance']:
            value = lu[attr]
            if not value:
                attributes_to_annotate.add(attr)

        return lu, attributes_to_annotate

    def get_morpho_type(self, le_xml_obj):
        morpho_type = None
        morph_type_el = le_xml_obj.find(f'morphology_{self.rbn_pos}/morpho-type')

        if morph_type_el is not None:
            morpho_type = morph_type_el.text

        return morpho_type


    def get_article(self, le_xml_obj):
        article_el = le_xml_obj.find(f'syntax_{self.rbn_pos}/sy-article')

        if article_el is None:
            article = None
        else:
            article = article_el.text

        return article


    def get_lu_type(self):
        if self.morpho_type in {'simpmorph',
                                'derivation',
                                'xderivation',
                                'zeroderivation',
                                'nmorph'}:
            lu_type = 'singleton'
        elif self.morpho_type in {'phrasal'}:
            lu_type = 'phrasal'
        elif self.morpho_type in {'xcompound',
                                  'x-compound'}:
            lu_type = 'exocentric compound'
        elif self.morpho_type is None:
            lu_type = None
        elif self.morpho_type in {'compound',
                                  'wordgroup',
                                  'compderiv',
                                  'derivcomp',
                                  'unspecified',
                                  'nil'}:
            lu_type = None

        else:
            raise Exception(f'no mapping available for morphotype {self.morpho_type}')


        return lu_type

    def get_lexemes(self):

        complete = False

        if self.lu_type is None:
            lexemes = []
        elif self.lu_type in {'singleton',
                              'exocentric compound'}:
            lexemes = [{
                "order": "1",
                "headword": "false",
                "breakBefore": "false",
                "POS": self.fn_pos,
                "name": self.lemma
            }]
            complete = True

        elif self.morpho_type == 'compound':
            lexemes = []
            for order, part in enumerate(self.parts, 1):
                lexeme = {
                    'order': str(order),
                    'breakBefore': "false",
                    "name": part,
                }
                if order < len(self.parts):
                    lexeme['headword'] = 'false'

                    if all([len(self.parts) == 3,
                            order == 2,
                            part in {'s', 'e', 'en', 'n', 'ne', 'er'}]):
                        lexeme['POS'] = 'I'
                else:
                    lexeme['POS'] = self.fn_pos
                    lexeme['head'] = 'true'
                lexemes.append(lexeme)

        elif all([self.lu_type in {'phrasal'},
                  len(self.parts) == 2]):

            part_one, part_two = self.parts
            lexemes = [
                {
                    'order' : '1',
                    'breakBefore' : "false",
                    "name" : part_one,
                    "headword": 'false',
                },
                {
                    'order': '2',
                    'breakBefore': "false",
                    "name": part_two,
                    "headword": 'false',
                    "POS": self.fn_pos
                }
            ]
            complete = True
        else:
            lexemes = []

        return lexemes, complete


    def get_lemma(self, le_xml_obj):
        form_el = le_xml_obj.find('form')

        if form_el is None:
            self.add = False
            lemma = None
        else:
            lemma = form_el.get('form-spelling')

        if not lemma:
            self.add = False

        return lemma


    def get_rbn_pos(self, le_xml_obj):
        form_el = le_xml_obj.find('form')

        if form_el is None:
            self.add = False
            pos = None
        else:
            pos = form_el.get('form-cat')
            pos = pos.lower()

            if pos == 'adjective':
                pos = 'adj'

        if not pos:
            self.add = False

        return pos

    def get_sense_id(self, le_xml_obj):
        sense_el = le_xml_obj.find('Sense')
        sense_id = sense_el.get('senseId')
        return sense_id

    def get_definition(self, le_xml_obj):
        definition = None

        if self.simple_pos == 'v':
            query = 'sem-definition/sem-def'
        elif self.simple_pos == 'n':
            query = 'sem-definition/sem-def-noun/sem-specificae'
        elif self.simple_pos == 'a':
            query = 'semantics_adj/sem-resume'

        sem_def_el = le_xml_obj.find(query)
        if sem_def_el is not None:
            definition = sem_def_el.text
            if definition is None:
                if self.verbose >= 1:
                    print(f'no definition for {self.sense_id} {definition}')

        return definition

    def get_canonical_forms(self, le_xml_obj):
        canonical_forms = dict()
        for example_el in le_xml_obj.xpath('examples/example'):
            example_id = example_el.get('r_ex_id')
            canonicalform_el = example_el.find('form_example/canonicalform')
            example = canonicalform_el.text

            if example:
                canonical_forms[example_id] = example
        return canonical_forms


    def get_simple_pos(self):
        if self.rbn_pos == 'verb':
            return 'v'
        elif self.rbn_pos == 'noun':
            return 'n'
        elif self.rbn_pos == 'adj':
            return 'a'
        else:
            raise ValueError(f'could not map rbn part of speech: {self.rbn_pos}')

    def get_fn_pos(self):
        if self.rbn_pos == 'verb':
            return 'V'
        elif self.rbn_pos == 'noun':
            return 'N'
        elif self.rbn_pos == 'adj':
            return 'A'
        else:
            raise ValueError(f'could not map rbn part of speech: {self.rbn_pos}')


    def get_sem_type(self, le_xml_obj):
        rbn_type_info = le_xml_obj.find(f'semantics_{self.rbn_pos}/sem-type')

        if rbn_type_info is None:
            semantic_type = None
        else:
            semantic_type = rbn_type_info.text

        return semantic_type

    def get_morpho_structure(self, le_xml_obj):
        morpho_struc_el = le_xml_obj.find(f'morphology_{self.rbn_pos}/morpho-structure')

        if morpho_struc_el is None:
            morphostructure = None
        else:
            morphostructure = morpho_struc_el.text

        return morphostructure

    def get_rbn_feature_set(self, le_xml_obj):
        rbn_type_info = le_xml_obj.find('semantics_verb/sem-caseframe/caseframe')

        if rbn_type_info is None:
            rbn_feature_set = None
        else:
            rbn_feature_set = rbn_type_info.text
        return rbn_feature_set

    def get_separable(self, le_xml_obj):
        morphology_el = le_xml_obj.find('Morphology')
        if 'separability' in morphology_el.attrib:
            if morphology_el.attrib['separability'] == 'separable':
                return True

        return False





