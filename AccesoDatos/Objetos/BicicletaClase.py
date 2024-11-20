class Bicicleta:
    color = ""
    tamanio = ""
    Vel_max=15
    def __init__(self):
        self.velocidad = 0
    def subirvelocidad (self):
        self.velocidad = self.velocidad+1
    def bajarvelocidad(self):
        self.velocidad = self.velocidad - 1
    def cambiarVelMax(self,maxVel):
        self.Vel_max = maxVel


class BicicletaCarreras(Bicicleta):
    marcha=0
    def subirmarcha(self):
        self.marcha = self.marcha + 1
    def bajarmarcha(self):
        self.marcha = self.marcha + 1
