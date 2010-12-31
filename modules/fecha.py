import datetime

class fechas:

    def fecha_espanol(self,d):
        fecha2=d.strftime("%A %d %B %Y").split()
        if fecha2[0]=='Monday':
            dia = "Lunes"
        elif fecha2[0]=='Tuesday':
            dia = "Martes"  
        elif fecha2[0]=='Wednesday':
            dia = "Miercoles"   
        elif fecha2[0]=='Thursday':
            dia = "Jueves"      
        elif fecha2[0]=='Friday':
            dia = "Viernes"
        elif fecha2[0]=='Saturday':
            dia = "Sabado"      
        elif fecha2[0]=='Sunday':
            dia = "Domingo" 
        if fecha2[2]=='January':
            mes = "Enero"
        elif fecha2[2]=='February':
            mes = "Febrero" 
        elif fecha2[2]=='March':
            mes = "Marzo"   
        elif fecha2[2]=='April':
            mes = "Abril"       
        elif fecha2[2]=='May':
            mes = "Mayo"
        elif fecha2[2]=='June':
            mes = "Junio"       
        elif fecha2[2]=='July':
            mes = "Julio"       
        elif fecha2[2]=='August':
            mes = "Agosto"  
        elif fecha2[2]=='September':
            mes = "Setiembre"       
        elif fecha2[2]=='October':
            mes = "Octubre"
        elif fecha2[2]=='November':
            mes = "Noviembre"       
        elif fecha2[2]=='Dicember':
            mes = "Diciemre" 
        else: mes="sin mes"           
        fechita = dia+" "+fecha2[1]+" de "+mes+" de "+fecha2[3]
        return fechita
