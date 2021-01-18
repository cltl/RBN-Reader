# ODWN-Reader

The goal of this repository is to load Open Dutch WordNet
into Python classes as well as compute descriptive statistics.

### Prerequisites
Python 3.6 was used to create this project. It might work with older versions of Python.

### Installing

A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

Also, please download the relevant resources by calling:
```bash 
bash install.sh
```

## Functionality

### Function 1: load ORBN senses
```python
import ODWN_reader
senseid_to_sense_obj = ODWN_reader.senseid_to_sense_obj
```
*senseid_to_sense_obj* is mapping from a sense identifier to a LE object.
We included two types of sense identifiers:
* **r_**: RBN
* **c_**: Cornetto

The definition of the LE object is found in *odwn_classes.LE*.

### Function 2: load phrasal entries
```
import ODWN_reader
verb_to_phrasal_entries = ODWN_Reader.verb_to_phrasal_entries
```
*verb_to_phrasal_entries* conains a mapping from a verb head, e.g., "bieden",
to all phrasal entries in RBN that are marked as "phrasal" (morpho_type == 'phrasal').

### Function 3: ORBN in Lemon 
You can load ORBN in Lemon the following way:

```python 
import ODWN_reader
orbn_in_lemon = ODWN_reader.load_orbn_in_lemon(ODWN_reader.orbn_lemon_path)
```

### Function: mapping senseid to URI
You can load a mapping from an ORBN sense id to a URI of the sense.

```python
import ODWN_reader 
orbn_in_lemon = ODWN_reader.load_orbn_in_lemon(ODWN_reader.orbn_lemon_path)
senseid_to_lu = ODWN_reader.get_senseid_to_lu_uri(orbn_in_lemon, verbose=2)
```

## TODO
* RDF namespace of WordNet 3.0
* synonymy information
* add English information about synset
* it seems that not all English WordNet synsets have an XML element in the LMF file

## Authors
* **Marten Postma** (m.c.postma@vu.nl)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
