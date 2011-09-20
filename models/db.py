#Importando libreria para deteminar el dia y hora actual (timestamp)
import datetime;
import time;
timestamp=datetime.datetime.now()
now=time.time()
comision=1000.00
"""
database class object creation
"""
db = SQLDB("sqlite://db.db")

"""
Table definition
"""
db.define_table("modulo", 
      SQLField("nModulo", "string", notnull=True, default=None, label="Modulo"))

"""
Table definition
"""
db.define_table("reporte", 
      SQLField("nReporte", "string", notnull=True, default=None, label="Nombre"),
      SQLField("descripcionReporte", "string", notnull=True, default=None, label="Descripción"),
      SQLField("permisoReporte", "string", notnull=True, default=None, label="Permiso"))            

"""
Table definition
"""
db.define_table("datosEmpresa", 
      SQLField("nombre", "string",  label="Nombre de la empresa"),
      SQLField("comision", "string",  label="Comision"),
      SQLField("impuesto", "string",  label="Impuesto"),
      SQLField("fotoIzquierda", "upload",  label="Foto Izquierda"),
      SQLField("fotoDerecha", "upload",  label="Foto Derecha"),
      SQLField("telefono", "string",  label="Telefono"),
      SQLField("lugar", "string",  label="Lugar"),                  
      SQLField("pais","string", label="Pais"))            

if len(db(db.datosEmpresa.id>0).select())==0:
    db.datosEmpresa.insert(nombre='Macc Ticket')
datos=db(db.datosEmpresa.id>0).select()[0]
      
"""
Table definition
"""
db.define_table("tipoPermiso",
      SQLField("nTipoPermiso", "string", notnull=True, default=None, label="Tipo de Permiso"))


"""
Table definition
"""
db.define_table("tipoUsuario",
      SQLField("nTipoUsuario", "string", notnull=True, default=None, label="Tipo de Usuario"))


"""
Table definition
"""
db.define_table("permiso",
      SQLField("idModulo", db.modulo, label="Modulo"),
      SQLField("idTipoPermiso", db.tipoPermiso, label="Tipo de Permiso"),
      SQLField("idTipoUsuario", db.tipoUsuario, label="Tipo de Usuario"))
      
permisodado=((db.modulo.id==db.permiso.idModulo)&(db.tipoPermiso.id==db.permiso.idTipoPermiso)&(db.tipoUsuario.id==db.permiso.idTipoUsuario))


"""
Table definition
"""
db.define_table("medioEnvio",
      SQLField("nMedioEnvio", "string", notnull=True, default=None, label="Medio de Envio"),
      SQLField("descripcionMedioEnvio", "text", default=None, label="Descripcion"),
      SQLField("precioMedioEnvio", "double", notnull=True, default=None, label="Precio"))

"""
Table definition
"""
db.define_table("pais",
      SQLField("nPais", "string", notnull=True, default=None, label="Pais"))


"""
Table definition
"""
db.define_table("provincia",
      SQLField("idPais", db.pais, label="Pais"),
      SQLField("nProvincia", "string", notnull=True, default=None, label="Provincia"))

"""
Table definition
"""
db.define_table("canton",
      SQLField("idProvincia", db.provincia, label="Provincia"),
      SQLField("nCanton", "string", notnull=True, default=None, label="Canton"))      

"""
Table definition
"""
db.define_table("tipoDocumento",
      SQLField("nTipoDocumento", "string", notnull=True, default=None, label="Tipo de Documento"))


"""
Table definition
"""
db.define_table("tipoDescuento",
      SQLField("nTipoDescuento", "string", notnull=True, default=None, label="Tipo de Descuento"),
      SQLField("porcetajeTipoDescuento", "double", notnull=True, default=None, label="Porcentaje de Descuento"))


"""
Table definition
"""
db.define_table("supraTipoEvento",
      SQLField("nSupraTipoEvento", "string", notnull=True, default=None, label="Tipo de Evento"))
db.supraTipoEvento.nSupraTipoEvento.requires = [IS_NOT_EMPTY()]

"""
Table definition
"""
db.define_table("tipoEvento",
      SQLField("idSupraTipoEvento", db.supraTipoEvento, label="Supra Tipo de Evento"),
      SQLField("nTipoEvento", "string", notnull=True, default=None, label="Tipo de Evento"),
      SQLField("descripcionTipoEvento", "text", notnull=False, default=None, label="Descripcion"),
      SQLField("imagenTipoEvento", "upload", notnull=False, default=None, label="Imagen"))


"""
Table definition
"""
db.define_table("tipoTarjeta",
      SQLField("nTipoTarjeta", "string", notnull=True, default=None, label="Tipo de Tajeta"),
      SQLField("descripcionTipoTarjeta", "text", default=None, label="Descripcion"))



