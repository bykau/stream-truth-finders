#!/bin/bash

source ../../../../bin/activate
export PYTHONPATH="${PYTHONPATH}:/home/evgeny/wonderful_programming/data-truth-finders/stream-truth-finders/"

vopros[0]=0.0
vopros[1]=0.1
vopros[2]=0.2
vopros[3]=0.3
vopros[4]=0.4
vopros[5]=0.5
vopros[6]=0.6
vopros[7]=0.7
vopros[8]=0.8
vopros[9]=0.9
vopros[10]=1.0

echo "Calculate..."
for p_t in "${vopros[@]}"; do
    for f0 in "${vopros[@]}"; do
        for i in 1 2 3 4 5 6 7 8 9 10; do
            python ../data_generator/generator.py $p_t $f0
            if [ $? -ne 0 ]; then
                echo "FAIL"
                exit 1
            fi
            python main.py
            if [ $? -ne 0 ]; then
                echo "FAIL 2"
                exit 2
            fi
        done
    done
done

echo "Done!"
exit 0