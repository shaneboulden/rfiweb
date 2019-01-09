# This is the RFI web front-end.

from flask import Flask, render_template, flash, redirect, request
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

import requests
import json
import os
import logging

application = Flask(__name__)
application.secret_key = os.environ['FLASK_SECRET']
pam_uri = os.environ['RHPAM_URI']
pam_user = os.environ['RHPAM_USER']
pam_pass = os.environ['RHPAM_PASS']
container_id = os.environ['CONTAINER_ID']

class PamContainerException(Exception):
    pass

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
    return kie_response('rfis_by_status.html') 

@application.route('/rfis', methods=['GET','POST'])
def rfis():
    return kie_response('rfis.html')

def kie_response(template):
    # ensure JSONDecodeError works across python 2.7 and 3.5+
    try:
        JSONDecodeError = json.decoder.JSONDecodeError
    except AttributeError:
        JSONDecodeError = ValueError

    # a variable to concatenate json strings
    json_arr = []
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    resp=requests.get(pam_uri+'/services/rest/server/queries/processes/instances/variables/v_priority', auth=HTTPBasicAuth(pam_user,pam_pass), headers=headers)
    try:
        # get all instances in the RFI system
        instances = resp.json()
        for instance in instances['process-instance']:
            resp1 = requests.get(pam_uri+'/services/rest/server/containers/' + container_id + '/processes/instances/'+str(instance['process-instance-id'])+'/variables',auth=HTTPBasicAuth(pam_user,pam_pass),headers=headers).json()
            if "cannot find container" in resp1:
                raise PamContainerException(resp1)
            json_arr.append(resp1)
        return render_template(template, rfis=json_arr)
    except PamContainerException as error:
        logging.error(str(error))
        return render_template('500.html', error_msg=str(error))
    except JSONDecodeError as error:
       msg = "It looks like the KIE server didn't provide a valid JSON response. Please contact the administrator."
       logging.error(str(error))
       return render_template('500.html', error_msg=msg)

