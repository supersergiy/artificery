#!/bin/bash
python3 create_categorical.py --compch 5 --outch 2 --grid true --maxvalue 7 --trainst true --step null
python3 create_architecture.py --name instnorm_categorical  --compch 5 --outch 2 --grid true --maxvalue 7 --trainst true --step null
python3 create_architecture.py --name m4_categorical  --compch 5 --outch 2 --grid true --maxvalue 7 --trainst true --step null

python3 create_categorical.py --compch 15 --outch 2 --grid false --maxvalue 7 --trainst true --step null
python3 create_architecture.py --name instnorm_categorical  --compch 15 --outch 2 --grid false --maxvalue 7 --trainst true --step null
python3 create_architecture.py --name m4_categorical  --compch 15 --outch 2 --grid false --maxvalue 7 --trainst true --step null

python3 create_experiment.py --compch 5 --outch 2 --grid true --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model instnorm_categorical --name_flag noaug
python3 create_experiment.py --compch 15 --outch 2 --grid false --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model instnorm_categorical --name_flag noaug

python3 create_experiment.py --compch 5 --outch 2 --grid true --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model m4_categorical --name_flag noaug
python3 create_experiment.py --compch 15 --outch 2 --grid false --maxvalue 7 --trainst true --step null --datapath "/tigress/popovych/aligner/params/data/data_params_m2_noaugment.json" --model m4_categorical --name_flag noaug
