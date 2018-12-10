# rfiweb

`rfiweb` is a flask front-end for Andy Yuen's excellent [RCM demo](https://github.com/AndyYuen/rcm2)

## Deployment

`rfiweb` can be deployed standalone or to OpenShift.

### standalone

Install the requirements, preferably in a virtual environment:
```
pip install -r requirements.txt
```
Start the application with gunicorn:
```
gunicorn wsgi:application
```
### openshift

Create a new application from the python 3.6 s2i builder:
```
oc new-app python:3.6~https://github.com/jockey10/rfiweb.git
oc expose svc/rfiweb
```
Set the following environment variables in the deployment config:
```
RHPAM_URI    - the base Process Automation Manager (PAM) URI
RHPAM_USER   - the PAM user
RHPAM_PASS   - the PAM pass
FLASK_SECRET - a value for CSRF protection
```
