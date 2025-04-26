#!/bin/bash

dir="results"

for r in {1..100}
do
python run_atlucb_xss.py -s $r -t 100 -m 2 > $dir/atlucb.$r.csv
python postprocess.py -m 2 -c $dir/atlucb.$r.csv -s prop_of_success > "$dir/atlucb-$r.prop_of_success"
python run_uniform_xss.py -s $r -t 200 -m 2 > $dir/uniform.$r.csv
python postprocess.py -m 2 -c $dir/uniform.$r.csv -s prop_of_success > "$dir/uniform-$r.prop_of_success"
done