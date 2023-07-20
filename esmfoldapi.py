import os
from datetime import datetime
import Bio.PDB

while True:
    protein_name = input("Enter protein name (or 'q' to quit): ")
    if protein_name == 'q':
        break
    amino_acids = input("Enter whole amino acid sequence: ")
    while True:
        # timestamp = datetime.now().strftime("%H-%M-%S")
        folder_date = datetime.now().strftime("%m-%d-%Y")
        folder_name = f"{protein_name}_{folder_date}"
        os.makedirs(f'proteins_esm/{folder_name}', exist_ok=True)

        # separation
        position_input = input("Enter position and variant like this - '254D,1914H and so on' (or 'n' for new protein): ")
        if position_input == 'n':
            break
        aa_numbers = []
        aa_change = []

        for item in position_input.split(','):
            aa_numbers.append(int(''.join(filter(str.isdigit, item))))
            aa_change.append(''.join(filter(str.isalpha, item)))

        for i in range(len(aa_numbers)):

            # cycle
            position = int(aa_numbers[i])
            substitution = str(aa_change[i])
            with open(f"RMSD/{protein_name}_rmsd.txt", "a") as f:
                f.write(f"{position}_{substitution}:\n")
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

            if start == 0:
                new_position = position
            elif end == len(amino_acids):
                new_position = position - (len(amino_acids) - 400)

            print(f"Here is your mutagenesis sequence: {amino_acids[position-5:position-1]}>{amino_acids[position-1]}<{amino_acids[position:position+4]}")

            # mut
            mutated_subsequence = subsequence[:new_position-1] + substitution + subsequence[new_position:]
            command = f'curl -X POST --data "{mutated_subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > proteins_esm/{folder_name}/{protein_name}_{position}_{substitution}_mutated.pdb'
            os.system(command)

            # wild type
            command = f'curl -X POST --data "{subsequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > proteins_esm/{folder_name}/{protein_name}_{position}.pdb'
            os.system(command)

            # RMSD part
            # Select what residues numbers you wish to align
            # and put them in a list
            rmsd_start_cut = [0, 50, 100, 150, 200, 250, 300]
            rmsd_end_cut = [100, 150, 200, 250, 300, 350, 400]
            for j in range(len(rmsd_start_cut)):
                start_id = rmsd_start_cut[j]
                end_id = rmsd_end_cut[j]
                atoms_to_be_aligned = range(start_id, end_id + 1)

                # Start the parser
                pdb_parser = Bio.PDB.PDBParser(QUIET=True)

                # Get the structures
                ref_structure = pdb_parser.get_structure("reference", f"proteins_esm/{folder_name}/{protein_name}_{position}.pdb")
                sample_structure = pdb_parser.get_structure("sample", f"proteins_esm/{folder_name}/{protein_name}_{position}_{substitution}_mutated.pdb")

                # Use the first model in the pdb-files for alignment
                # Change the number 0 if you want to align to another structure
                ref_model = ref_structure[0]
                sample_model = sample_structure[0]

                # Make a list of the atoms (in the structures) you wish to align.
                # In this case we use CA atoms whose index is in the specified range
                ref_atoms = []
                sample_atoms = []

                # Iterate of all chains in the model in order to find all residues
                for ref_chain in ref_model:
                    # Iterate of all residues in each model in order to find proper atoms
                    for ref_res in ref_chain:
                        # Check if residue number ( .get_id() ) is in the list
                        if ref_res.get_id()[1] in atoms_to_be_aligned:
                            # Append CA atom to list
                            ref_atoms.append(ref_res['CA'])

                # Do the same for the sample structure
                for sample_chain in sample_model:
                    for sample_res in sample_chain:
                        if sample_res.get_id()[1] in atoms_to_be_aligned:
                            sample_atoms.append(sample_res['CA'])

                # Now we initiate the superimposer:
                super_imposer = Bio.PDB.Superimposer()
                super_imposer.set_atoms(ref_atoms, sample_atoms)
                super_imposer.apply(sample_model.get_atoms())

                # Print RMSD:
                rmsd = super_imposer.rms

                def save_rmsd_to_file(rmsd_s, protein_name_s, position_s, start_id_s, end_id_s):
                    start_position = position_s + start_id_s - 200
                    end_position = position_s + end_id_s - 200
                    with open(f"RMSD/{protein_name_s}_rmsd_log.txt", "a") as f:
                        f.write(f"RMSD of {protein_name} at position {start_position}-{end_position} {rmsd_s}\n")


                save_rmsd_to_file(rmsd, protein_name, position, start_id, end_id)
        #
        with open(f"RMSD/{protein_name}_rmsd_log.txt", "a") as f:
            f.write(f"\n\n")
            # Save the aligned version of 1UBQ.pdb
            # io = Bio.PDB.PDBIO()
            # io.set_structure(sample_structure)
            # io.save("NBAS_07-17-2023/NBAS_1914_aligned.pdb")
