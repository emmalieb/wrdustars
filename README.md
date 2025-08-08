# WRDustERS Repository

This branch consists of the following: 

- dustERS_ami_pipeline_epoch1_2_ami3.ipynb: Notebook to run JWST pipeline on Aperture Masking Interferometry(AMI) data of WR137 and calibrator HD228337 observed on August 8, 2022.
- oifits.zip: raw JWST+NIRISS fits files.
- requirements_dusters.txt: all necessary packages to install prior to running dustERS_ami_pipeline_epoch1_2_ami3.ipynb.
- run_ami_pipeline_1_2_amianalyze.py: Script to run JWST pipeline on JWST NIRISS Aperture Masking Interferometry(AMI) data from ERS program 1349.
- run_aminormalize.py: script to run ami_normalize step of the AMI3 pipeline on the raw oifits files to calibrate target observables with calibrator observables.