"""
Table definition
"""
db.define_table("medioPago",
      SQLField("nMedioPago", "string", notnull=True, default=None, label="Medio de Pago"))
      

"""
Table definition
"""
db.define_table("distrito",
      SQLField("idCanton", db.canton, label="Canton"),
      SQLField("nDistrito", "string", notnull=True, default=None, label="Distrito"),
      SQLField("codigoPostalDistrito", "string", notnull=True, default=None, label="Codigo Postal"))
  
  
"""
Table definition
"""
db.define_table("lugar",
      SQLField("nLugar", "string", notnull=True, default=None, label="Lugar"),
      SQLField("direccionLugar", "string", notnull=True, default=None, length=100, label="Direccion"),
      SQLField("idDistrito", db.distrito, label="Distrito"),
      SQLField("referenciaLugar", "text", default=None, label="Referencia"),
      SQLField("observacionesLugar", "text", default=None, label="Observaciones"),
      SQLField("fotoLugar", "upload", default=None, label="Imagen"))
      

"""
Table definition
"""
db.define_table("evento",
      SQLField("nEvento", "string", notnull=True, default=None, label="Evento"),
      SQLField("idTipoEvento", db.tipoEvento, label="Tipo de Evento"),
      SQLField("idLugar", db.lugar, label="Lugar"),
      SQLField("descripcionEvento", "text", default=None, label="Descripcion"),
      SQLField("observacionEvento", "text", default=None, label="Observaciones"),
      SQLField("fEvento", "date", notnull=True, default=None, label="Fecha"),
      SQLField("hEvento", "time", notnull=True, default=None, label="Hora"),
      SQLField("publicidadEvento", "upload", default=None, label="Flyer"),
      SQLField("distribucionAsientosEvento", "upload", default=None, label="Distribucion de Asientos"),
      SQLField("calificacion", "double", default=None, label="Calificacion"))


"""
Table definition
"""
db.define_table("zona",
      SQLField("idEvento", db.evento, label="Evento"),
      SQLField("nZona", "string", notnull=True, default=None, label="Zona"),
      SQLField("costoZona", "double", notnull=True, default=None, label="Costo de la Zona"),
      SQLField("descripcionZona", "text", notnull=True, default=None, label="Descripcion"),
      SQLField("fotoZona", "upload", notnull=True, default=None, label="Imagen"),
      SQLField("distribucionZona", "upload", default=None, label="Distribución"))      


            
"""
Table definition
"""
db.define_table("usuario",
      SQLField("aPaternoUsuario", "string", notnull=True, default=None, label="Apellido Paterno"),
      SQLField("aMaternoUsuario", "string", default=None, label="Apellido Materno"),
      SQLField("nUsuario", "string", default=None, label="Nombre"),
      SQLField("idTipoDocumento", db.tipoDocumento, label="Tipo de Documento"),
      SQLField("numeroDocumentoUsuario", "string", notnull=True, default=None, label="N Documento"),
      SQLField("direccionUsuario", "string", notnull=True, default=None, label="Direccion"),
      SQLField("idDistrito", db.distrito, label="Distrito"),
      SQLField("idTipoUsuario", db.tipoUsuario, label="Tipo de Usuario"),
      SQLField("telefonoUsuario", "string", notnull=True, default=None, label="Telefono"),
      SQLField("celularUsuario", "string", default=None, label="Celular"),
      SQLField("correoUsuario", "string", notnull=True, default=None,  requires=[IS_EMAIL(), IS_NOT_IN_DB(db,'usuario.correoUsuario')], label="Correo Electronico"),
      SQLField("fNacimientoUsuario", "date", notnull=True, default=None, label="Fecha de Nacimiento"),
      SQLField("claveUsuario", "password", notnull=True, default=None, label="Contraseña"),
      SQLField("activoUsuario", "boolean", notnull=True, default=None, label="Actividad"),
      SQLField("fInscripcionUsuario", "datetime", notnull=True, default=timestamp, label="Fecha de Inscripcion"),
      SQLField("verificacionUsuario",default='', label="Verificacion de Usuario"),
      SQLField("ultimoIntentoUsuario",'integer',default=0, label="Ultimo Intento de Acceso"),
      SQLField("intentoFallidosUsuario",'integer',default=0, label="Intentos Fallidos de Acceso"))

db.define_table('incidente',
                SQLField('ctime','integer',default=now),
                SQLField('url'),
                SQLField('codigo'),
                SQLField('usuario',db.usuario))


