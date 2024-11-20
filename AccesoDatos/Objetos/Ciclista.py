from BicicletaClase import BicicletaCarreras

mibici = BicicletaCarreras()
print ("Velocidad: ",mibici.velocidad)
mibici.subirmarcha()
mibici.subirmarcha()
print ("Marcha: ",mibici.marcha)
mibici.bajarmarcha()
print ("Marcha: ",mibici.marcha)
mibici.subirvelocidad()
print ("Velocidad: ",mibici.velocidad)
mibici.cambiarVelMax(25)
print ("Velocidad máxima: ",mibici.Vel_max)
