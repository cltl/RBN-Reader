import sys
sys.path.append('../..')

import ODWN_reader

orbn_in_lemon = ODWN_reader.load_orbn_in_lemon(ODWN_reader.orbn_lemon_path)
senseid_to_lu = ODWN_reader.get_senseid_to_lu_uri(orbn_in_lemon, verbose=2)
