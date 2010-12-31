import datetime, string;
timestamp=datetime.datetime.now()
hoy = datetime.date.today()
dias = datetime.timedelta(days=3)
nuevaFecha = hoy + dias
import random;
if not session.incidente: redirect(URL(r=request,c='default',f='login'))
#if session.tipoUsuario<>3: redirect(URL(r=request,c='default',f='index'))

def buscar():
    selected=[]
    form=FORM(TABLE(
    TD("Nombre usuario"),INPUT(_type='text',_name="nombreUsuario"),
    TD(),INPUT(_type='submit',_value='Buscar')))
    if form.accepts(request.vars, session):
        selected=[[m.id for m in db().select(db.usuario.ALL) 
        if string.lower(form.vars.nombreUsuario) 
        in string.lower(m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario)],
        [m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario for m in db().select(db.usuario.ALL) 
        if string.lower(form.vars.nombreUsuario) 
        in string.lower(m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario)],
        [m.idTipoDocumento for m in db().select(db.usuario.ALL) 
        if string.lower(form.vars.nombreUsuario) 
        in string.lower(m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario)],
        [m.numeroDocumentoUsuario for m in db().select(db.usuario.ALL) 
        if string.lower(form.vars.nombreUsuario) 
        in string.lower(m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario)],        
        [m.direccionUsuario for m in db().select(db.usuario.ALL) 
        if string.lower(form.vars.nombreUsuario) 
        in string.lower(m.nUsuario+' '+m.aPaternoUsuario+' '+m.aMaternoUsuario)],
        [m.distrito.nDistrito for m in db(db.distrito.id==db.usuario.idDistrito).select() 
        if string.lower(form.vars.nombreUsuario)
        in string.lower(m.usuario.nUsuario+' '+m.usuario.aPaternoUsuario+' '+m.usuario.aMaternoUsuario)]]
                    
        selected=map(None,*selected)
        selected.insert(0,["ID","Usuario","Tipo de Doc.","Num. Doc.","Dirección","Distrito"])
            
    return dict(form=form, selected=selected)

def index():
    if not request.vars.id: 
        id=1
    else:
        id=request.vars.id
    if not session.idUsuario:
        session.vendedor=2
    else:
        session.vendedor=session.idUsuario
    if not request.vars.cliente:
        session.cliente=7
    else:
        session.cliente=request.vars.cliente    
    #session.cliente=7
    session.lista=""     
    session.desc=0
    session.pEnvio=0
    session.puntoVenta=''
    session.costoAsientos=0
    session.direccion=''
    session.distrito=''
    session.puntoVenta=''
    session.total=0
    session.totalPorAsiento=0
    
    form=FORM(TABLE(
    TD("Consultar otra zona"), TD(SELECT(_id="listaZonaEvento",_name="listaZonaEvento",
    *[OPTION(x.zona.nZona,_value=x.zona.id)
    for x in db((db.evento.id==(db(db.zona.id==id).select(db.zona.ALL))[0].idEvento)&\
    (db.zona.idEvento==db.evento.id)).select(orderby=db.evento.nEvento)])),
    INPUT(_type='submit',_value='Consultar asientos disponibles')))
    
    if form.accepts(request.vars, session): 
        id=form.vars.listaZonaEvento
    asientos=db((db.asiento.idZona==id)&(db.zona.id==db.asiento.idZona)&\
    (db.evento.id==db.zona.idEvento)).select()
    filaAsientos=db(db.asiento.idZona==id).select(db.asiento.FilaAsiento, groupby=db.asiento.FilaAsiento)
    if not len(asientos): redirect(URL(r=request,c='default',f='falla'))
    cliente=db(db.usuario.id==session.cliente).select()
    vendedor=db(db.usuario.id==session.vendedor).select()
    if request.vars.boton:
        listaAsientos=((request.vars.asientosActivos)[1:]).split(';')
        for asiento in listaAsientos:
            cont=0
            for elemento in listaAsientos: 
                if asiento==elemento: cont+=1
            if cont%2==0:
                while cont>0: cont-=1; listaAsientos.remove(asiento);
            else:
                while cont>1: cont-=1; listaAsientos.remove(asiento);
        if not len(listaAsientos):
            response.flash = 'Ningún asiento seleccionado'
        elif listaAsientos[0]=='':
            response.flash = 'Ningún asiento seleccionado'
        else:
            session.lista=listaAsientos 
            redirect(URL(r=request,f='venta'))
    return dict(form=form, asientos=asientos, filaAsientos= filaAsientos,
                cliente=cliente, vendedor=vendedor)
