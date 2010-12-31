import datetime 
now=datetime.datetime.now()
response.title='Sistema de Venta de Tickets'

### the CAS service login URL
#CAS.login_url='http://maccticket.com/SVT/cas/login'
CAS.login_url='http://127.0.0.1:8000/SVT/cas/login'
### the CAS service check URL
#CAS.check_url='http://maccticket.com/SVT/cas/check'
CAS.check_url='http://127.0.0.1:8000/SVT/cas/check'
### the CAS service logout URL
#CAS.logout_url='http://maccticket.com/SVT/cas/logout'
CAS.logout_url='http://127.0.0.1:8000/SVT/cas/logout'
### the URL to return to after login
#CAS.my_url='http://maccticket.com/default/index'
CAS.my_url='http://127.0.0.1:8000/SVT/default/index'

def falla(): return dict(message="No hay Registros Disponibles temporalmente intentelo mas tarde")

def index():
    records=db((db.evento.fEvento>now)&(db.evento.id>0)&(db.lugar.id==db.evento.idLugar)&(db.tipoEvento.id==db.evento.idTipoEvento)).select(orderby = "evento.fEvento ASC")
    if not len(records): redirect(URL(r=request,f='falla'))
    return dict(records=records)    

def supra():
    id=request.vars.id
    records=db((db.supraTipoEvento.id==id)&(db.supraTipoEvento.id==db.tipoEvento.idSupraTipoEvento)).select(orderby = "supraTipoEvento.nSupraTipoEvento ASC")
    if not len(records): redirect(URL(r=request,f='index'))
    return dict(records=records)

def evento():
    id=request.vars.id
    records=db((db.evento.fEvento>now)&(db.evento.idTipoEvento==id)&(db.lugar.id==db.evento.idLugar)&(db.tipoEvento.id==db.evento.idTipoEvento)).select(orderby = "evento.fEvento ASC")
    if not len(records): redirect(URL(r=request,f='index'))
    return dict(records=records)

def zona():
    id=request.vars.id
    records=db((db.zona.idEvento==id)&(db.evento.id==db.zona.idEvento)&(db.lugar.id==db.evento.idLugar)).select(orderby = "zona.costoZona DESC")     
    if not len(records): redirect(URL(r=request,f='index'))
    return dict(records=records)

def ptoVenta():
    id=1
    records=db().select(db.puntoVenta.ALL)    
    if not len(records): redirect(URL(r=request,f='index'))
    return dict(records=records)    
def login():
    session.token=CAS.login(request)
    redirect(URL(r=request,f='index'))    
def logout():
    session.token=None
    CAS.logout()

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/download/[filename]
    """
    return response.download(request,db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
