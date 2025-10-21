#!/usr/bin/env bash

data_input_dir="datasets/oregano_dr/"
vocab_dir="datasets/oregano_dr/vocab"
total_iterations=1000
path_length=4
hidden_size=32
embedding_size=32
batch_size=128
learning_rate=0.0006
beta=0.05
num_rollouts=30
Lambda=0.02
LSTM_layers=2
eval_every=10
max_num_actions=400
use_entity_embeddings=1
train_entity_embeddings=1
train_relation_embeddings=1
base_output_dir="output/oregano_dr/"
model_load_dir="oregano_dr/model.ckpt"
load_model=1
nell_evaluation=0