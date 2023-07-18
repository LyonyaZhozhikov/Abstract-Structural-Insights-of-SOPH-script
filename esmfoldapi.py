import os
from datetime import datetime


while True:
    protein_name = input("Enter protein name (or 'q' to quit): ")
    if protein_name == 'q':
        break
    amino_acids = input("Enter whole amino acid sequence: ")
    while True:
        # timestamp = datetime.now().strftime("%H-%M-%S")
        folder_date = datetime.now().strftime("%m-%d-%Y")
        folder_name = f"{protein_name}_{folder_date}"
        os.makedirs(folder_name, exist_ok=True)

        # separation
        position = input("Enter position and variant like this - '1914H,200R and so on' (or 'n' for new protein): ")
        if position == 'n':
            break
        aa_numbers = []
        aa_change = []

        for item in position.split(','):
            aa_numbers.append(int(''.join(filter(str.isdigit, item))))
            aa_change.append(''.join(filter(str.isalpha, item)))

        for i in range(len(aa_numbers)):

            # cycle
            position = int(aa_numbers[i])
            substitution = str(aa_change[i])

            start = max(0, position - 200)
            end = min(len(amino_acids), position + 199)
            subsequence = amino_acids[start:end]

            # terminal parts carry
            if len(subsequence) < 400:
                if start == 0:
                    end = min(len(amino_acids), 400)
                    subsequence = amino_acids[start:end]
                elif end == len(amino_acids):
                    start = max(0, len(amino_acids) - 400)
                    subsequence = amino_acids[start:end]

            # position comment
            new_position = position - start
            print(f"Here is your mutagenesis sequence: {amino_acids[position-5:position-1]}>{amino_acids[position-1]}<{amino_acids[position:position+4]}")

            # mut
            mutated_subsequence = subsequence[:199] + substitution + subsequence[200:]
            command = f'curl -X POST --data "{mutated_subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > {folder_name}/{protein_name}_{position}_{substitution}_mutated.pdb'
            os.system(command)

            # wild type
            command = f'curl -X POST --data "{subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > {folder_name}/{protein_name}_{position}.pdb'
            os.system(command)
