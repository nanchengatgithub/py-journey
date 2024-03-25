#!/usr/bin/env python

# this script runs StimPlan simulation
# Nov. 2020

import glob
import os
import shutil
from hfm_fracture_modeling import wellname, input_vars

stp_exe = '/project/res/bin/stimplan '
input_path = 'resinsight/input/'

lastdata_files = glob.glob('stimplan/input/*.FRK')
print(lastdata_files)

models = glob.glob(f'stimplan/model/{wellname}/*')
print('StimPlan models: ', models)

for model in models:
    model_dir = os.path.join(f'stimplan/output/{wellname}', model.split('/')[-1])
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    run_dir = os.path.join(model_dir, 'mainfrac')

    lastdata = input_vars['default_base_data']

    job_id = model.split('/')[-1].split('_')[0]

    for lastdata_file in lastdata_files:
        if job_id in lastdata_file and 'mainfrac' in lastdata_file:
            lastdata = lastdata_file

    print(f'Job ID: {job_id}; StimPlan basefile: {lastdata}; StimPlan Model: {model}')

    geo = model + '/Geological.frk'     # -g
    dev = model + '/Deviation.frk'      # -e
    perfs = model + '/Perfs.frk'        # -p
    asym = model + '/Asymmetric.frk'    # -y 

    impl = ' --implicit=on'
    maxruns5 = ' --maxruns=5'

    stp = f'\n{stp_exe} -d {run_dir} -i {lastdata} -g {geo} -e {dev} -p {perfs} {maxruns5}'
    print(stp) 

    print('\nCurrent running model: ', model)
    print('StimPlan base file for current running model: ', lastdata, '\n')

    if os.path.isdir(run_dir):
        shutil.rmtree(run_dir)
    os.system(stp)

    src = os.path.join(run_dir, 'contour.xml')
    if os.path.exists(src):
        print('\nStimPlan simulation result file found: ' + src)
        name = model.split('/')[-1] + '.xml'
        dst = os.path.join(input_path, name)
        shutil.copyfile(src, dst)
        print('Copied file: ' + src + ' to ' + dst + '\n')

    else:
        print("StimPlan simulation result file contour.xml NOT found in: " + run_dir)
        exit
  
            
#### move the folder 'Log' generated by StimPlan to 'stimplan/Log'
original = r'Log'
target = r'stimplan/log'

if os.path.isdir(original):
    shutil.move(original, target)
