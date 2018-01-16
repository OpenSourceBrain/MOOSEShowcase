#!/bin/bash
( 
    cd ./tests/python/ 
    python test_function.py
    python test_kkit.py
    python test_moose_paths.py
    python test_pymoose.py
    python test_synchan.py
    python test_vec.py
)

