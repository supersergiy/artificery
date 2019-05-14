#!/bin/bash
python3 create_pyramid_categorical.py --compch 3 15 65  --outch 2 --grid true  --maxvalue 3 7 --trainst false true --step null
python3 create_pyramid_categorical.py --compch 15  --outch 2 --grid true false  --maxvalue 3 --trainst true --step null
