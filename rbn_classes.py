from lxml import etree


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

class LE:
    """

    """
    def __init__(self, id_, le_xml_obj, mw, verbose=0):

        self.id_ = id_
        self.mw = mw
        self.verbose = verbose

        self.lemma = self.get_lemma(le_xml_obj)

        self.pos = None
        self.rbn_type = None
        self.rbn_feature_set = None
        self.separable = None

        if not self.mw:
            self.pos = self.get_normalized_pos(le_xml_obj)

        if self.pos == 'v':
            self.rbn_type = self.get_rbn_type(le_xml_obj)
            self.rbn_feature_set = self.get_rbn_feature_set(le_xml_obj)
            self.separable = self.get_separable(le_xml_obj)

    def __str__(self):
        return f'{self.id_}, mw:{self.mw}, {self.lemma}, {self.pos}, {self.rbn_type}, {self.rbn_feature_set}'

    def get_lemma(self, le_xml_obj):
        if self.mw:
            child_label = 'MultiwordExpression'
        else:
            child_label = 'Lemma'

        lemma_el = le_xml_obj.find(child_label)
        lemma = lemma_el.get('writtenForm')
        return lemma

    def get_normalized_pos(self, le_xml_obj):
        rbn_pos = le_xml_obj.get('partOfSpeech')

        if rbn_pos == 'verb':
            return 'v'
        elif rbn_pos == 'noun':
            return 'n'
        elif rbn_pos == 'adjective':
            return 'a'
        elif rbn_pos == 'adverb':
            return 'r'
        elif rbn_pos == 'other':
            return 'o'
        else:
            raise ValueError(f'could not map rbn part of speech: {rbn_pos}')

    def get_rbn_type(self, le_xml_obj):
        rbn_type_info = le_xml_obj.find('Sense/Semantics-verb')
        children = rbn_type_info.getchildren()
        if children:
            semantic_type_els = rbn_type_info.xpath('semanticTypes[@semanticType]')

            semantic_type = extract_attribute_value_if_el_is_not_none(semantic_type_els,
                                                                      'semanticType',
                                                                      verbose=0)
        else:
            if self.verbose >= 2:
                print(f'no rbn type found for {self.id_}')
            semantic_type = None

        return semantic_type

    def get_separable(self, le_xml_obj):
        morphology_el = le_xml_obj.find('Morphology')
        if 'separability' in morphology_el.attrib:
            if morphology_el.attrib['separability'] == 'separable':
                return True
    
        return False

    def get_rbn_feature_set(self, le_xml_obj):
        rbn_type_info = le_xml_obj.find('Sense/Semantics-verb')
        children = rbn_type_info.getchildren()
        if children:
            feature_set_els = rbn_type_info.xpath('semanticTypes[@semanticFeatureSet]')

            feature_set = extract_attribute_value_if_el_is_not_none(feature_set_els,
                                                                    'semanticFeatureSet',
                                                                    verbose=0)
        else:
            if self.verbose >= 2:
                print(f'no rbn feature set found for {self.id_}')
            feature_set = None

        return feature_set





