import sys
sys.path.insert(0, '../../')

import ODWN_reader

orbn_in_lemon = ODWN_reader.load_orbn_in_lemon(ODWN_reader.orbn_lemon_path)

print(orbn_in_lemon)