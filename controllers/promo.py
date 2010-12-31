import datetime 
import random
now=datetime.datetime.now()

def index(): return dict(message="No hay Registros Disponibles")

def evento():
    registros=db((db.evento.fEvento>now)&(db.evento.id>0)&(db.lugar.id==db.evento.idLugar)).select(orderby = "evento.calificacion DESC")
    if not len(registros): redirect(URL(r=request,f='index'))
    tantos=len(registros)
    if tantos<3:
        cantidad=int(tantos)
    else:   
        cantidad=3 
    return dict(registros=registros,cantidad=cantidad)
    
def promo():
    registros=db((db.evento.fEvento>now)&(db.evento.id>0)&(db.lugar.id==db.evento.idLugar)).select()
    if not len(registros): redirect(URL(r=request,f='index'))
    tantos=len(registros)
    cantidad=random.randint(0, tantos-1)
    return dict(registros=registros,cantidad=cantidad)    

def categoria():
    registros=db((db.supraTipoEvento.id>0)).select(orderby = "supraTipoEvento.nSupraTipoEvento ASC")
    if not len(registros): redirect(URL(r=request,f='index'))
    return dict(registros=registros)
    
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
