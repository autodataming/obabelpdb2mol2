#!python2
# coding: utf-8
import os 
from flask import Flask



import os
import time 
from flask import render_template
from flask import request

from flask import url_for
from flask import jsonify
from celery.utils.log import get_task_logger
from celery import Celery
from celery.result import AsyncResult
from flask import send_file, send_from_directory
import uuid



logger = get_task_logger(__name__)


# from celery_tasks import tasks 
# from celery_tasks.celery import celery


app = Flask(__name__)

app.config['UPLOADED_PATH'] = os.path.join(os.getcwd(),'upload')
print ("upload path",app.config['UPLOADED_PATH'])

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/3',
    CELERY_RESULT_BACKEND='redis://localhost:6379/3'
)



celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL']
)
celery.conf.update(app.config)


@celery.task
def add(x,y):
    return x+y 

@celery.task
def plus(x,y):
    return x+y 
    
@celery.task
def pdb2mol2(pdbfile):
    time.sleep(5)
    molfile = pdbfile.replace(".pdb",".mol2")
    uploadpath=app.config['UPLOADED_PATH']
    # set work dir 
    pdbfile = os.path.join(uploadpath,pdbfile)
    fnn = molfile
    molfile = os.path.join(uploadpath,molfile)
    command= "obabel -i pdb %s -o mol2 -O %s"%(pdbfile,molfile)
    logger.info(command)
    print("command:%s"%command)
    os.system(command)

    # dict
    return { 'status': 'Finished!',
            'mol2file222': molfile,
            'filename':fnn}




@app.route('/')
def index():
    return render_template('index.htm')
    # return 'Hello World!'



@app.route('/handleupload', methods=['POST'])
def handleupload():
    '''
    '''
    if request.method == 'POST':
        print ("upload files")
        for f in request.files.getlist('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))    
            # 开始计算作业
            print("ready to perform task in the background")

    # 为该文件创造一个ID，用于控制  
    return render_template('index.htm')
    
@app.route('/longtask')
def longtask():
    '''
    '''
    id = request.args.get("id")
    pdbfile= request.args.get("pdbfile")
    # # print "pdbfile",pdbfile
    task2 = pdb2mol2.delay(pdbfile)
    # mol2file= task2.mol2file
    # task = add.delay(1,3)
    # task.wait()
    # print(task.backend)
    # print dir(task)

    # print task.id
    # print task.result
    # print task2.id 
    return jsonify({'taskid': task2.id,'id':id})
    # return jsonify({}), 202, {'Location': url_for('taskstatus',
    #                                               task_id=task.id)}


from pprint import  pprint
@app.route('/status/<taskid>')
def state(taskid):
    id = request.args.get("id")
    task = AsyncResult(taskid,app=celery)
    print("task result:")
    pprint(task.result)
    #'mol2file':task.result['mol2file'] 

    if task.result:
        # print type(task.result)
        # print dir(task.result)
        # print task.result.keys()
        downlink = task.result['filename']
    else:
        downlink ="none"
        
    return jsonify({'status': task.status,'downlink':downlink,'id':id })
    # return jsonify({}), 202, {'Location': url_for('taskstatus',
    #                                               task_id=task.id)}

    

@app.route('/download/<mol2file>')
def download(mol2file):
    '''
    '''
    directory=app.config['UPLOADED_PATH']
    filename=mol2file
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/zip')
def zip():
    molfiles=request.args.getlist('molfile')
    #7z -tZip a test.zip 1.mol2 2.mol2
    zipfile='mol2_%s.zip'%uuid.uuid4()
    if molfiles:
        target=os.path.join(app.config['UPLOADED_PATH'],zipfile)

        command="7z a -tZip  %s "%target+' '.join( map(lambda i:os.path.join(app.config['UPLOADED_PATH'],i)   ,molfiles))
        print(command)
        os.system(command)
        return jsonify({'type':'7zip','zipfile':zipfile})
    else:
        print "no molfiles",molfiles
        return jsonify({'type':'7zip','zipfile':"none.zip"})
        
        


@app.route('/downloadall/<zipfile>')
def downloadall(zipfile):
    '''
    '''
    directory=app.config['UPLOADED_PATH']
    filename=zipfile
    return send_from_directory(directory, filename, as_attachment=True)

    


@app.route('/test')
def test():

    return "hello test"
    # return jsonify({}), 202, {'Location': url_for('taskstatus',
    #                                               task_id=task.id)}


# if __name__ =='__main__':
#     app.run()

