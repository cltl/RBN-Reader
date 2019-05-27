# ODWN-Reader

The goal of this repository is to load Open Dutch WordNet
into Python classes as well as compute descriptive statistics.

### Prerequisites
Python 3.7 was used to create this project. It might work with older versions of Python.

### Installing

A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

## How to use
```bash
python main.py -h
```
For more information about how to use.

## TODO
* add adverbs and adjectives from RBN
* RDF namespace of WordNet 3.0
* synonymy information
* add English information about synset
* make hover_info a method in all classes instead of attribute

## Information

The sense ids mean:
* **r_**: RBN
* **c_**: Cornetto
* **o_**: -
* **t_n**: translation

## Authors

* **Marten Postma** (m.c.postma@vu.nl)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
