#!/bin/bash


python create_scp_test.py
python test.py -scp ./scp/tt_mix.scp -opt ./config/train.yml -save_file /DL_data_big/AIGC_3rd_track3/2020_track3_rev/t3_audio.TAUVAD.DPCL
#python test.py -scp ./scp/tt_mix.scp -opt ./config/train.yml -save_file /DL_data_big/AIGC_3rd_track3/Mono_100_test/DPCL