def venta():
    cliente=db(db.usuario.id==session.cliente).select()
    vendedor=db(db.usuario.id==5).select()
    medioEnvio=db().select(db.medioEnvio.ALL)
    puntoVenta=db(db.puntoVenta.id!=3).select(db.puntoVenta.ALL)#sin el punto de venta VIAWEB
    distrito=db().select(db.distrito.ALL)
    medioPago=db(db.medioPago.id!=1).select(db.medioPago.ALL)
    tipoTarjeta=db().select(db.tipoTarjeta.ALL)
    campana=db().select(db.campana.ALL) 
    paisProvincia = db((db.provincia.idPais==db.pais.id)&(db.canton.idProvincia==db.provincia.id)&\
    (db.distrito.idCanton==db.canton.id)&(db.canton.id>0)).select(groupby=db.provincia.id) 
    numAsiento=[]
    numFila=[]    
    if not len(session.lista):
        redirect(URL(r=request,f='index'))
    for a in db().select(db.asiento.ALL):
        for x in xrange(len(session.lista)):
            if a.id==int(session.lista[x]):
                numAsiento.append('Fila: '+str(a.FilaAsiento)+' - Asiento: '+str(a.numeroAsiento))
    aregistros = db((db.asiento.id==session.lista[0])&\
                (db.asiento.idZona==db.zona.id)&\
                (db.zona.idEvento==db.evento.id)).select()
    session.costoAsientos=int(aregistros[0].zona.costoZona)*len(session.lista)
    session.evento=aregistros[0].evento.id
    if request.vars.boton:
        time.sleep(5)
        if request.vars.medioEnvio=='1':
            session.direccion=request.vars.direccion
            session.distrito=request.vars.cantonDistrito
        else:
            session.direccion=(db(db.puntoVenta.id==3).select(db.puntoVenta.ALL))[0].direccionPuntoVenta
            session.distrito=(db(db.puntoVenta.id==3).select(db.puntoVenta.ALL))[0].idDistrito
        for x in xrange(len(session.lista)):
            db.ticket.insert(
            direccionTicket=str(session.direccion),
            comisionVentaTicket=int(datos.comision),
            montoTotalTicket=session.totalPorAsiento,
            imprimioTicket=False,
            hashTicket='',#falta implementar el valor para el hash
            codigoOperacionTicket='',#falta implementar el valor para el codigo de operacions
            fVentaTicket=timestamp,
            fEntregaTicket=nuevaFecha,#falta aumentar a la fecha 3 dias
            idAsiento=int(session.lista[x]),
            idMedioEnvio=str(request.vars.medioEnvio),
            idCampana=str(session.campana),
            numeroTarjetaTicket=str(request.vars.numTarjeta),
            pinTicket=random.randint(0,9999),#falta implementar el valor para el pin
            observaciones=str(request.vars.observaciones),
            idTipoTarjeta=str(request.vars.tipoTarjeta),
            idMedioPago=str(request.vars.medioPago),
            idDistrito=str(session.distrito),
            idCliente=str(session.cliente),
            idVendedor=(session.vendedor),
            idPuntoVenta=str(session.puntoVenta))
        redirect(URL(r=request,f='ok'))
    return dict(datosUnicos=aregistros[0], numAsiento=numAsiento,
    medioEnvio=medioEnvio, puntoVenta=puntoVenta, distrito=distrito,
    medioPago=medioPago, tipoTarjeta=tipoTarjeta, campana=campana, paisProvincia= paisProvincia,
    cliente=cliente, vendedor=vendedor)

