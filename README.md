#  Abstract "Dissecting NBAS Protein Function using AlphaFold - Structural Insights of Rare Short Stature, Optic Nerve Atrophy, and Pelger-Huet Anomaly (SOPH) Syndrome" script

## ESM fold API for multiple mutagenesis

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
