class Professor:

    def __init__(self,
                 matricula : int,
                 nome : str
                 ):
                 
        self.matricula = matricula
        self.nome = nome
        self.horarios = list()
        self.horarios_bloqueados = list()
        self.dias_concentrados = None

    def setHorarios_Bloqueados(self, horarios_block : tuple):
        self.horarios_bloqueados.append(horarios_block)

    def getHorarios_Bloqueados(self):
        return self.horarios_bloqueados
    

    def setHorarios(self, horarios : list):
        self.horarios.append(horarios)

    def getHorarios(self):
        return self.horarios


    def setDias_concentrados(self, dias_concentrados : bool):
        self.dias_concentrados = dias_concentrados

    def getDias_concentrados(self):
        return self.dias_concentrados
    
    def __repr__(self):
        return f"{self.nome}"
