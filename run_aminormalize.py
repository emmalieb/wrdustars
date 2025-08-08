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

odir = './pipeline_calibrated_data_epoch1_2/'

# Run ami_normalize step of the AMI3 pipeline on the raw oifits files to calibrate target observables with calibrator observables

def normalize_oifits(targ_oi,cal_oi,calib_oi):
    """
    calibrate closure phases and square visibilities of target with those of the calibrator."

    Parameters
    ----------
    input
        targ_oi: target oifits file
        cal_oi: calibrator oifits file
        calib_oi: name of calibrated (normalized) oifits file

    Returns:
        calibrated oifits file
    -------
    """
    normalize = AmiNormalizeStep()
    normalize.output_dir = odir
    normalize.output_file = calib_oi
    normalize.save_results = True
    normmodel = normalize.run(targ_oi,cal_oi) # target oifits file, calibrator oifits file


if __name__ == "__main__":

    # WR137 and calibrator HD228337 oifits files from epoch 1 and epoch 2
    oifits_targ_ep1 = sorted(glob.glob(os.path.join(odir, 'jw01349006*nis_ami-oi.fits')))
    oifits_targ_ep2 = sorted(glob.glob(os.path.join(odir, 'jw01349053*nis_ami-oi.fits')))
    oifits_calibrator_ep1 = sorted(glob.glob(os.path.join(odir, 'jw01349005*nis_ami-oi.fits')))
    oifits_calibrator_ep2 = sorted(glob.glob(os.path.join(odir, 'jw01349054*nis_ami-oi.fits')))

    oifits_targ = oifits_targ_ep1 + oifits_targ_ep2
    oifits_calibrator = oifits_calibrator_ep1 + oifits_calibrator_ep2

    # Construct output file names for calibrated oifits files
    calib_oifiles_rootname = [os.path.basename(oifits_targ[0].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[0].replace('_ami-oi.fits','')),
                 os.path.basename(oifits_targ[1].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[1].replace('_ami-oi.fits','')),
                 os.path.basename(oifits_targ[2].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[2].replace('_ami-oi.fits','')),
                 os.path.basename(oifits_targ[3].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[3].replace('_ami-oi.fits','')),
       	       	 os.path.basename(oifits_targ[4].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[4].replace('_ami-oi.fits','')),
       	       	 os.path.basename(oifits_targ[5].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[5].replace('_ami-oi.fits','')),
       	       	 os.path.basename(oifits_targ[6].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[6].replace('_ami-oi.fits','')),
       	       	 os.path.basename(oifits_targ[7].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[7].replace('_ami-oi.fits','')),
                 os.path.basename(oifits_targ[8].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[8].replace('_ami-oi.fits','')),
                 os.path.basename(oifits_targ[9].replace('_ami-oi.fits',''))+'_norm_'+os.path.basename(oifits_calibrator[9].replace('_ami-oi.fits','')),
                ]
    # Calibrate target observables with calibrator observables
    # calibrate observation 006 exposures with observation 005 exposures, calibrate observation 053 with observation 054 exposures
    # with the same dither and filter combination.
    normalize_oifits(oifits_targ[0], oifits_calibrator[0],calib_oifiles_rootname[0])
    normalize_oifits(oifits_targ[1], oifits_calibrator[1],calib_oifiles_rootname[1])
    normalize_oifits(oifits_targ[2], oifits_calibrator[2],calib_oifiles_rootname[2])
    normalize_oifits(oifits_targ[3], oifits_calibrator[3],calib_oifiles_rootname[3])
    normalize_oifits(oifits_targ[4], oifits_calibrator[4],calib_oifiles_rootname[4])
    normalize_oifits(oifits_targ[5], oifits_calibrator[5],calib_oifiles_rootname[5])
    normalize_oifits(oifits_targ[6], oifits_calibrator[6],calib_oifiles_rootname[6])
    normalize_oifits(oifits_targ[7], oifits_calibrator[7],calib_oifiles_rootname[7])
    normalize_oifits(oifits_targ[8], oifits_calibrator[6],calib_oifiles_rootname[8])
    normalize_oifits(oifits_targ[9], oifits_calibrator[7],calib_oifiles_rootname[9])

    print("Output of AmiNormalizeStep: Calibrated observables of target WR137")
    calib_oifiles = sorted(glob.glob(os.path.join(odir,'jw*nis_aminorm-oi.fits')))
    print('\n'.join(calib_oifiles))
