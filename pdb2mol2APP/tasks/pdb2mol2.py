from flask import current_app
from celery.utils.log import get_task_logger
import time 
import os
from .. import celery

logger = get_task_logger(__name__)


@celery.task()
def pdb2mol2(pdbfile):
    time.sleep(5)
    molfile = pdbfile.replace(".pdb",".mol2")
    app= current_app._get_current_object()
    uploadpath=app.config['UPLOADED_PATH']
    # set work dir 
    pdbfile = os.path.join(uploadpath,pdbfile)
    molfile = os.path.join(uploadpath,molfile)

    command= "obabel -i pdb %s -o mol2 -O %s"%(pdbfile,molfile)
    logger.infor(command)
    os.system(command)
    return "finished"