def ok():
    for x in session.lista:
        db(db.asiento.id==x).update(estadoAsiento='1')
    for x in session.lista:
        session.lista.remove(x)
    session.lista=''    
    session.vendedor=5   
    session.desc=0
    session.pEnvio=0
    session.puntoVenta=''
    session.costoAsientos=0
    session.direccion=''
    session.distrito=''
    session.puntoVenta=''
    session.total=0
    session.totalPorAsiento=0
    time.sleep(2)
    response.flash='Compra exitosa'
    return dict()
        
def envio():
    if request.vars.medioEnvioId=='1':
        session.puntoVenta=3
    else:
        session.puntoVenta=request.vars.puntoVentaId
    precioEnvio=db(request.vars.medioEnvioId==db.medioEnvio.id).select()
    return 'Envio: ' + str(precioEnvio[0].precioMedioEnvio)

def campana():
    r=db((db.campana.id>0)&\
    (db.campana.fInicioCampana<timestamp)&(db.campana.fFinCampana>timestamp)&\
    (db.campana.idEvento==session.evento)&(db.campana.idMedioPago==request.vars.medioPagoId)&\
    (db.campana.idTipoTarjeta ==request.vars.tipoTarjetaId)    
    ).select()
    if len(r)>0:
        session.campana=r[0].id
        return 'Campaña: '+str(r[0].nCampana)
    else:
        session.campana=1
        return  'Campaña: '+str((db(db.campana.id==1).select(db.campana.ALL))[0].nCampana)
def descuento():
    r=db((db.campana.id>0)&\
    (db.campana.fInicioCampana<timestamp)&(db.campana.fFinCampana>timestamp)&\
    (db.campana.idEvento==session.evento)&(db.campana.idMedioPago==request.vars.medioPagoId)&\
    (db.campana.idTipoTarjeta ==request.vars.tipoTarjetaId)    
    ).select()
    if len(r)>0:
        descuento=db((db.campana.id==r[0].id)&\
            (db.campana.idTipoDescuento==db.tipoDescuento.id)).select()        
    else:
        descuento=db((db.campana.id==1)&\
            (db.campana.idTipoDescuento==db.tipoDescuento.id)).select()        
    return 'Descuento: '+\
                str((session.costoAsientos*(int(descuento[0].tipoDescuento.porcetajeTipoDescuento))/100))

def precios():
    r=db((db.campana.id>0)&\
    (db.campana.fInicioCampana<timestamp)&(db.campana.fFinCampana>timestamp)&\
    (db.campana.idEvento==session.evento)&(db.campana.idMedioPago==request.vars.medioPagoId)&\
    (db.campana.idTipoTarjeta ==request.vars.tipoTarjetaId)    
    ).select()
    if len(r)>0:
        descuento=db((db.campana.id==r[0].id)&\
            (db.campana.idTipoDescuento==db.tipoDescuento.id)).select()        
    else:
        descuento=db((db.campana.id==1)&\
            (db.campana.idTipoDescuento==db.tipoDescuento.id)).select()        
    precioEnvio=db(db.medioEnvio.id==request.vars.medioEnvioId).select()
    session.pEnvio = int(precioEnvio[0].precioMedioEnvio)
    session.desc = int(descuento[0].tipoDescuento.porcetajeTipoDescuento)
    session.total=int(datos.comision) + (session.costoAsientos*(100-session.desc)/100) + session.pEnvio
    session.totalPorAsiento=int(session.total)/len(session.lista)
    return 'Total: '+str(session.total)

def cantonDistrito(): 
    provincia = request.vars.paisDistrito
    cantonDistrito = db((db.canton.idProvincia == provincia)&(db.canton.id==db.distrito.idCanton)).select() 
    return SELECT(_id="cantonDistritoId",_name="cantonDistrito",_type="select",
            *[OPTION(cantonDistrito[i].canton.nCanton+'-'+ cantonDistrito[i].distrito.nDistrito, _value=str 
            (cantonDistrito[i].distrito.id)) for i in range(len(cantonDistrito))])
