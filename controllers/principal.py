#Se importan las librerías necesarias
#Se importan las librerías
import os, socket
import gluon.contenttype
import gluon.fileutils
#Se establece el título de la página
response.title='Administracion de Tablas del SVT'
if not session.incidente: redirect(URL(r=request,c='default',f='login'))

#Se define la vista para el controlador
response.view='principal.html'
##if not session.incidente: redirect(URL(r=request,c='cas',f='login'))
##if session.tipoUsuario<>1: redirect(URL(r=request,c='default',f='index'))
#Se definen las funciones
#Función para listar las tablas necesarias
def index():
    redirect(URL(r=request,f='todos'))
    return dict()
    
    
def todos():
    response.view='principal/todos.html'
    import types as _types
    _dbs = {'db': [('db', 'asiento'), ('db', 'asistencia'), ('db', 'campana'), ('db', 'canton'),('db', 'distrito'),
    ('db', 'evento'), ('db', 'lugar'), ('db', 'medioPago'), ('db', 'medioEnvio'),
    ('db', 'modulo'), ('db', 'pais'), ('db', 'permiso'), ('db', 'provincia'),
    ('db', 'puntoVenta'), ('db', 'ticket'), ('db', 'tipoDescuento'), ('db', 'tipoDocumento'),
    ('db', 'tipoEvento'), ('db', 'supraTipoEvento'),('db', 'tipoPermiso'), ('db', 'tipoTarjeta'), ('db', 'tipoUsuario'),
    ('db', 'usuario'), ('db', 'zona')
    ]} 
    return dict(dbs=_dbs) 
    
    
def ubicacion():
    response.view='principal/ubicacion.html'
    import types as _types
    _dbs = {'db': [('db', 'lugar'), ('db', 'distrito'), ('db', 'canton'), ('db', 'provincia'),('db', 'pais')
    ]} 
    return dict(dbs=_dbs)
    
def usuario():
    response.view='principal/usuario.html'
    import types as _types
    _dbs = {'db': [('db', 'usuario'), ('db', 'tipoUsuario'), ('db', 'modulo'), ('db', 'tipoPermiso'),('db', 'permiso'),
    ('db', 'tipoDocumento')
    ]} 
    return dict(dbs=_dbs)
    
    
def campana():
    response.view='principal/campana.html'
    import types as _types
    _dbs = {'db': [('db', 'campana'), ('db', 'tipoDescuento'), ('db', 'tipoTarjeta'), ('db', 'medioPago')
    ]} 
    return dict(dbs=_dbs)
    
    
def ptoVenta():
    response.view='principal/ptoVenta.html'
    import types as _types
    _dbs = {'db': [('db', 'puntoVenta'), ('db', 'asistencia'), ('db', 'usuario')
    ]} 
    return dict(dbs=_dbs)  
    
          
def evento():
    response.view='principal/evento.html'
    import types as _types
    _dbs = {'db': [('db', 'evento'), ('db', 'tipoEvento'), ('db', 'zona'), ('db', 'lugar'), ('db', 'asiento')
    ]} 
    return dict(dbs=_dbs)       
    
    
def ticket():
    response.view='principal/ticket.html'
    import types as _types
    _dbs = {'db': [('db', 'campana'), ('db', 'tipoDescuento'), ('db', 'tipoTarjeta'), ('db', 'medioPago'), ('db', 'medioEnvio')
    ]} 
    return dict(dbs=_dbs)        
     
            
#Funcion para insertar valores en la tabla seleccionada
def insert():
    try:
        dbname=request.args[0]
        db=eval(dbname)
        table=db[request.args[1]]
    except:
        session.flash='Requerimiento no válido'
        redirect(URL(r=request,f='index'))
    form=SQLFORM(table)
    if form.accepts(request.vars,session):
        response.flash='Nuevo registro insertado'
        redirect(URL(r=request,f='select/%s/%s'%(dbname,table)))
    return dict(form=form)


