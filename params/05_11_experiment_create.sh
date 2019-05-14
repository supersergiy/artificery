#!/bin/bash
python3 create_experiment.py --compch 3 15 65  --outch 2 --grid true  --maxvalue 3 7 --trainst false true --step null --datapath "~/aligner/params/data/data_params_m2_noaugment.json"
python3 create_experiment.py --compch 15  --outch 2 --grid true false  --maxvalue 3 --trainst true --step null --datapath "~/aligner/params/data/data_params_m2_noaugment.json" --name_flag noaug
