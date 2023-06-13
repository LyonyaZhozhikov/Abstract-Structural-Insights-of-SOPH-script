import os
from datetime import datetime

folder_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
os.makedirs(folder_name, exist_ok=True)

mode = input("Enter mode (normal or mut): ")

while True:
    protein_name = input("Enter protein name (or 'q' to quit): ")
    if protein_name == 'q':
        break
    amino_acids = input("Enter amino acid sequence: ")

    while True:
        positions = input("Enter positions to analyze (comma-separated) (or 'n' for new protein): ")
        if positions == 'n':
            break
        positions = [int(pos) for pos in positions.split(",")]

        substitutions = []
        if mode == "mut":
            while True:
                substitutions = input("Enter substituted amino acids (comma-separated): ").split(",")
                if len(substitutions) != len(positions):
                    print("Warning: Number of positions and substitutions do not match.")
                else:
                    break

        for i, position in enumerate(positions):
            start = max(0, position - 200)
            end = min(len(amino_acids), position + 199)
            subsequence = amino_acids[start:end]

            if mode == "mut" and i < len(substitutions):
                substitution = substitutions[i]
                print(f"Here is your mutagenesis sequence: {amino_acids[position-5:position-1]}>{amino_acids[position-1]}<{amino_acids[position:position+4]}")
                mutated_subsequence = subsequence[:199] + substitution + subsequence[200:]

                timestamp = datetime.now().strftime("%H-%M-%S")
                command = f'curl -X POST --data "{mutated_subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > {folder_name}/{protein_name}_{position}_{timestamp}_mutated.pdb'
                os.system(command)

            timestamp = datetime.now().strftime("%H-%M-%S")
            command = f'curl -X POST --data "{subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > {folder_name}/{protein_name}_{position}_{timestamp}.pdb'
            os.system(command)
