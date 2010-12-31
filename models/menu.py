menu_admin=[
    ['Mantenimiento',request.function=='todos',URL(r=request,c='principal',f='todos')],
    ['Asientos',request.function=='evento',URL(r=request,c='asiento',f='evento')],
    ['Reportes',request.function=='evento',URL(r=request,c='reporte',f='index')],    
    ['Editar Perfil',request.function=='edit_profile',URL(r=request,c='cas',f='edit_profile')],
    ['Contraseña',request.function=='change_password',URL(r=request,c='cas',f='change_password')],
    ['Salir',request.function=='logout',URL(r=request,c='default',f='logout')]
    ]

menu_web=[
    ['Comprar Tickets',request.function=='index',URL(r=request,c='ventaWeb',f='index')],
    ['Editar Perfil',request.function=='edit_profile',URL(r=request,c='cas',f='edit_profile')],
    ['Cambiar Contraseña',request.function=='change_password',URL(r=request,c='cas',f='change_password')],
    ['Salir',request.function=='logout',URL(r=request,c='default',f='logout')]
    ]

menu_sell=[
    ['Venta Call Center',request.function=='index',URL(r=request,c='ventaPhone',f='buscar')],
    ['Venta POS',request.function=='index',URL(r=request,c='ventaPOS',f='buscar')], 
    ['Editar Perfil',request.function=='edit_profile',URL(r=request,c='cas',f='edit_profile')],
    ['Cambiar Contraseña',request.function=='change_password',URL(r=request,c='cas',f='change_password')],
    ['Salir',request.function=='logout',URL(r=request,c='default',f='logout')]
    ]

menu_prom=[
    ['Reportes',request.function=='evento',URL(r=request,c='reporte',f='index')],    
    ['Editar Perfil',request.function=='edit_profile',URL(r=request,c='cas',f='edit_profile')],
    ['Cambiar Contraseña',request.function=='change_password',URL(r=request,c='cas',f='change_password')],
    ['Salir',request.function=='logout',URL(r=request,c='default',f='logout')]
    ]

menu_out=[
    ['Iniciar Sesion',request.function=='login',URL(r=request,c='default',f='login')],
    ['Registrarse',request.function=='register',URL(r=request,c='cas',f='register')],
    ['Recuperar Contraseña',request.function=='retrieve',URL(r=request,c='cas',f='retrieve')]
    ]



if session.tipoUsuario==1:
    response.menu=menu_admin
elif session.tipoUsuario==2:
    response.menu=menu_web
elif session.tipoUsuario==3:
    response.menu=menu_sell  
elif session.tipoUsuario==4:
    response.menu=menu_prom    
else:
    response.menu=menu_out
