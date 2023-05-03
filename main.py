import os
import subprocess
import re

mutated_list_path = 'mutated_list/'

pdb_file_path = 'NBAS_wt_Repair.pdb'

mutated_pdb_path = 'mutated_proteins/'

stability_results_path = 'stability_results/'

i = 1
with open('stability_report.txt', 'w') as stability_report:
    for filename in os.listdir(mutated_list_path):
        if filename.startswith('individual_list_') and filename.endswith('.txt'):
            mutation_file_path = os.path.join(mutated_list_path, filename)

            with open(mutation_file_path, 'r') as f:
                lines = f.readlines()
                mutation_info = lines[0].strip()
                chain = mutation_info[1]
                position = re.search(r'\d+', mutation_info).group()
                new_residue = mutation_info[-2]
                mutation = f'{chain}_{position}_{new_residue}'

            build_model_output_dir = os.path.join(mutated_pdb_path, f'build_model_{i}')
            os.makedirs(build_model_output_dir, exist_ok=True)

            subprocess.run(['foldx_5', '--command=BuildModel', f'--pdb={pdb_file_path}', f'--mutant-file={mutation_file_path}',
                            '--out-pdb=on', f'--output-dir={build_model_output_dir}'])

            pdb_filename = os.path.basename(pdb_file_path)
            pdb_name, pdb_ext = os.path.splitext(pdb_filename)

            mutation_stability_results_path = os.path.join(stability_results_path, f'{mutation}_{i}')
            os.makedirs(mutation_stability_results_path, exist_ok=True)

            stability_output = subprocess.check_output(['foldx_5', '--command=Stability',
                                                        f'--pdb={pdb_name}_1{pdb_ext}',
                                                        f'--pdb-dir={build_model_output_dir}',
                                                        f'--output-dir={mutation_stability_results_path}'])

            stability_report.write(f'Mutation: {mutation}\n')
            stability_report.write(stability_output.decode('utf-8'))

            i += 1
