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

## keycloak configuration

RFIweb can be configured with Keycloak/Red Hat Single Sign On.

Firstly, create a new SSO container instance ensuring that the admin username and password are set. The default routes will be created with a TLS re-encrypt policy, which is fine.

Create an RFI web instance:
```
oc new-app python:3.6~https://github.com/jockey10/rfiweb.git
``` 
Create a new secure route for RFIweb using a TLS edge policy.

Create a client in SSO with the HTTPS URL for RFIweb. Ensure a user is created for the application.

Create a file `keycloak.json` in the `static` directory of rfiweb, and add the following:
```
{
  "realm" : "keycloak realm for rfiweb",
  "auth-server-url" : "https://sso-server/auth",
  "resource" : "keycloak client id for rfiweb",
  "public-client": "true"
}
```
Access the RFIweb URL from OpenShift, and you should be redirected to Keycloak.
