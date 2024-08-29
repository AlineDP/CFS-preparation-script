# Streamlined Script for Crystallographic Fragment Screening: Systematic Data Preparation, Phase Determination, and Initial Refinement of Multiple Datasets


**Abstract**

Crystallographic fragment screening (CFS) is a powerful approach in drug discovery, enabling the identification of small molecules that bind to protein targets and revealing the molecular mechanisms involved in these interactions. This script automates essential steps in the CFS workflow, facilitating the phase determination and refinement of crystal structures. By using modern synchrotron facilities for high-throughput data collection, this methodology can be implemented in traditional crystallography laboratories, improving the efficiency and accessibility of fragment screening campaigns.

---

**Purpose of the Script**

This Python script automates critical stages of crystallographic fragment screening (CFS), including:

1. **Data Preparation**: Preparing processed diffraction data for phase determination.
2. **Phase Determination**: Running the Phaser molecular replacement tool to identify the correct orientation and position of the protein in the crystal.
3. **Occupancy Adjustment**: Automatically adjusting ligand occupancies in the resulting structure files.
4. **Structure Refinement**: Refining the structure using the Phenix Refine tool to improve model accuracy.

This script is designed for use in large-scale CFS campaigns, where hundreds of datasets need to be processed in an automated and reproducible manner.

---

# Usage Instructions


**Prerequisites**

Before running the script, ensure the following software is installed and accessible from your command line:

- **Phenix** (including Phaser, Refine, and optionally ReadySet! for generating ligand CIF files)
- **CCP4** (to provide `uniqueify` and `cad` commands)

**Required Files**

To use this script, you must have the following files in each dataset directory:

1. **Processed MTZ File**: This file contains the diffraction data and must be named with a `.mtz` extension.
2. **input.pdb**: A PDB file that will be used as the input model for molecular replacement.
3. **input.ligands.cif**: CIF files for the ligands in the input PDB file. These can be generated using tools like ReadySet! from Phenix.

**Dataset Organization**

- Directory Structure: Each dataset should be placed in a separate directory, with the same prefix for all datasets. We recommend that the directory name starts with the name of the protein and library being tested. For example, if you are testing a library named "MyLibrary" in the protein “MyProtein”, the directories should be named as follows:

  ```
  /home/user/Fragment-screening/MyProtein-MyLibrary-01/
  /home/user/Fragment-screening/MyProtein-MyLibrary-02/
  ```
or

  ```
  /home/user/Fragment-screening/MyProtein-MyLibrary-A01/
  /home/user/Fragment-screening/MyProtein-MyLibrary-A02/
  ```
In fact, how you number or name the fragments in the library does not affect the function of the script. Just be sure to have the same prefix for all datasets.

---

# Script Customization --- NOT OPTIONAL

Before running the script, ensure the following:

1. **Base Directory**: Modify the `base_dir` variable at the end of the script **(line 152)** to point to your top-level directory containing the dataset folders:

   ```python
   base_dir = "/path/to/your/Fragment-screening"
   ```

2. **Directory Naming Convention**: Update the script to reflect the naming convention for your directories. Modify the condition in the `main` function **(line 143)** that checks for the directory name prefix:

   ```python
   if os.path.isdir(subdir_path) and subdir.startswith("MyProtein-MyLibrary-"):
   ```
Change the subdir.startswith("**MyProtein-MyLibrary-**") for your directories prefix.


3. **Output File Handling**: The script generates output files (`output-uniqueify.mtz`, `output-cad.mtz`, `PHASER.1.*`, etc.) in each dataset directory. Ensure these names do not conflict with existing files in your directory.

---

# Running the Script

To execute the script:

1. Ensure All Dependencies Are Met: Verify that Phenix and CCP4 tools are installed and accessible.
2. Customize the Script: Update the `base_dir` variable and ensure your dataset files are correctly named and placed. Also, ensure the directory naming matches your library name.
3. Prepare Ligand CIF Files: Ensure that CIF files for the ligands in your PDB files are generated and placed in the respective directories. You can generate these using tools like ReadySet! from Phenix.
4. Run the Script: Execute the script from the command line:

   ```bash
   python3 CFS_preparation_script.py
   ```

---

# Expected Output

After running the script, each dataset directory will contain:

- **Processed MTZ and PDB Files**: Files ready for downstream analysis or further refinement.
- **PHASER.pdb**, **PHASER.mtz**: Generated after successful phase determination.
- **PHASER.phenix_refine_001.pdb**, **PHASER.phenix_refine_001.mtz**: Refined structure files after running Phenix Refine.

These files represent the key outputs from molecular replacement and subsequent refinement, ready for ligand identification through PanDDA!

---

# Conclusion

This script provides a streamlined and automated approach to processing large datasets in crystallographic fragment screening campaigns. By reducing the manual workload associated with each dataset, it allows the preparation of datasets for the ligand identification from large CFS campaigns.
