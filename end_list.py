import re

# Define your amino acid dictionary here
amino_acid_dict = {
    'A': 'Ala',
    'C': 'Cys',
    'D': 'Asp',
    'E': 'Glu',
    'F': 'Phe',
    'G': 'Gly',
    'H': 'His',
    'I': 'Ile',
    'K': 'Lys',
    'L': 'Leu',
    'M': 'Met',
    'N': 'Asn',
    'P': 'Pro',
    'Q': 'Gln',
    'R': 'Arg',
    'S': 'Ser',
    'T': 'Thr',
    'V': 'Val',
    'W': 'Trp',
    'Y': 'Tyr'
}

# Open the text file for reading
with open('stability_report_done.txt', 'r') as f:
    # Read the contents of the file
    contents = f.read()

    # Use regular expressions to find all Mutation and Total strings
    mutation_matches = re.findall(r'Mutation: (.+)', contents)
    total_matches = re.findall(r'Total\s+=\s+([\d.-]+)', contents)

    # Open the total_mutations.txt file for writing
    with open('total_mutations.txt', 'w') as f:
        # Loop through all Mutation and Total matches
        for mutation, total in zip(mutation_matches, total_matches):
            # Split the mutation string into its components
            chain, position, residue = mutation.split('_')

            # Convert the one-letter residue code to its three-letter code using the amino acid dictionary
            residue = amino_acid_dict[residue]

            # Write the converted mutation string and Total value to the file
            f.write(f'Mutation: {chain}_{position}_{residue} Total: {total}\n')