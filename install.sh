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