"""
Table definition
"""
db.define_table("puntoVenta",
      SQLField("nPuntoVenta", "string", notnull=True, default=None, label="Punto de Venta"),
      SQLField("direccionPuntoVenta", "string", notnull=True, default=None, label="Direccion"),
      SQLField("referenciaPuntoVenta", "text", default=None, label="Referencia"),
      SQLField("observacionPuntoVenta", "text", default=None, label="Observaciones"),
      SQLField("idDistrito", db.distrito, label="Distrito"),
      SQLField("fotoPuntoVenta", "upload", notnull=False, default=None, label="Imagen"),
      SQLField("activoPuntoVenta", "boolean", notnull=False, default=True, label="Activo"),
      )


"""
Table definition
"""
db.define_table("asiento",
      SQLField("FilaAsiento", notnull=True, default=None, label="Fila"),
      SQLField("numeroAsiento", "integer", notnull=True, default=None, label="Numero de Asiento"),
      SQLField("idZona", db.zona, label="Zona"),
      SQLField("estadoAsiento", "integer", notnull=True, default=None, label="Estado del Asiento"),
      SQLField("fechaCambioEstadoAsiento", "datetime", notnull=True, default=timestamp, label="Ultima Actualizacion"),
      SQLField("idUsuario", db.usuario, label="Usuario"))


"""
Table definition
"""
db.define_table("asistencia",
      SQLField("idPuntoVenta", db.puntoVenta, label="Punto de Venta"),
      SQLField("idUsuario", db.usuario, label="Usuario"),
      SQLField("fAsistencia", "date", notnull=True, default=None, label="Fecha de Asistencia"),
      SQLField("hIngreso", "time", notnull=True, default=None, label="Hora de Ingreso"),
      SQLField("hSalida", "time", notnull=True, default=None, label="Hora de Salida"),
      SQLField("hSalidaRefrigerio", "time", notnull=True, default=None, label="Salida a Refrigerio"),
      SQLField("hIngresoRefrigerio", "time", notnull=True, default=None, label="Ingreso de Refrigerio"),
      SQLField("hSalidaAdicional", "time", notnull=True, default=None, label="Salida Adicional"),
      SQLField("hIngresoAdicional", "time", notnull=True, default=None, label="Ingreso Adicional"))


"""
Table definition
"""
db.define_table("campana",
      SQLField("nCampana", "string", notnull=True, default=None, label="Campaña"),
      SQLField("descripcionCampana", "text", default=None, label="Descripcion"),
      SQLField("fInicioCampana", "date", notnull=True, default=None, label="Fecha de Incio"),
      SQLField("fFinCampana", "date", notnull=True, default=None, label="Fecha de Finalizacion"),
      SQLField("observacionCampana", "text", default=None, label="Observacion"),
      SQLField("idTipoDescuento", db.tipoDescuento, label="Tipo de Descuento"),
      SQLField("idTipoTarjeta", db.tipoTarjeta, label="Tipo de Tarjeta"),
      SQLField("idMedioPago", db.medioPago, label="Medio de Pago"),
      SQLField("idEvento", db.evento, label="Evento"))


"""
Table definition
"""
db.define_table("ticket",
      SQLField("direccionTicket", "string", notnull=True, default=None, label="Direccion de Envio"),
      SQLField("comisionVentaTicket", "double", notnull=True, default=comision, label="Comision de Venta"),
      SQLField("montoTotalTicket", "double", notnull=True, default=None, label="Monto Total"),
      SQLField("imprimioTicket", "boolean", notnull=True, default=None, label="Impresion"),
      SQLField("hashTicket", "string", default=None, label="Codigo de Seguridad"),
      SQLField("codigoOperacionTicket", "string", default=None, label="Codigo de Operacaion"),
      SQLField("fVentaTicket", "datetime", notnull=True, default=timestamp, label="Fecha de Venta"),
      SQLField("fEntregaTicket", "date", notnull=True, default=None, label="Fecha de Entrega"),
      SQLField("idAsiento", db.asiento, label="Numero de Asiento"),
      SQLField("idMedioEnvio", db.medioEnvio, label="Medio de Envio"),
      SQLField("idCampana", db.campana, label="Campaña"),
      SQLField("numeroTarjetaTicket", "string", notnull=False, default=None, label="N Tarjeta"),
      SQLField("pinTicket", "string", default=None, label="Pin"),
      SQLField("observaciones", "string",  default=None, label="observaciones"),      
      SQLField("idTipoTarjeta", db.tipoTarjeta, label="Tipo de Tarjeta"),
      SQLField("idMedioPago", db.medioPago, label="Medio de Pago"),
      SQLField("idDistrito", db.distrito, label="Distrito"),
      SQLField("idCliente", db.usuario, label="Cliente"),
      SQLField("idVendedor", db.usuario, label="Vendedor"),
      SQLField("idPuntoVenta", db.puntoVenta, label="Punto de Venta"))
            