def select():
    try:
        dbname=request.args[0]
        db=eval(dbname)
        if request.vars.query:
            query=request.vars.query
            orderby=None
            start=0
        elif request.vars.orderby:
            query=session.appadmin_last_query
            orderby=request.vars.orderby
            if orderby==session.appadmin_last_orderby:
                if orderby[-5:]==' DESC': oderby=orderby[:-5]
                else: orderby=orderby+' DESC'
            start=0
        elif request.vars.start!=None:
            query=session.appadmin_last_query
            orderby=session.appadmin_last_orderby
            start=int(request.vars.start)
        else:
            table=request.args[1]
            query='%s.id>0' % table
            orderby=None
            start=0
        session.appadmin_last_query=query
        session.appadmin_last_orderby=orderby
        limitby=(start,start+100)
    except:
        session.flash='Requerimiento no válido'
        redirect(URL(r=request,f='index'))

    try:
        #CAMPAÑA
        if query=='campana.id>0':
            records=db((db.campana.idTipoDescuento==db.tipoDescuento.id)&
                    (db.campana.idTipoTarjeta==db.tipoTarjeta.id)&
                    (db.campana.idMedioPago==db.medioPago.id)&
                    (db.campana.idEvento==db.evento.id)).select(
                    'campana.id','campana.nCampana','campana.fInicioCampana', 'campana.fFinCampana', 
                    'campana.descripcionCampana','campana.observacionCampana', 
                    'tipoDescuento.nTipoDescuento', 'tipoTarjeta.nTipoTarjeta', 'medioPago.nMedioPago', 'evento.nEvento')                             
        #PROVINCIA
        elif query=='provincia.id>0':
            records=db((db.provincia.idPais==db.pais.id)).select('provincia.id',
                    'provincia.nProvincia','pais.nPais')
        #CANTON
        elif query=='canton.id>0':
            records=db((db.canton.idProvincia==db.provincia.id)&
                    (db.provincia.idPais==db.pais.id)).select('canton.id',
                    'canton.nCanton','provincia.nProvincia','pais.nPais')
        #DISTRITO
        elif query=='distrito.id>0':
            records=db((db.distrito.idCanton==db.canton.id)&
                    (db.canton.idProvincia==db.provincia.id)&
                    (db.provincia.idPais==db.pais.id)).select('distrito.id',
                    'distrito.nDistrito','canton.nCanton','distrito.codigoPostalDistrito','provincia.nProvincia','pais.nPais') 
        #LUGAR
        elif query=='lugar.id>0':
            records=db((db.lugar.idDistrito==db.distrito.id)).select('lugar.id',
                    'lugar.nLugar','lugar.direccionLugar','distrito.nDistrito','distrito.codigoPostalDistrito',
                    'lugar.referenciaLugar','lugar.observacionesLugar','lugar.fotoLugar')                                                                             
        #EVENTO
        elif query=='evento.id>0':
            records=db((db.evento.idLugar==db.lugar.id)&
                    (db.evento.idTipoEvento==db.tipoEvento.id)).select('evento.id',
                    'evento.nEvento','tipoEvento.nTipoEvento','lugar.nLugar','evento.descripcionEvento',
                    'evento.observacionEvento','evento.fEvento','evento.hEvento','evento.publicidadEvento',
                    'evento.distribucionAsientosEvento','evento.calificacion')     
        #ZONA
        elif query=='zona.id>0':
            records=db((db.zona.idEvento==db.evento.id)).select('zona.id',
                    'zona.nZona','evento.nEvento','zona.costoZona','zona.descripcionZona',
                    'zona.fotoZona')  
        #ASIENTO
        elif query=='asiento.id>0':
            records=db((db.asiento.idZona==db.zona.id)&
                    (db.asiento.idUsuario==db.usuario.id)).select('asiento.id',
                    'asiento.numeroAsiento','zona.nZona','asiento.estadoAsiento','asiento.fechaCambioEstadoAsiento',
                    'usuario.correoUsuario')  
        #PERMISO
        elif query=='permiso.id>0':
            records=db((db.modulo.id==db.permiso.idModulo)&
                    (db.tipoPermiso.id==db.permiso.idTipoPermiso)&
                    (db.tipoUsuario.id==db.permiso.idTipoUsuario)).select('permiso.id',
                    'modulo.nModulo','tipoPermiso.nTipoPermiso','tipoUsuario.nTipoUsuario')         
        #USUARIO
        elif query=='usuario.id>0':
            records=db((db.usuario.idTipoDocumento==db.tipoDocumento.id)&
                    (db.usuario.idDistrito==db.distrito.id)&
                    (db.usuario.idTipoUsuario==db.tipoUsuario.id)).select('usuario.id',
                    'tipoUsuario.nTipoUsuario','usuario.aPaternoUsuario','usuario.aMaternoUsuario',
                    'usuario.nUsuario', 'tipoDocumento.nTipoDocumento','usuario.numeroDocumentoUsuario',
                    'usuario.direccionUsuario', 'distrito.nDistrito','usuario.telefonoUsuario',
                    'usuario.celularUsuario','usuario.correoUsuario','usuario.fNacimientoUsuario',
                    'usuario.claveUsuario','usuario.activoUsuario','usuario.fInscripcionUsuario')  
        #TICKET
        elif query=='ticket.id>0':
            records=db((db.ticket.idAsiento==db.asiento.id)&
                    (db.ticket.idMedioPago==db.medioPago.id)&
                    (db.ticket.idTipoTarjeta==db.tipoTarjeta.id)&
                    (db.ticket.idCampana==db.campana.id)&
                    (db.ticket.idDistrito==db.distrito.id)&
                    (db.ticket.idCliente==db.usuario.id)&
                    (db.ticket.idVendedor==db.usuario.id)&
                    (db.ticket.idMedioEnvio==db.medioEnvio.id)&
                    (db.ticket.idPuntoVenta==db.puntoVenta.id)).select('ticket.id',
                    'ticket.fVentaTicket','puntoVenta.nPuntoVenta',
                    'asiento.numeroAsiento','usuario.correoUsuario',
                    'ticket.direccionTicket', 'distrito.nDistrito','medioPago.nMedioPago',
                    'tipoTarjeta.nTipoTarjeta', 'ticket.numeroTarjetaTicket','ticket.codigoOperacionTicket',
                    'medioPago.nMedioPago','campana.nCampana','medioEnvio.nMedioEnvio',
                    'ticket.comisionVentaTicket', 'ticket.montoTotalTicket','ticket.fEntregaTicket','ticket.imprimioTicket','ticket.hashTicket')   
        else:
            records=db(query).select(limitby=limitby,orderby=orderby)

    except: 
        response.flash='Consulta SQL errada'
        return dict(records='No hay registros',nrecords=0,query=query,start=0)
    linkto=URL(r=request,f='update',args=[dbname])
    upload=URL(r=request,f='download')
    headers=dict([(c,db[c.split('.')[0]][c.split('.')[1]].label) for c in records.colnames]) 
    return dict(start=start,query=query,orderby=orderby, \
                nrecords=len(records),\
                records=SQLTABLE(records, linkto, upload, _class='sortable', headers=headers))

#Función para actualizar los registros
def update():
    try:
        dbname=request.args[0]
        db=eval(dbname)
        table=request.args[1]
    except:
        response.flash='Requerimiento no válido'
        redirect(URL(r=request,f='index'))
    try:
        id=int(request.args[2])
        record=db(db[table].id==id).select()[0]
    except:
        session.flash='El registro no existe'
        redirect(URL(r=request,f='select/%s/%s'%(dbname,table)))

    form=SQLFORM(db[table],record,deletable=True, delete_label=T('Habilitar para eliminar registro'), 
                 linkto=URL(r=request,f='select',args=[dbname]))

    if form.accepts(request.vars,session): 
        response.flash='Hecho!'
        redirect(URL(r=request,f='select/%s/%s'%(dbname,table)))
    return dict(form=form)

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
