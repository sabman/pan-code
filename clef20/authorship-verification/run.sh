#!/bin/bash

# baseline script is representing documents using bag-of-character-ngrams model that is TFIDF weighted, cosine similarity between each document pair in the calibration data set is  calculated.

# resulting similarities are optimized, and projected through a simple rescaling operation, so that they can function as pseudo-probabilities, indiciating the likelihood that a document-pair is a same-author pair

# Input Pairs path:
# datasets/pan20-authorship-verification-training-small/pan20-authorship-verification-training-small.jsonl
# sample of data to check authors
# TODO: create this data by sampling pan20-authorship-verification-training-small.jsonl
# it has the following schema
# {"id": "6cced668-6e51-5212-873c-717f2bc91ce6", "fandoms": ["Guardians of Ga'Hoole", "Hetalia - Axis Powers"], "pair": ["I shift a bit, warily letting my eyes dart from one owl to the other -- but my ey
# {"id": "3c6c188a-db28-59aa-8c09-3d0f799ff579", "fandoms": ["Guardians of Ga'Hoole", "Warriors"], "pair": ["I shift a bit, warily letting my eyes dart from one owl to the other -- but my eyes are traine...

# head -n 1000 pan20-authorship-verification-training-small.jsonl >> input_pairs.jsonl
# tail -n 1000 pan20-authorship-verification-training-small.jsonl >> input_pairs.jsonl
# ➜ wc -l input_pairs.jsonl
#     2000 input_pairs.jsonl

input_pairs=datasets/pan20-authorship-verification-training-small/prepare/input_pairs.jsonl

# Input Truth path:
# datasets/pan20-authorship-verification-training-small/pan20-authorship-verification-training-small-truth.jsonl
# This is labeled pairs with just the document ids the schema looks as follows:
# {"id": "6cced668-6e51-5212-873c-717f2bc91ce6", "same": true, "authors": ["1446633", "1446633"]}
# {"id": "3c6c188a-db28-59aa-8c09-3d0f799ff579", "same": true, "authors": ["1446633", "1446633"]}
input_truth=datasets/pan20-authorship-verification-training-small/prepare/input_truth.jsonl

# Test Pairs Path:
# datasets/pan20-authorship-verification-test/truth.jsonl

# created by deleting first 1000 lines
# ➜ sed '1,1000d' pan20-authorship-verification-training-small.jsonl > test_pairs.jsonl
# ➜ wc -l test_pairs.jsonl
#    51601 test_pairs.jsonl

# then last 1000 lines
# ➜ mv test_pairs.jsonl test_pairs_d1000.jsonl
# ➜ tac  test_pairs_d1000.jsonl | sed "1,1000d" | tac > test_pairs.jsonl
# ➜ wc -l test_pairs.jsonl
#    50601 test_pairs.jsonl

test_pairs=datasets/pan20-authorship-verification-training-small/prepare/test_pairs.jsonl

python pan20-verif-baseline.py \
    -input_pairs=${input_pairs} \
    -input_truth=${input_truth} \
    -test_pairs=${test_pairs} \
    -num_iterations=0 \
    -output="out"


