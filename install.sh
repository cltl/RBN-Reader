#!/usr/bin/env bash


rm -rf resources
mkdir resources
cd resources
wget https://github.com/cltl/OpenDutchWordnet/raw/master/resources/odwn/orbn_n-v-a.xml.gz
gunzip orbn_n-v-a.xml.gz

wget https://github.com/cltl/OpenDutchWordnet/raw/master/resources/odwn/odwn_orbn_gwg-LMF_1.3.xml.gz
gunzip odwn_orbn_gwg-LMF_1.3.xml.gz

cd ..

mkdir -p output

python main.py --orbn_path="resources/orbn_n-v-a.xml" --odwn_path="resources/odwn_orbn_gwg-LMF_1.3.xml" --output_folder="output" --allowed_prefixes="r+c" --exclude_sub_NUMBER="True" --namespace="http://premon.fbk.eu/resource/" --short_namespace="pm"
python convert_mapping_to_json.py --path_to_excel="mapping_to_fn/Mapping.xlsx" --json_output_path="mapping_to_fn/mapping.json"
cd ..
