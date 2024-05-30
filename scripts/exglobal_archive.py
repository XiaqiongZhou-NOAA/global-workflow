#!/usr/bin/env python3

import os

from pygfs.task.archive import Archive
from wxflow import AttrDict, Logger, cast_strdict_as_dtypedict, chdir, logit

# initialize root logger
logger = Logger(level=os.environ.get("LOGGING_LEVEL", "DEBUG"), colored_log=True)


@logit(logger)
def main():

    config = cast_strdict_as_dtypedict(os.environ)

    # Instantiate the Archive object
    archive = Archive(config)

    # Pull out all the configuration keys needed to run the rest of archive steps
    keys = ['ATARDIR', 'current_cycle', 'FHMIN', 'FHMAX', 'FHOUT', 'RUN', 'PDY',
            'DO_VERFRAD', 'DO_VMINMON', 'DO_VERFOZN', 'DO_ICE', 'DO_AERO', 'PARMgfs',
            'DO_OCN', 'DO_WAVE', 'WRITE_DOPOST', 'PSLOT', 'HPSSARCH', 'DO_MOS',
            'DO_JEDISNOWDA', 'LOCALARCH', 'REALTIME', 'ROTDIR', 'ARCH_WARMICFREQ',
            'ARCH_FCSTICFREQ', 'ARCH_CYC', 'assim_freq', 'ARCDIR', 'SDATE',
            'FHMIN_GFS', 'FHMAX_GFS', 'FHOUT_GFS', 'ARCH_GAUSSIAN', 'MODE',
            'FHOUT_OCNICE', 'FHOUT_OCNICE_GFS', 'DO_BUFRSND', 'DOHYBVAR',
            'ARCH_GAUSSIAN_FHMAX', 'ARCH_GAUSSIAN_FHINC', 'ARCH_GAUSSIAN_FHINC',
            'DOIAU', 'OCNRES', 'ICERES', 'NUM_SND_COLLECTIVES', 'FHOUT_WAV',
            'FHOUT_HF_WAV', 'FHMAX_WAV', 'FHMAX_HF_WAV', 'FHMAX_WAV_GFS',
            'restart_interval_gdas', 'restart_interval_gfs',
            'AERO_ANL_CDUMP', 'AERO_FCST_CDUMP', 'DOIBP_WAV', 'DO_JEDIOCNVAR',
            'NMEM_ENS', 'DO_JEDIATMVAR', 'DO_VRFY_OCEANDA', 'FHMAX_FITS',
            'FITSARC', 'IAUFHRS']

    archive_dict = AttrDict()
    for key in keys:
        archive_dict[key] = archive.task_config[key]

    # Also import all COM* directory and template variables
    for key in archive.task_config.keys():
        if key.startswith("COM"):
            archive_dict[key] = archive.task_config[key]

    cwd = os.getcwd()

    os.chdir(config.ROTDIR)

    # Determine which archives to create
    arcdir_set, atardir_sets = archive.configure(archive_dict)

    # Populate the product archive (ARCDIR)
    archive.execute_store_products(arcdir_set)

    # Create the backup tarballs and store in ATARDIR
    for atardir_set in atardir_sets:
        archive.execute_backup_dataset(atardir_set)

    os.chdir(cwd)


if __name__ == '__main__':
    main()