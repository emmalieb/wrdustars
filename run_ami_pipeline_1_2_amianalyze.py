#!/usr/bin/env python

import os
import sys
import glob
import time
import argparse
import json
from datetime import datetime

import numpy as np
from astropy.io import fits
from astropy import units as u

from jwst.pipeline import Detector1Pipeline, Image2Pipeline
from jwst.ami import AmiAnalyzeStep
from jwst.ami import AmiNormalizeStep
from jwst import datamodels



def run_pipeline_wbadpix(odir=None):
    """
    This script runs JWST pipeline on JWST NIRISS Aperture Masking Interferometry(AMI) data from ERS program 1349

    Steps:

    [1] Run Detector1 pipeline on all _uncal.fits files to create _rate.fits and _rateints.fits files.

    [2] Run Image2 pipeline on all _rate.fits files to create _cal.fits and on _rateints.fits files to
       create _calints.fits files.

    [3]Run AmiAnalyzeStep of the AMI3 pipeline to reduce data calibrated by Detector1 and Image2 pipelines to interferometric observables, extract observables in oifits format.

    To call
    python run_ami_pipeline_1.py <with optional odir name>

    Parameters
    ----------

    input
         indir: help="Directory containing uncal.fits files
         odir (optional): Directory to save pipeline-calibrated data
    Returns
         calibrated data (rate, rateints, cal, calints, ramp files)
    """
    
    start = time.time()
    currentdir = os.getcwd()

    # On orbit data epoch 1
    # Only using observations 005 and 006. Observation 003 was affected by mirror tilt event and observation 004 failed to execute.
    uncal_dir_epoch1 = os.path.join(currentdir, 'uncal_data_july13_15/')
    # On orbit data epoch 2
    uncal_dir_epoch2 = os.path.join(currentdir, 'uncal_data_august8/')

    uncalfiles_epoch1 = sorted(glob.glob(os.path.join(uncal_dir_epoch1,'jw*uncal.fits')))
    uncalfiles_epoch2 = sorted(glob.glob(os.path.join(uncal_dir_epoch2,'jw*uncal.fits')))

    uncalfiles = uncalfiles_epoch1 + uncalfiles_epoch2
    #uncalfiles = [os.path.basename(i) for i in uncalfiles]
    print("\n".join(uncalfiles))


    # Define output directory to save pipeline output products
    if odir is None:
        odir = './pipeline_calibrated_data_epoch1_2/'
    if not os.path.exists(odir):
        os.makedirs(odir)
    print("Output directory for pipeline products:", odir)
    
    # for later use in __main__
    run_pipeline_wbadpix.outdir = odir

    #Uncomment when running the pipeline from outside STScI. See https://jwst-pipeline.readthedocs.io/en/latest/jwst/user_documentation/reference_files_crds.html
    #os.environ['CRDS_PATH'] = '$HOME/crds_cache'    
    #os.environ['CRDS_SERVER_URL'] = 'https://jwst-crds.stsci.edu'
 

    # Run Detector1 and Image2 pipelines
    for df in uncalfiles_epoch1:
        # Set charge migration signal threshold 
        cm_th = 16227 #ADU
        result1 = Detector1Pipeline()
        result1.ipc.skip = True
        # skipping the charge migration step since it was not implemented at the time of writing the paper
        result1.charge_migration.skip = True
        # cm_th will be used when charge_migration.skip = False
        result1.charge_migration.signal_threshold = cm_th
        print("using CM threshold", cm_th, "ADU")
        # Uncomment to skip dark subtraction
        # Not skipping the dark_current step since it was not skipped at the time of writing the paper
        # result1.dark_current.skip = True
        result1.save_results = True
        result1.save_calibrated_ramp = True
        result1.output_dir = odir
        result1.run(df)

        df_rate = os.path.join(odir, os.path.basename(df.replace('uncal', 'rate')))
        result2 = Image2Pipeline()
        result2.photom.skip = True
        result2.resample.skip = True
        result2.save_results = True
        result2.output_dir = odir
        result2.run(df_rate)

        df_cal = os.path.join(odir, os.path.basename(df.replace('uncal','cal')))
        print("Generated calibrated 2D files", df_cal)

        df_rateints = os.path.join(odir, os.path.basename(df.replace('uncal', 'rateints')))
        result3 = Image2Pipeline()
        result3.photom.skip = True
        result3.resample.skip = True
        result3.save_results = True
        result3.output_dir = odir
        result3.run(df_rateints)

        df_calints = os.path.join(odir, os.path.basename(df.replace('uncal','calints')))
        print("Generated calibrated 3D files", df_calints)


        analyze = AmiAnalyzeStep()
        analyze.save_results = True
        analyze.firstfew = None
        analyze.output_dir = odir
        analyze.usebp = False 
        analyze.oversample = 5
        analyze.run_bpfix = True
        output_model, outputmodelmulti, lgmodel = analyze.run(df_calints)

    end = time.time()
    print("RUNTIME: %.2f s" % (end - start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the JWST pipeline to calibrate real or simulated data containing bad pixels")
    parser.add_argument("--odir", help="Directory to save pipeline-calibrated data to", default=None)
    args = parser.parse_args()
    run_pipeline_wbadpix(odir=args.odir)

