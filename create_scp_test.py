import os

test_mix_scp = 'scp/tt_mix.scp'
test_s1_scp = 'scp/tt_s1.scp'
test_s2_scp = 'scp/tt_s2.scp'
#test_mix = '/DL_data_big/AIGC_3rd_track3/Mono_100_test/mix'
#test_s1 = '/DL_data_big/AIGC_3rd_track3/Mono_100_test/mix'
#test_s2 = '/DL_data_big/AIGC_3rd_track3/Mono_100_test/mix'
test_mix = '../wav_tmp/DPCL_optim'
test_s1 = '../wav_tmp/DPCL_optim'
test_s2 = '../wav_tmp/DPCL_optim'


tt_mix = open(test_mix_scp,'w')
for root, dirs, files in os.walk(test_mix):
    files.sort()
    for file in files:
        tt_mix.write(file+" "+root+'/'+file)
        tt_mix.write('\n')


tt_s1 = open(test_s1_scp,'w')
for root, dirs, files in os.walk(test_s1):
    files.sort()
    for file in files:
        tt_s1.write(file+" "+root+'/'+file)
        tt_s1.write('\n')


tt_s2 = open(test_s2_scp,'w')
for root, dirs, files in os.walk(test_s2):
    files.sort()
    for file in files:
        tt_s2.write(file+" "+root+'/'+file)
        tt_s2.write('\n')