"""
Relations between tables (remove fields you don't need from requires)
"""
db.permiso.idModulo.requires=IS_IN_DB(db, 'modulo.id','%(nModulo)s')
db.permiso.idTipoPermiso.requires=IS_IN_DB(db, 'tipoPermiso.id','%(nTipoPermiso)s')
db.permiso.idTipoUsuario.requires=IS_IN_DB(db, 'tipoUsuario.id','%(nTipoUsuario)s')
db.asiento.idZona.requires=IS_IN_DB(db, 'zona.id','%(nZona)s')
db.asiento.idUsuario.requires=IS_IN_DB(db, 'usuario.id','%(aPaternoUsuario)s %(aMaternoUsuario)s, %(nUsuario)s - %(correoUsuario)s')
db.asistencia.idPuntoVenta.requires=IS_IN_DB(db, 'puntoVenta.id','%(nPuntoVenta)s')
db.asistencia.idUsuario.requires=IS_IN_DB(db, 'usuario.id','%(aPaternoUsuario)s %(aMaternoUsuario)s, %(nUsuario)s - %(correoUsuario)s')
db.campana.idTipoDescuento.requires=IS_IN_DB(db, 'tipoDescuento.id','%(nTipoDescuento)s')
db.campana.idTipoTarjeta.requires=IS_IN_DB(db, 'tipoTarjeta.id','%(nTipoTarjeta)s')
db.campana.idMedioPago.requires=IS_IN_DB(db, 'medioPago.id','%(nMedioPago)s')
db.campana.idEvento.requires=IS_IN_DB(db, 'evento.id','%(nEvento)s')
db.canton.idProvincia.requires=IS_IN_DB(db, 'provincia.id','%(nProvincia)s')
db.tipoEvento.idSupraTipoEvento.requires=IS_IN_DB(db, 'supraTipoEvento.id','%(nSupraTipoEvento)s')
db.evento.idTipoEvento.requires=IS_IN_DB(db, 'tipoEvento.id','%(nTipoEvento)s')
db.evento.idLugar.requires=IS_IN_DB(db, 'lugar.id','%(nLugar)s')
db.lugar.idDistrito.requires=IS_IN_DB(db, 'distrito.id','%(nDistrito)s')
db.provincia.idPais.requires=IS_IN_DB(db, 'pais.id','%(nPais)s')
db.puntoVenta.idDistrito.requires=IS_IN_DB(db, 'distrito.id','%(nDistrito)s')
db.ticket.idAsiento.requires=IS_IN_DB(db, 'asiento.id','%(numeroAsiento)s')
db.ticket.idMedioEnvio.requires=IS_IN_DB(db, 'medioEnvio.id','%(nMedioEnvio)s')
db.ticket.idCampana.requires=IS_IN_DB(db, 'campana.id','%(nCampana)s')
db.ticket.idTipoTarjeta.requires=IS_IN_DB(db, 'tipoTarjeta.id','%(nTipoTarjeta)s')
db.ticket.idMedioPago.requires=IS_IN_DB(db, 'medioPago.id','%(nMedioPago)s')
db.ticket.idDistrito.requires=IS_IN_DB(db, 'distrito.id','%(nDistrito)s')
db.ticket.idPuntoVenta.requires=IS_IN_DB(db, 'puntoVenta.id','%(nPuntoVenta)s')
db.ticket.idCliente.requires=IS_IN_DB(db, 'usuario.id','%(aPaternoUsuario)s %(aMaternoUsuario)s, %(nUsuario)s - %(correoUsuario)s')
db.ticket.idVendedor.requires=IS_IN_DB(db, 'usuario.id','%(aPaternoUsuario)s %(aMaternoUsuario)s, %(nUsuario)s - %(correoUsuario)s')
db.distrito.idCanton.requires=IS_IN_DB(db, 'canton.id','%(nCanton)s')
db.usuario.idTipoDocumento.requires=IS_IN_DB(db, 'tipoDocumento.id','%(nTipoDocumento)s')
db.usuario.idDistrito.requires=IS_IN_DB(db, 'distrito.id','%(nDistrito)s')
db.usuario.idTipoUsuario.requires=IS_IN_DB(db, 'tipoUsuario.id','%(nTipoUsuario)s')
db.usuario.claveUsuario.requires = [
    IS_NOT_EMPTY(error_message='Campo obligatorio'),
    CRYPT()]
db.zona.idEvento.requires=IS_IN_DB(db, 'evento.id','%(nEvento)s')

