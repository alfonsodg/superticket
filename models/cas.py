import gluon.storage

### this the CAS object used to acces a CAS serive client side
CAS=gluon.storage.Storage()

def _CAS_login(request):
    """
    exposed as CAS.login(request)
    returns a token on success, None on failed authentication
    """
    CAS.incidente=request.vars.incidente
    import urllib
    if not request.vars.incidente:
        redirect("%(login_url)s?service=%(my_url)s" % CAS)
    else:
        url="%(check_url)s?service=%(my_url)s&incidente=%(incidente)s" % CAS
        data=urllib.urlopen(url).read().split('\n')
        if data[0]=='yes': return data[1].split(':')
    return None

def _CAS_logout():
    """
    exposed CAS.logout()
    redirects to the CAS logout page
    """
    import urllib
    redirect("%(logout_url)s?service=%(my_url)s" % CAS)

CAS.login=lambda r=request: _CAS_login(r)
CAS.logout=lambda: _CAS_logout()

### Parameters for the CAS serivice, these should be customized by the user

HOST=request.env.http_x_forwarded_for
if not HOST: HOST=request.env.http_host
### the CAS service login URL
CAS.login_url='http://%s/%s/cas/login' % (HOST,request.application)
### the CAS service check URL
CAS.check_url='http://%s/%s/cas/check' % (HOST,request.application)
### the CAS service logout URL
CAS.logout_url='http://%s/%s/cas/logout' % (HOST,request.application)
### the URL to return to after login
CAS.my_url='http://%s%s' % (HOST,request.env.path_info)
### this is the URL used to confirm and email address
CAS.verify_url='http://%s/%s/cas/verify' % (HOST,request.application)
