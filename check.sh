#!/bin/bash

DIR=${1:-.}

for file in "$DIR"/*; do
    if [[ -f "$file" ]]; then
        value=$(awk 'NR==22 {print $5}' "$file")
        if [[ "$value" == "1" ]]; then
            echo "$file → wartość: $value"
        fi
    fi
done

