#!/bin/bash
python3 create_categorical.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null
python3 create_pyramid_categorical.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null
python3 create_experiment.py --compch 3 15 65  --outch 2 --grid false --maxvalue 3 7 --trainst false true --step null --datapath "/tigress/aligner/params/data/data_params_m2_noaugment.json"
