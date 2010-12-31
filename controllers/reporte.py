import applications.SVT.modules.fecha as fecha
if not session.incidente: redirect(URL(r=request,c='default',f='login'))

##############################################
#LIBRERIAS DEL REPORTLAB 
##############################################
try:
    from reportlab.lib.pagesizes import A4, landscape, portrait 
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
    from reportlab.platypus import   Spacer, SimpleDocTemplate, Table, TableStyle
    from reportlab.platypus import Paragraph, Image    
    from reportlab.lib import colors  
    f = file('./applications/SVT/logo.jpg')   
except:
    redirect(URL(r=request, c='default', f='index'))
    #redirect(URL(r=request))
##############################################
#LIBRERIAS DEL WEB2PY
##############################################
import datetime;
import time;
timestamp=datetime.datetime.now()
now=time.time()
##############################################
#DATOS GENERALES PARA LOS REPORTES
##############################################
styleSheet=getSampleStyleSheet()                               
style=styleSheet['BodyText']
h1=styleSheet['Heading1'] 
h1.pageBreakBefore=0       
h1.keepWithNext=1
h2=styleSheet['Heading2']   
h2.pageBreakBefore=0        
h2.keepWithNext=6
EstiloTablaH=TableStyle([('VALIGN',(0,0),(0,0),'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
        ('GRID',(0,0),(-1,0),1.5,colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
EstiloTablaV=TableStyle([('VALIGN',(0,0),(0,0),'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lavender),
        ('GRID',(0,0),(0,-1),1.5,colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
story=[]
# INICIO DEL REPORTE , CONTENIDO PARA TODOS LOS INFORMES - USUARIO Y FECHA
usuario=[['Usuario Id',session.idUsuario],['Fecha', str(timestamp)[:10]] ]; t=Table(usuario); t.hAlign='RIGHT'
t.setStyle(EstiloTablaV); story.append(t)
# LOGO Y NOMBRE DE LA EMPRESA
logo=Image(f,width=100,height=40); logo.hAlign='CENTER'; story.append(logo)
titulo=Table([['Sistema de ventas de ticket']]); story.append(titulo); story.append(Spacer(0,20))
def reporte01(x,y,z):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Detalle de ventas por Evento" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    P=Paragraph("TIPO DE REPORTE: 01" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    #CONSULTA
    consulta=db((db.evento.id==x)&(db.ticket.idPuntoVenta==y)&\
    (db.ticket.idMedioPago==z)&(db.ticket.idMedioPago==db.medioPago.id)&\
    (db.ticket.idPuntoVenta==db.puntoVenta.id)&(db.evento.idTipoEvento==db.tipoEvento.id)&\
    (db.zona.idEvento==db.evento.id)&(db.asiento.idZona==db.zona.id)&\
    (db.ticket.idAsiento==db.asiento.id)&(db.ticket.idCampana==db.campana.id)&\
    (db.ticket.idMedioEnvio==db.medioEnvio.id)&(db.campana.idTipoDescuento==db.tipoDescuento.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #response.flash='No hay una consulta'
        redirect(URL(r=request))
    Evento =str(consulta[0].evento.nEvento)
    TipoEvento = str(consulta[0].tipoEvento.nTipoEvento)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Evento',Evento],['Tipo Evento', TipoEvento]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t); story.append(Spacer(0,12))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['#Asiento'], ['Zona'], ['FechaVenta'], ['Costo'], ['Descuento'], ['Monto Total'],
    ['Pto. Venta'],['Medio Pago']]
    m=[[x.asiento.numeroAsiento  for x in consulta],[x.zona.nZona  for x in consulta],
    [x.ticket.fVentaTicket  for x in consulta],[x.zona.costoZona  for x in consulta],
    [x.tipoDescuento.porcetajeTipoDescuento  for x in consulta],
    [x.ticket.montoTotalTicket  for x in consulta],
    [x.puntoVenta.nPuntoVenta  for x in consulta],
    [x.medioPago.nMedioPago  for x in consulta]]
    mcab=[cab[x]+m[x] for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab); t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=landscape(A4),showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte02(x):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Evento - precios" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    P=Paragraph("TIPO DE REPORTE: 02" ,h1);  story.append(P);  
    story.append(Spacer(0,12))    
    #CONSULTA
    consulta=db((db.evento.id==x)&(db.evento.idTipoEvento==db.tipoEvento.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request))
    Evento =str(consulta[0].evento.nEvento)
    TipoEvento = str(consulta[0].tipoEvento.nTipoEvento)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Evento',Evento],['Tipo Evento', TipoEvento]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t)
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Zona'],['Cantidad'],['Costo'],['Descuento(%)'],['Costo Total']]
    sql=db.executesql('select nZona,count(estadoAsiento),costoZona,sum(porcetajeTipoDescuento),\
                    count(estadoAsiento)*costoZona\
                    from evento inner join zona \
                    on zona.idEvento=evento.id inner join asiento\
                    on asiento.idZona=zona.id inner join ticket\
                    on ticket.idAsiento=asiento.id inner join campana\
                    on ticket.idCampana=campana.id inner join tipoDescuento\
                    on campana.idTipoDescuento=tipoDescuento.id\
                    where evento.id='+x+' and estadoAsiento=1\
                    group by zona.id')
    m=[]
    for i in sql: m.append(list(i))
    if not len(m):
        print 'No hay una consultaa'
        redirect(URL(r=request))    
    m=map(None,*m);
    mcab=[cab[x]+list(m[x]) for x in range(len(cab))]; 
    mcab=map(None,*mcab); t=Table(mcab);
    t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=A4,showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte03(x):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Asientos vendidos - ADM." ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    P=Paragraph("TIPO DE REPORTE: 03" ,h1);  story.append(P);  
    story.append(Spacer(0,12))    
    #CONSULTA
    consulta=db((db.evento.id==x)&(db.evento.idTipoEvento==db.tipoEvento.id)&\
    (db.zona.idEvento==db.evento.id)&(db.asiento.idZona==db.zona.id)&\
    (db.ticket.idAsiento==db.asiento.id)&(db.ticket.idCampana==db.campana.id)&\
    (db.ticket.idMedioPago==db.medioPago.id)&(db.ticket.idTipoTarjeta==db.tipoTarjeta.id)&\
    (db.ticket.idMedioEnvio==db.medioEnvio.id)&(db.campana.idTipoDescuento==db.tipoDescuento.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request))
    Evento =str(consulta[0].evento.nEvento)
    TipoEvento = str(consulta[0].tipoEvento.nTipoEvento)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Evento',Evento],['Tipo Evento', TipoEvento]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t); story.append(Spacer(0,12))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['#Venta'],['FechaVenta'],['#Asiento'],['Zona'],['Medio Pago'] ,['Tipo tarjeta'],
    ['Costo'],['Comision'],['Costo envio'], ['Descuento'], ['Monto Total']]
    m=[[x.ticket.id  for x in consulta],[x.ticket.fVentaTicket  for x in consulta],
    [x.asiento.numeroAsiento  for x in consulta],[x.zona.nZona  for x in consulta],
    [x.medioPago.nMedioPago for x in consulta],[x.tipoTarjeta.nTipoTarjeta for x in consulta],
    [x.zona.costoZona  for x in consulta],[int(datos.comision) for x in range(len(consulta))],
    [x.medioEnvio.precioMedioEnvio  for x in consulta],
    [x.tipoDescuento.porcetajeTipoDescuento  for x in consulta],
    [x.ticket.montoTotalTicket  for x in consulta]]
    mcab=[cab[x]+m[x] for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab); t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=landscape(A4),showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte04(x):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Asiento vendidos - ADM." ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    P=Paragraph("TIPO DE REPORTE: 04" ,h1);  story.append(P);  
    story.append(Spacer(0,12))      
    #CONSULTA
    consulta=db((db.evento.id>0)&(db.evento.idTipoEvento==db.tipoEvento.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request))
    Evento =str(consulta[0].evento.nEvento)
    TipoEvento = str(consulta[0].tipoEvento.nTipoEvento)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Evento',Evento],['Tipo Evento', TipoEvento]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t); story.append(Spacer(0,12))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Zona'],['Cantidad'],['Costo'],['Total Envio'],['Total desc.'],['Comision'],['Costo Total']]
    sql=db.executesql('select nZona,count(estadoAsiento),costoZona,'+str(datos.comision)+
                    ', sum(precioMedioEnvio), sum(porcetajeTipoDescuento),count(estadoAsiento)*costoZona\
                    from evento inner join zona \
                    on zona.idEvento=evento.id inner join asiento\
                    on asiento.idZona=zona.id inner join ticket\
                    on ticket.idAsiento=asiento.id inner join campana\
                    on ticket.idCampana=campana.id inner join tipoDescuento\
                    on campana.idTipoDescuento=tipoDescuento.id inner join medioEnvio\
                    on ticket.idMedioEnvio=medioEnvio.id\
                    where evento.id='+x+' and estadoAsiento=1\
                    group by zona.id')
    m=[]
    for i in sql: m.append(list(i))
    if not len(m):
        print 'No hay una consulta'
        redirect(URL(r=request))
    m=map(None,*m); mcab=[cab[x]+list(m[x]) for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab);
    t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=A4,showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte05(x):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Evento - precios" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    #CONSULTA
    consulta=db((db.evento.id==x)&(db.evento.idTipoEvento==db.tipoEvento.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request,c='default', f='index'))#redirect(URL(r=request))
    Evento =str(consulta[0].evento.nEvento)
    TipoEvento = str(consulta[0].tipoEvento.nTipoEvento)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Evento',Evento],['Tipo Evento', TipoEvento]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t); story.append(Spacer(0,12))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Zona'],['Cantidad comprada'],['Cantidad disponible']]
    sql1=db.executesql('select nZona,count(estadoAsiento) \
                    from evento inner join zona \
                    on zona.idEvento=evento.id inner join asiento\
                    on asiento.idZona=zona.id where evento.id='+x+' and estadoAsiento=1\
                    group by zona.id')
    sql2=db.executesql('select count(estadoAsiento) from evento inner join zona \
                    on zona.idEvento=evento.id inner join asiento\
                    on asiento.idZona=zona.id where evento.id='+x+' and estadoAsiento=0\
                    group by zona.id')
    m1=[]
    for i in sql1: m1.append(list(i)); print m1
    m2=[]
    for i in sql2: m2.append(list(i))   
    m1=map(None,*m1); m2=map(None,*m2); m1+=m2; 
    if not len(m1):
        #print 'No hay una consulta'
        redirect(URL(r=request))
    mcab=[cab[x]+list(m1[x])for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab);
    t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=A4,showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte06():
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Reporte de eventos" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    #CONSULTA
    consulta=db((db.evento.id>0)&\
    (db.evento.idLugar==db.lugar.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request,c='default', f='index'))#redirect(URL(r=request))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Nombre evento'], ['Lugar'], ['Fecha '], ['Status']]
    m=[[x.evento.nEvento  for x in consulta],[x.lugar.nLugar  for x in consulta],
    [x.evento. fEvento  for x in consulta],[x.evento.calificacion  for x in consulta]]
    mcab=[cab[x]+m[x] for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab); t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=A4,showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte07():
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Reporte de vendedores" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    #CONSULTA
    consulta=db((db.usuario.id>0)&(db.usuario.idDistrito==db.distrito.id)&\
    (db.distrito.idCanton==db.canton.id)&\
    (db.canton.idProvincia==db.provincia.id)&(db.provincia.idPais==db.pais.id)).select() 
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request,c='default', f='index'))#redirect(URL(r=request))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Usuario '], ['A Paterno'], ['A Materno'], ['Nombres(s)'],['DNI'],['direccion'],
    ['distrito'],['provincia'],['canton'],['Pais'],['telefono'],['e-mail']]
    m=[[x.usuario.nUsuario  for x in consulta],[x.usuario.aPaternoUsuario  for x in consulta],
    [x.usuario.aMaternoUsuario  for x in consulta], [x.usuario. nUsuario for x in consulta],
    [x.usuario.numeroDocumentoUsuario  for x in consulta], [x.usuario.direccionUsuario  for x in consulta],
    [x.distrito.nDistrito  for x in consulta],[x.canton.nCanton  for x in consulta],
    [x.provincia.nProvincia  for x in consulta],[x.pais.nPais  for x in consulta],
    [x.usuario.telefonoUsuario  for x in consulta],[x.usuario.correoUsuario  for x in consulta]]    
    mcab=[cab[x]+m[x] for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab); t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=landscape(A4),showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte08(x,y):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Reporte clientes TOP" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    #CONSULTA
    consulta=db((db.ticket.fVentaTicket>x)&(db.ticket.fVentaTicket<y)&\
    (db.usuario.idDistrito==db.distrito.id)&\
    (db.distrito.idCanton==db.canton.id)&(db.ticket.idCliente==db.usuario.id)&\
    (db.canton.idProvincia==db.provincia.id)&(db.provincia.idPais==db.pais.id)).select(groupby=db.usuario.id ) 
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request,c='default', f='index'))#redirect(URL(r=request))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Usuario '], ['A Paterno'], ['A Materno'], ['Nombres(s)'],['DNI'],['direccion'],
    ['distrito'],['provincia'],['canton'],['Pais'],['telefono'],['e-mail']]
    m=[[x.usuario.nUsuario  for x in consulta],[x.usuario.aPaternoUsuario  for x in consulta],
    [x.usuario.aMaternoUsuario  for x in consulta], [x.usuario. nUsuario for x in consulta],
    [x.usuario.numeroDocumentoUsuario  for x in consulta], [x.usuario.direccionUsuario  for x in consulta],
    [x.distrito.nDistrito  for x in consulta],[x.canton.nCanton  for x in consulta],
    [x.provincia.nProvincia  for x in consulta],[x.pais.nPais  for x in consulta],
    [x.usuario.telefonoUsuario  for x in consulta],[x.usuario.correoUsuario  for x in consulta]]    
    mcab=[cab[x]+m[x] for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab); t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=landscape(A4),showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def reporte09(x,y,z):
    #TITULO DEL REPORTE
    P=Paragraph("TÍTULO DEL REPORTE: Reporte de los puntos de venta" ,h1);  story.append(P);  
    story.append(Spacer(0,12))
    P=Paragraph("TIPO DE REPORTE: 09" ,h1);  story.append(P);  
    story.append(Spacer(0,12)) 
    #CONSULTA
    consulta=db((db.puntoVenta.id==z)&(db.ticket.idPuntoVenta==db.puntoVenta.id)).select()
    #CABECERA DEL REPORTE
    if not len(consulta):
        #print 'No hay una consulta'
        redirect(URL(r=request,c='default', f='index'))#redirect(URL(r=request))
    PuntoVenta =str(consulta[0].puntoVenta.nPuntoVenta)
    Direccion = str(consulta[0].puntoVenta.direccionPuntoVenta)
    P=Paragraph("Cabecera del reporte",h1); story.append(P)
    cab=[['Punto de Venta', PuntoVenta],['Dirección', Direccion]]; t=Table(cab); t.hAlign='CENTER'
    t.setStyle(EstiloTablaV); story.append(t); story.append(Spacer(0,12))
    #CUERPO DEL REPORTE
    P=Paragraph("Cuerpo del reporte",h1); story.append(P)
    cab=[['Evento'],['Zona'],['Monto Vendido'],['Participación Zona %'],['Participación Evento %']]
    sql=db.executesql('select nEvento, nZona, sum(montoTotalTicket),\
                    sum(montoTotalTicket)*100/(select sum(montoTotalTicket) FROM ticket), \
                    sum(montoTotalTicket)*100/(select sum(montoTotalTicket) FROM ticket\
                    inner join asiento on ticket.idAsiento=asiento.id inner join zona on\
                    zona.id=asiento.idZona group by zona.id) \
                    from evento inner join zona \
                    on zona.idEvento=evento.id inner join asiento\
                    on asiento.idZona=zona.id inner join ticket\
                    on ticket.idAsiento=asiento.id inner join puntoVenta \
                    on ticket.idPuntoVenta=puntoVenta.id\
                    where  puntoVenta.id='+z+' and estadoAsiento=1 and\
                    ticket.fVentaTicket between ('+ fechaNueva(x)+') and ('+ fechaNueva(y)+')\
                    group by zona.id, evento.id')
    print fechaNueva(x)
    m=[]#buscar between
    for i in sql: m.append(list(i))
    if not len(m):
        print 'No hay una consulta'
        redirect(URL(r=request))    
    m=map(None,*m); mcab=[cab[x]+list(m[x]) for x in range(len(cab))]; mcab=map(None,*mcab); t=Table(mcab);
    t.setStyle(EstiloTablaH)
    story.append(t)
    story.append(Spacer(0,10))
    doc=SimpleDocTemplate("Reporte.pdf",pagesize=A4,showBoundary=1); doc.build(story)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=Reporte.pdf'
    return response.stream(open("Reporte.pdf", 'rb'))
