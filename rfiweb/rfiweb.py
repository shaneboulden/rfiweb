# This is the RFI web front-end.

from flask import Flask, render_template, flash, redirect, request
from requests.auth import HTTPBasicAuth

import requests
import json
import os

application = Flask(__name__)
application.secret_key = os.environ['FLASK_SECRET']
pam_uri = os.environ['RHPAM_URI']
pam_user = os.environ['RHPAM_USER']
pam_pass = os.environ['RHPAM_PASS']

@application.route('/healthz')
def healthz():
    """
    Check the health of this rfiweb instance. OCP will hit this endpoint to verify the readiness
    of the rfiweb pod.
    """
    return 'OK'

@application.route('/')
def index():
    return render_template('index.html')

# the keycloak authenticator requires that all routes support GET and 
# POST methods
@application.route('/rfisByStatus', methods=["GET","POST"])
def rfis_by_status():
    # a variable to concatenate json strings
    json_arr = []
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    # get all instances in the RFI system
    resp=requests.get(pam_uri+'/services/rest/server/queries/processes/instances/variables/v_priority', auth=HTTPBasicAuth(pam_user,pam_pass), headers=headers).json()
    instances = resp['process-instance']
    for instance in instances:
        resp1 = requests.get(pam_uri+'/services/rest/server/containers/RCM2_1.0.2/processes/instances/'+str(instance['process-instance-id'])+'/variables',auth=HTTPBasicAuth(pam_user,pam_pass),headers=headers).json()
        json_arr.append(resp1)
    return render_template('rfis_by_status.html', rfis=json_arr)


@application.route('/rfis', methods=['GET','POST'])
def rfis():
    # a variable to concatenate json strings
    json_arr = []
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    # get all instances in the RFI system
    resp=requests.get(pam_uri+'/services/rest/server/queries/processes/instances/variables/v_priority', auth=HTTPBasicAuth(pam_user,pam_pass), headers=headers).json()
    instances = resp['process-instance']
    for instance in instances:
        resp1 = requests.get(pam_uri+'/services/rest/server/containers/RCM2_1.0.2/processes/instances/'+str(instance['process-instance-id'])+'/variables',auth=HTTPBasicAuth(pam_user,pam_pass),headers=headers).json()
        json_arr.append(resp1)
    return render_template('rfis.html', rfis=json_arr)
