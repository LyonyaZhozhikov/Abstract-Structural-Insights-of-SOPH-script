#  Article "Computational genotype-protein-phenotype study of SOPH syndrome" (tools)

## 1. FoldX Stability Analysis of multiple variants

This script automates the process of running FoldX `BuildModel` and `Stability` commands on a set of mutation files.

### Requirements

- Python 3
- FoldX 5

### Usage

1. Place your mutation files in the `mutated_list_path` directory. Mutation files should be text files that start with `'individual_list_'` and end with `'.txt'`.
2. Set the `pdb_file_path` variable to the path of your input PDB file.
3. Set the `mutated_pdb_path` and `stability_results_path` variables to the desired output directories for the `BuildModel` and `Stability` commands, respectively.
4. Run the script using Python 3: `python3 script.py`

The script will loop through all mutation files in the `mutated_list_path` directory and run the FoldX `BuildModel` and `Stability` commands on each file. The output of the `BuildModel` command will be saved to individual folders in the `mutated_pdb_path` directory. The output of the `Stability` command will be saved to individual folders in the `stability_results_path` directory.

In addition, the script will extract the mutation and total energy values from the output of the `Stability` command and write them to a file named `stability_report.txt` in the working directory.

### Notes

- Make sure that FoldX 5 is installed and available in your system's PATH.
- The script assumes that mutation files contain a single line with the mutation information in the format `'A_123_X'`, where `'A'` is the chain, `'123'` is the position, and `'X'` is the new residue.

### Converting One-Letter Residue Codes to Three-Letter Codes

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

## 2. ESM fold API for multiple mutagenesis

This script takes a whole protein sequence as input, prompts the user to enter a position in the sequence to be analyzed, cuts the sequence to a 400 amino acid long protein with the specified position in the middle, and sends the resulting subsequence using a curl API command. 

The script can be run in two modes: `normal` and `mutagenesis`. 
In normal mode, the script behaves exactly as described. 
In mutagenesis mode, the script additionally prompts the user to enter a substituted amino acid after the position to analyze, and sends two API requests: one with the original cut sequence and another with the substituted amino acid.

### Usage

1. To use this script, you need to have `Python` installed on your computer. 
2. Open a `terminal` or command prompt and navigate to the directory where you saved the script. 
3. Run the script by typing `python3 esmfoldapi.py`. 
4. The script will prompt you to enter the mode `(normal or mut)`, protein name, and amino acid sequence. 
5. After entering this information, it will prompt you to enter a position in the sequence to analyze. If in mutagenesis mode, it will also prompt you to enter a substituted amino acid. 
6. The script will then cut the sequence to a 400 amino acid long protein with the specified position in the middle, create a folder named with the current date and time, execute a curl command with the original or mutated subsequence (depending on mode), and save the output to a file named with the protein name, position, timestamp, and mode inside the created folder.

### Notes

Not sensitive to positions +- 200 aa from N and C terminal of the protein sequences.

ESM fold have limit of max 400 aa long sequences.
