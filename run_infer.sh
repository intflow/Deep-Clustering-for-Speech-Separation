#!/bin/bash


python create_scp_test.py
python test.py -scp ./scp/tt_mix.scp -opt ./config/train.yml -save_file /DL_data_big/AIGC_3rd_track3/DC_results