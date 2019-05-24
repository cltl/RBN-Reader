#!/usr/bin/env bash


rm -rf resources
mkdir resources
cd resources
wget https://github.com/cltl/OpenDutchWordnet/raw/master/resources/odwn/orbn_1.0.xml.gz
gunzip orbn_1.0.xml.gz

wget https://github.com/cltl/OpenDutchWordnet/raw/master/resources/odwn/odwn_orbn_gwg-LMF_1.3.xml.gz
gunzip odwn_orbn_gwg-LMF_1.3.xml.gz

cd ..

mkdir -p output
