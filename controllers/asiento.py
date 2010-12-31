import datetime 
now=datetime.datetime.now()
response.title='Generador de Asientos'

if not session.incidente: redirect(URL(r=request,c='default',f='login'))

def evento():
    records=db().select(db.evento.ALL)
    return dict(records=records)
    
           
def zona():
    id=request.vars.id
    zonas=db(db.zona.idEvento==id).select(db.zona.ALL)
    evento=[x.nEvento for x in db(db.evento.id==id).select(db.evento.nEvento)]    
    if not len(zonas): redirect(URL(r=request,f='evento'))
    return dict(zonas=zonas, evento=evento)

def asiento():
    id=request.vars.id
    numAsientos=db(db.asiento.idZona==id).count()    
    zona=[x.nZona for x in db(db.zona.id==id).select(db.zona.nZona)]
    eventoId=[x.id for x in db((db.zona.id==id)&(db.evento.id==db.zona.idEvento)).select(db.evento.id)]
    zonaId=[x.id for x in db(db.zona.id==id).select(db.zona.id)]
    evento=[x.nEvento for x in db((db.zona.id==id) & (db.zona.idEvento==db.evento.id)).select(db.evento.nEvento)]
    form=FORM(TABLE(
    TR(TD(),TD("Cantidad de asientos: ", INPUT(_type="text",_name="asientos", value='0', requires=IS_NOT_EMPTY()))
    ,TD("Fila: ", INPUT(_type="text",_name="fila", requires=IS_NOT_EMPTY()))),
    TR(TD(),INPUT(_type='submit',_value='Enviar datos'))))   
    if form.accepts(request.vars, session):
        numAsientosFila = db(db.asiento.FilaAsiento==form.vars.fila).count()
        for valor in xrange(int(form.vars.asientos)):
                db.asiento.insert(FilaAsiento=form.vars.fila, numeroAsiento=valor+1+numAsientosFila, idZona=int(zonaId[0]), estadoAsiento=0, fechaCambioEstadoAsiento=now)
        redirect=URL(r=request,c='principal',f='asiento?id=%s'%zonaId)
        numAsientos=db(db.asiento.idZona==id).count()
    asientos=db(db.asiento.idZona==id).select(db.asiento.ALL, orderby=db.asiento.FilaAsiento)
    #if not len(asientos) and not id: redirect(URL(r=request,f='evento'))
    return dict(form=form, asientos=asientos,zona=zona,evento=evento,numAsientos=numAsientos,eventoId=eventoId[0])
