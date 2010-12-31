import md5, random, time, datetime

timestamp=datetime.datetime.now()

response.title='Sistema de Venta de Tickets'
response.view='cas/generic.html'
DT=300

if request.vars.service: session.service=request.vars.service
if not session.service: session.service=URL(r=request,f='login')
if not session.ctime: session.ctime=0
if session.ctime<now-DT and request.function in ['change_password','edit_profile']:
    redirect(URL(r=request,f='logout'))
else:
    session.ctime=now    

def index():
    if session.incidente:
        return dict(form=B("Bienvenido %(name)s" % {'name':session.usuario_name}))
    else:
        return dict(form=B("Usted no ha podido ingresar"))

def insert_incidente(session):
    db(db.incidente.url==session.service)\
      (db.incidente.usuario==session.idUsuario).delete()
    db.incidente.insert(codigo=session.incidente,usuario=session.idUsuario,
                     url=session.service,ctime=now)

def login(): 
    response.menu=menu_out
    if request.vars.service and session.incidente and session.ctime>now-DT:
        insert_incidente(session)
        redirect(session.service+"?incidente="+session.incidente)
    form=FORM(TABLE(TR("Correo:",INPUT(_name="email",requires=IS_NOT_EMPTY())),
                    TR("Contraseña:",INPUT(_name="password",_type='password',
                                         requires=[IS_NOT_EMPTY(),CRYPT()])),
                    TR("",INPUT(_type="submit",_value="login"))))
    if form.accepts(request.vars,session):
        r=db(db.usuario.correoUsuario==form.vars.email)\
            (db.usuario.claveUsuario==form.vars.password)\
            (db.usuario.verificacionUsuario=='')\
             .select()
        if len(r)>0:
            session.idUsuario=r[0].id
            session.usuario_name=r[0].nUsuario
            session.usuario_email=form.vars.email
            session.incidente=str(time.time()*random.random())
            session.ctime=now
            session.tipoUsuario=r[0].idTipoUsuario
            session.flash='Usuario Logeado'
            insert_incidente(session)
            redirect(session.service+"?incidente="+session.incidente)
        else:
            time.sleep(2)
            response.flash='Inicio de Sesion Invalido'
    if form.errors:
        response.flash='Inicio de Sesion Invalido'
    return dict(form=form)

def check():
    response.headers['Content-Type']='text'
    rows=db(db.incidente.url==request.vars.service)\
           (db.incidente.codigo==request.vars.incidente)\
           (db.incidente.ctime>now-60)\
           (db.incidente.usuario==db.usuario.id).select()    
    if len(rows):
        usuario=rows[0].usuario
        return 'yes\n%s:%s:%s'%(usuario.id,usuario.correoUsuario,usuario.nUsuario)
    return 'no\n'

def logout():
    response.menu=menu_out
    session.incidente=None
    session.tipoUsuario=None
    response.flash="Sesion Finalizada"
    return dict(form=B("Hasta Pronto, %(name)s" % {'name':session.usuario_name}))

def register():
    form=FORM(TABLE(TR("Apellido Paterno:",\
          INPUT(_name="paterno",requires=IS_NOT_EMPTY())),TR("Apellido Materno:",\
          INPUT(_name="materno",requires=IS_NOT_EMPTY())),TR("Nombres:",\
          INPUT(_name="name",requires=IS_NOT_EMPTY())),TR("Tipo de Docuemento:",\
          SELECT(_type="select", _name="distrito",*[OPTION(x.nTipoDocumento,_value=x.id)
           for x in db().select(db.tipoDocumento.ALL)])),TR("N Documento:",\
          INPUT(_name="nDocumento",requires=IS_NOT_EMPTY())),TR("Direccion:",\
          INPUT(_name="direccion",requires=IS_NOT_EMPTY())),TR("Distrito:",\
          SELECT(_type="select", _name="distrito",*[OPTION(x.nDistrito,_value=x.id)
           for x in db().select(db.distrito.id, db.distrito.nDistrito)])),TR("Telefono:",\
          INPUT(_name="telefono",requires=IS_NOT_EMPTY())),TR("Celular:",\
          INPUT(_name="celular",requires=IS_NOT_EMPTY())),TR("Fecha de Nacimiento:",\
          INPUT(_name="birth",_class='date',_id="birth",requires=[IS_NOT_EMPTY(), IS_DATE('%Y-%m-%d')])),TR("Correo Electronico:",\
          INPUT(_name="email",requires=[IS_NOT_EMPTY(), IS_EMAIL(),\
             IS_NOT_IN_DB(db,'usuario.correoUsuario')])),\
                    TR("Contraseña:",\
          INPUT(_name="password",_type='password',requires=[IS_NOT_EMPTY(),CRYPT()])),\
                    TR("Contraseña (nuevamente):",\
          INPUT(_name="password2",_type='password',requires=[IS_NOT_EMPTY(),CRYPT()])),\
                    TR("",INPUT(_type="submit",_value="register"))))                    
    if form.accepts(request.vars,session) and \
       form.vars.password==form.vars.password2:
        key=md5.new(str(random.randint(0,9999))).hexdigest()
        id=db.usuario.insert(aPaternoUsuario=form.vars.paterno,
                          aMaternoUsuario=form.vars.materno,
                          nUsuario=form.vars.name,
                          idTipoDocumento=form.vars.tipoDocuemento,
                          numeroDocumentoUsuario=form.vars.nDocumento,
                          direccionUsuario=form.vars.direccion,
                          idTipoUsuario=2,
                          telefonoUsuario=form.vars.telefono,
                          celularUsuario=form.vars.celular,
                          fNacimientoUsuario=form.vars.birth,
                          fInscripcionUsuario=timestamp,
                          correoUsuario=form.vars.email,
                          claveUsuario=form.vars.password,
                          activoUsuario=0,
                          verificacionUsuario=key)
        message="Para completar su registro visite: %s?id=%s&key=%s"%(CAS.verify_url,id,key) 
        try:
            #session.flash=message
            email(EMAIL_SENDER,form.vars.email,'Registro Maccticket',message)
            session.flash="Se le ha Enviado un Correo Electronico"
            redirect(URL(r=request,f='login'))
        except Exception:
            print message
            response.flash="Error Interno, no se ha podido enviar el correo electronico"
    elif form.vars.password!=form.vars.password2:
        form.errors.password2='Las contraseñas no coinciden'
        response.flash="Form error"
    return dict(form=form)

