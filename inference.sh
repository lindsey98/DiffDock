#!/bin/bash

# Directory containing the CSV files
data_dir="./data/"

# Base output directory
base_out_dir="./results/protein315_drugbank9k/"

# Get a count of the CSV files for progress indication
total_files=$(ls -1 "${data_dir}"*.csv | wc -l)
current_file=0

# Loop through all CSV files in the data directory
for csv_file in "${data_dir}"*.csv; do
    ((current_file++))
    # Extract the base name of the CSV file (without extension), this is the protein name
    base_name=$(basename "${csv_file}" .csv)

    # Construct the output directory path
    out_dir="${base_out_dir}${base_name}"

    # Display progress
    echo "Processing file ${current_file} of ${total_files}: ${csv_file}"

    # Run the Python command
    CUDA_VISIBLE_DEVICES=2,3 python -m inference \
        --protein_ligand_csv "${csv_file}" \
        --out_dir "${out_dir}" \
        --inference_steps 10 \
        --samples_per_complex 10 \
        --batch_size 10 \
        --actual_steps 10 \
        --no_final_step_noise
done