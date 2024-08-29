import os
import subprocess

# Function to run uniqueify on the dataset
def run_uniqueify(directory):
    mtz_file = os.path.join('*.mtz')
    uniqueify_output = os.path.join('output-uniqueify.mtz')
    uniqueify_command = f"uniqueify -s {mtz_file} {uniqueify_output}"
    print(f"Running uniqueify in {directory} with command:{uniqueify_command}")
    try:
        subprocess.run(uniqueify_command, shell=True, check=True, cwd=directory)
        print(f"Successfully ran uniqueify in {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error running uniqueify in {directory}: {e}")

# Function to run cad on the uniqueified dataset
def run_cad(directory):
    uniqueify_output = os.path.join('output-uniqueify.mtz')
    cad_output = os.path.join('output-cad.mtz')
    cad_command = (
        f"cad hklin1 {uniqueify_output} hklout {cad_output} <<eof\n"
        "monitor BRIEF\n"
        "labin file 1 E1=I(+) E2=SIGI(+) E3=I(-) E4=SIGI(-) E5=FreeRflag\n"
        "resolution file 1 999.0 1\n"
        "eof"
    )
    print(f"Running cad in {directory} with command:\n{cad_command}")
    try:
        subprocess.run(cad_command, shell=True, check=True, cwd=directory)
        print(f"Successfully ran cad in {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error running cad in {directory}: {e}")

# Function to run Phenix Phaser
def run_phaser(directory):
    mtz_file = os.path.join('output-cad.mtz')
    pdb_file = os.path.join('input.pdb')
    output_prefix = os.path.join('PHASER')
    phaser_command = f"phenix.phaser hklin {mtz_file} model {pdb_file} phaser.mode=MR_AUTO output.prefix={output_prefix} output.dir={directory}"
    print(f"Running phenix.phaser in {directory} with command:\n{phaser_command}")
    try:
        subprocess.run(phaser_command, shell=True, check=True, cwd=directory)
        print(f"Successfully ran phenix.phaser in {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error running phenix.phaser in {directory}: {e}")

# Function to change the occupancy of ligands in the PHASER.1.pdb file
def change_occupancy(directory):
    pdb_file = os.path.join(directory, 'PHASER.pdb')
    
    # Wait until the PHASER.1.pdb file is generated
    wait_for_file(pdb_file)
    
    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as file:
            lines = file.readlines()
        
        with open(pdb_file, 'w') as file:
            for line in lines:
                if line.startswith("HETATM"):
                    # Replace only if '0.00' is within columns 56-62
                    if "0.00" in line[55:62]:
                        line = line.replace("0.00", "0.50")
                file.write(line)
        
        print(f"Modified: {pdb_file}")
    else:
        print(f"File not found: {pdb_file}")

# Function to run phenix.refine
def run_phenix_refine(directory):
    mtz_file = os.path.join(directory, 'PHASER.mtz')
    pdb_file = os.path.join(directory, 'PHASER.pdb')
    cif_file = os.path.join(directory, 'input.ligands.cif')
    
    # Wait until the necessary files are generated
    wait_for_file(mtz_file)
    wait_for_file(pdb_file)
    wait_for_file(cif_file)
    
    if os.path.exists(mtz_file) and os.path.exists(pdb_file) and os.path.exists(cif_file):
        refine_command = [
            'phenix.refine', mtz_file, pdb_file, cif_file,
            'xray_data.low_resolution=75',
            'xray_data.r_free_flags.generate=True',
            'xray_data.r_free_flags.fraction=0.05',
            'xray_data.r_free_flags.max_free=500',
            'refinement.refine.occupancies.individual="element C or element O or element N or element S or element P"',
            f'output.prefix={os.path.join(directory, "PHASER.phenix_refine")}'
        ]

        try:
            subprocess.run(refine_command, check=True)
            print(f"Successfully ran phenix.refine in {directory}")
        except subprocess.CalledProcessError as e:
            print(f"Error running phenix.refine in {directory}. See log for details.")
            print(e)
    else:
        print(f"Missing necessary files in {directory}")

# Function to change the occupancy of ligands in the PHASER.1.phenix_refine_001.pdb file
def change_occupancy_refine(directory):
    pdb_file = os.path.join(directory, 'PHASER.phenix_refine_001.pdb')
    
    # Wait until the PHASER.1.phenix_refine_001.pdb file is generated
    wait_for_file(pdb_file)
    
    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as file:
            lines = file.readlines()
        
        with open(pdb_file, 'w') as file:
            for line in lines:
                if line.startswith("HETATM") or line.startswith("ATOM"):
                    # Replace only if '0.00' is within columns 56-62
                    if "0.00" in line[55:62]:
                        line = line.replace("0.00", "0.01")
                file.write(line)
        
        print(f"Modified: {pdb_file}")
    else:
        print(f"File not found: {pdb_file}")

# Function to wait until a file is generated
def wait_for_file(filepath, timeout=300, check_interval=5):
    """
    Wait for a file to be generated.
    :param filepath: Path to the file to wait for.
    :param timeout: Maximum time to wait in seconds. Default is 300 seconds.
    :param check_interval: Time interval between checks in seconds. Default is 5 seconds.
    """
    total_time = 0
    while not os.path.exists(filepath) and total_time < timeout:
        time.sleep(check_interval)
        total_time += check_interval
    if not os.path.exists(filepath):
        print(f"Warning: File not found after waiting: {filepath}")

# Main function to run all steps in each dataset
def main(base_dir):
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path) and subdir.startswith("MyProtein-MyLibrary-"):
            run_uniqueify(subdir_path)
            run_cad(subdir_path)
            run_phaser(subdir_path)
            change_occupancy(subdir_path)
            run_phenix_refine(subdir_path)
            change_occupancy_refine(subdir_path)

if __name__ == "__main__":
    base_dir = "/home/user/Fragment-screening/"
    main(base_dir)