def fechaNueva(x):
    anio=str(x)[:4]
    mes=str(x)[5:][:2]
    dia=str(x)[8:]
    x="'"+dia+"/"+mes+"/"+anio+"'"
    return x
    
def index(): 
    #a=db.executesql('select nReporte from reporte where permisoReporte like 2')
    #consulta=db((db.reporte.permisoReporte.like('%'+'2'+'%'))).select(db.reporte.ALL)
    #reporte=[x.nReporte+' - '+x.descripcionReporte for x in consulta]  
    form=FORM(TABLE(
    TR("Tipo de reporte:",
    SELECT(_type="select", _id="tipo", _name="tipo",
    *[OPTION(x.nReporte+' - '+x.descripcionReporte ,_value=x.id-1)
     for x in db((db.reporte.id>0)&\
     (db.reporte.permisoReporte.like('%'+str(session.tipoUsuario).capitalize()+'%'))).
     select(db.reporte.ALL)])),
    TR(LABEL("Evento",_id="lbE"), SELECT(_id="evento",_name="evento",*[OPTION(x.nEvento,_value=x.id)
    for x in db().select(db.evento.ALL)])),
    TR(LABEL("Pto. venta",_id="lbP"),SELECT(_id="pto",_name="pto",*[OPTION(x.nPuntoVenta,_value=x.id)
    for x in db().select(db.puntoVenta.ALL)])),
    TR(LABEL("Medio de pago",_id="lbM"),SELECT(_id="mPago",_name="mPago",*[OPTION(x.nMedioPago,_value=x.id)
    for x in db().select(db.medioPago.ALL)])),    
    TR(LABEL("Fecha Inicio",_id="lbFI"), INPUT(_id="fInicio",_name="datelimite1",_class='date')), 
    TR(LABEL("Fecha final",_id="lbFF"), INPUT(_id="fFin",_name="datelimite2",_class='date')),     
    TR("", INPUT(_type='submit',_value='Reporte'))
        )) 
    if form.accepts(request.vars, session): 
        #print form.vars.evento
        try:
            if form.vars.tipo=='0':
                return reporte01(form.vars.evento,form.vars.pto,form.vars.mPago)
            elif form.vars.tipo=='1':
                return reporte02(form.vars.evento)
            elif form.vars.tipo=='2':
                return reporte03(form.vars.evento)
            elif form.vars.tipo=='3':
                return reporte04(form.vars.evento)
            elif form.vars.tipo=='4':
                return reporte05(form.vars.evento)
            elif form.vars.tipo=='5':
                return reporte06()
            elif form.vars.tipo=='6':
                return reporte07()
            elif form.vars.tipo=='7':
                return reporte08(form.vars.datelimite1 , form.vars.datelimite2)
            elif form.vars.tipo=='8':
                return reporte09(form.vars.datelimite1 ,form.vars.datelimite2 , form.vars.pto )
        except:
            response.flash='Consulta vacia, error al generar el reporte'     
        #redirect(URL(r=request,c='reporte', f='fun'))
        #return reporte08(form.vars.datelimite1 , form.vars.datelimite2)
        #return reporte09(form.vars.datelimite1 ,form.vars.datelimite2 , form.vars.pto )        
    return dict(form=form)
