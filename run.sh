#!/usr/bin/env bash

# Get just the name of the current file
CURRENT_FILE=${0}

ts-node-esm ${CURRENT_FILE}.ts $@