def verify():
    id=request.vars.id
    key=request.vars.key
    r=db(db.usuario.id==id)\
        (db.usuario.verificacionUsuario==key)\
        .select()
    if len(r)==0: raise HTTP(400,'pagina no existe')
    r[0].update_record(verificacionUsuario='')
    session.incidente=str(time.time()*random.random())
    session.idUsuario=r[0].id
    session.usuario_name=r[0].nUsuario
    session.usuario_email=r[0].correoUsuario
    session.ctime=now
    insert_incidente(session)
    if r[0].claveUsuario=='':
        session.flash='Debe cambiar su contraseña'
        redirect(URL(r=request,f="change_password"))
    else: session.flash='Registro Exitoso'
    redirect(session.service)

def retrieve():
    form=FORM(TABLE(TR("Correo Electronico:",INPUT(_name="email",requires=[IS_NOT_EMPTY(),IS_IN_DB(db,'usuario.correoUsuario')])),
                    TR("",INPUT(_type="submit",_value="retrieve"))))    
    if form.accepts(request.vars,session):
        r=db(db.usuario.correoUsuario==form.vars.email).select()
        if len(r):
            key=md5.new(str(random.randint(0,9999))).hexdigest()
            id=r[0].id
            r[0].update_record(claveUsuario='',verificacionUsuario=key)
            message="Para cambiar su contraseña visite: %s?id=%s&key=%s"%(CAS.verify_url,id,key) 
            try:
                email(EMAIL_SENDER,form.vars.email,'Registro Maccticket',message)
                #session.flash=message
                session.flash="Se le ha Enviado un Correo Electronico"            
                redirect(URL(r=request,f='login'))                
            except Exception:
                print message
                response.flash="Error Interno, no se pudo enviar el correo"
        else:
            form.errors.email='El correo no se encuentra registrado'
            response.flash="Form error"
    return dict(form=form)

def change_password():
    if not session.incidente: redirect(URL(r=request,f='login'))
    form=FORM(TABLE(TR("Contraseña:",INPUT(_name="password",_type='password',requires=[IS_NOT_EMPTY(),CRYPT()])),
                    TR("Contraseña (nuevamente):",INPUT(_name="password2",_type='password',requires=[IS_NOT_EMPTY(),CRYPT()])),
                    TR("",INPUT(_type="submit",_value="Registrar"))))    
    if form.accepts(request.vars,session) and \
       form.vars.password==form.vars.password2:
        db(db.usuario.id==session.idUsuario).update(claveUsuario=form.vars.password)
        session.flash='Contraseña Actualizada'
        redirect(session.service)
    elif form.vars.password!=form.vars.password2:
        form.errors.passwords2='Las Contraseñas no coinciden'
        response.flash="Form error"
    return dict(form=form)


def edit_profile():
    if not session.incidente: redirect(URL(r=request,f='login'))
    usuario=db(db.usuario.id==session.idUsuario).select()[0]
    form=SQLFORM(db.usuario,usuario,fields=['aPaternoUsuario', 'aMaternoUsuario', 'nUsuario', 'idTipoDocumento','numeroDocumentoUsuario', 'direccionUsuario',
     'idDistrito', 'telefonoUsuario', 'celularUsuario', 'fNacimientoUsuario', 'correoUsuario'],showid=False)
    if form.accepts(request.vars,session):
        session.flash='Perfil actualizado'
        redirect(session.service)
    return dict(form=form)
