#!/bin/bash
python3 create_categorical.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null
python3 create_m4_categorical.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null
#python3 create_experiment.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model m4_categorical --name_flag noaug
python3 create_experiment.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_augment02.json" --model m4_categorical --name_flag aug02
