# FoldX-multiple-variant-assessment
Protein stability assessment of multiple variants
# FoldX Stability Analysis

This script automates the process of running FoldX `BuildModel` and `Stability` commands on a set of mutation files.

## Requirements

- Python 3
- FoldX 5

## Usage

1. Place your mutation files in the `mutated_list_path` directory. Mutation files should be text files that start with `'individual_list_'` and end with `'.txt'`.
2. Set the `pdb_file_path` variable to the path of your input PDB file.
3. Set the `mutated_pdb_path` and `stability_results_path` variables to the desired output directories for the `BuildModel` and `Stability` commands, respectively.
4. Run the script using Python 3: `python3 script.py`

The script will loop through all mutation files in the `mutated_list_path` directory and run the FoldX `BuildModel` and `Stability` commands on each file. The output of the `BuildModel` command will be saved to individual folders in the `mutated_pdb_path` directory. The output of the `Stability` command will be saved to individual folders in the `stability_results_path` directory.

In addition, the script will extract the mutation and total energy values from the output of the `Stability` command and write them to a file named `stability_report.txt` in the working directory.

## Notes

- Make sure that FoldX 5 is installed and available in your system's PATH.
- The script assumes that mutation files contain a single line with the mutation information in the format `'A_123_X'`, where `'A'` is the chain, `'123'` is the position, and `'X'` is the new residue.

## Converting One-Letter Residue Codes to Three-Letter Codes

The `end_list.py` script can be used to convert the one-letter residue codes in the `Mutation` strings of the `stability_report.txt` file to their corresponding three-letter codes.

To use the script, make sure that the `stability_report.txt` file is in the working directory and that you have defined your amino acid dictionary in the `amino_acid_dict` variable at the top of the script.

Then, run the script using Python 3: `python3 end_list.py`

The script will read the contents of the `stability_report.txt` file and extract all `Mutation` and `Total` strings. It will then split the `Mutation` strings into their components and convert the one-letter residue codes to their corresponding three-letter codes using the `amino_acid_dict` dictionary. The converted `Mutation` strings and `Total` values will be written to a new file named `total_mutations.txt`.

Example, `stability_report.txt` file contains the following lines:
###### Mutation: A_873_W 
###### Total: 201.01 
###### Mutation: A_877_V 
###### Total: 205.04

After running the script, your `total_mutations.txt` file will contain the following lines:
###### Mutation: A_873_Trp Total: 201.01 
###### Mutation: A_877_Val Total: 205.04
