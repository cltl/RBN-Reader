import sys
sys.path.append('../..')

import ODWN_reader

senseid_to_lu = ODWN_reader.senseid_to_uri

print(len(senseid_to_lu))
