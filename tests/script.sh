#!/bin/bash

# Check if the Python file is passed as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <python_file>"
    exit 1
fi

# Python file to execute
python_file=$1

# Check if the file exists
if [ ! -f "$python_file" ]; then
    echo "Error: File '$python_file' not found."
    exit 1
fi

# Number of runs
num_runs=5
total_time=0

number_regex='^-?[0-9]+(\.[0-9]+)?([eE]-?[0-9]+)?$'

# Run the Python program multiple times
for i in $(seq 1 $num_runs); do
    echo "Run $i..."
    # Capture the output of the Python script
    result=$(python3 "$python_file" 2>/dev/null | tail -n 1)
    
    # Check if the result is numeric (supports scientific notation)
    if [[ "$result" =~ $number_regex ]]; then
        # Add the result to the total
        total_time=$(echo "$total_time + $result" | bc -l)
    else
        echo "Error: Run $i returned a non-numeric value ('$result'). Skipping..."
    fi
done

# Calculate the average
average=$(echo "$total_time / $num_runs" | bc -l)

# Print the average
echo "Average time: $average seconds"
