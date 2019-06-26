#!/bin/bash
python3 create_categorical.py --compch 3 9 15 21 45   --outch 2 --grid false --maxvalue 7 --trainst true --step null
python3 create_categorical.py --compch 3 5 7 9 11  --outch 2 --grid true --maxvalue 7 --trainst true --step null

python3 create_m4_categorical.py --compch 3 5 7 9 11  --outch 2 --grid true --maxvalue 7 --trainst true --step null
python3 create_m4_categorical.py --compch 3 9 15 21 45   --outch 2 --grid false --maxvalue 7 --trainst true --step null

python3 create_experiment.py --compch 3 5 7 9 11 --outch 2 --grid true --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model m4_categorical --name_flag noaug
python3 create_experiment.py --compch 3 5 7 9 11 --outch 2 --grid true --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_augment02.json" --model m4_categorical --name_flag aug02

python3 create_experiment.py --compch 3 9 15 21 45 --outch 2 --grid false --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model m4_categorical --name_flag noaug
python3 create_experiment.py --compch 3 9 15 21 45 --outch 2 --grid false --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_augment02.json" --model m4_categorical --name_flag aug02
