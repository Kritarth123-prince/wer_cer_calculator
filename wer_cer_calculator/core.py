import os
import csv
import argparse
import pkg_resources
import pandas as pd
from distance import levenshtein

def load_data(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '\t' in line:
                filename, text = line.split('\t', 1)
                normalized_filename = os.path.splitext(filename)[0]
                data[normalized_filename] = text
    return data

def get_version():
    try:
        return pkg_resources.get_distribution("wer_cer_calculator").version
    except pkg_resources.DistributionNotFound:
        return "Package not installed!" 

def create_csv(gt_file, hyp_file, output_csv):
    gt_data = load_data(gt_file)
    hyp_data = load_data(hyp_file)

    common_filenames = set(gt_data.keys()) & set(hyp_data.keys())

    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['filename', 'ground_truth', 'hypothesis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename in common_filenames:
            writer.writerow({
                'filename': filename,
                'ground_truth': gt_data[filename],
                'hypothesis': hyp_data[filename]
            })

    print(f"CSV file created with {len(common_filenames)} entries at: {output_csv}")
    return pd.read_csv(output_csv)

# Calculate Word Error Rate (WER) and Character Error Rate (CER) from a CSV file.
def calculate_wer_cer(references, predictions):
    if len(references) == 0 or len(predictions) == 0:
        print("No valid data for WER/CER calculation. Check the input data.")
        return

    # Calculate WER and CER manually using Levenshtein distance
    wer_score = calculate_wer(references, predictions)
    cer_score = calculate_cer(references, predictions)

    print(f"Word Error Rate (WER): {wer_score * 100:.2f}%")
    print(f"Character Error Rate (CER): {cer_score * 100:.2f}%")

# Calculate Word Error Rate (WER) using Levenshtein distance.
def calculate_wer(references, predictions):
    total_words = 0
    total_edits = 0

    for ref, pred in zip(references, predictions):
        ref_words = ref.split()
        pred_words = pred.split()

        total_words += len(ref_words)
        total_edits += levenshtein(ref_words, pred_words)

    return total_edits / total_words if total_words > 0 else 0

# Calculate Character Error Rate (CER) using Levenshtein distance.
def calculate_cer(references, predictions):
    total_chars = 0
    total_edits = 0

    for ref, pred in zip(references, predictions):
        total_chars += len(ref)
        total_edits += levenshtein(ref, pred)

    return total_edits / total_chars if total_chars > 0 else 0

def main():
    parser = argparse.ArgumentParser(
        description="Calculate Word Error Rate (WER) and Character Error Rate (CER) from ground truth and hypothesis text data."
    )
    parser.add_argument("--gt_file", type=str, required=True, help="Path to the ground truth file.")
    parser.add_argument("--hyp_file", type=str, required=True, help="Path to the hypothesis file.")
    parser.add_argument("--output_csv", type=str, help="Path to the output CSV file. Optional.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {get_version()}")

    args = parser.parse_args()

    # Load ground truth and hypothesis data
    gt_data = load_data(args.gt_file)
    hyp_data = load_data(args.hyp_file)

    # Find common filenames
    common_filenames = set(gt_data.keys()) & set(hyp_data.keys())
    references = [gt_data[filename] for filename in common_filenames]
    predictions = [hyp_data[filename] for filename in common_filenames]

    # If output_csv is provided, create the CSV file
    if args.output_csv:
        create_csv(args.gt_file, args.hyp_file, args.output_csv)
    
    # Calculate WER and CER
    calculate_wer_cer(references, predictions)

if __name__ == "__main__":
    main()
