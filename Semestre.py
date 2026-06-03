class Semestre:

    def __init__(self,
                 id : int,
                 semestre_letivo : int):
                 
        self.id = id
        self.semestre_letivo = semestre_letivo

    def getSemestreLetivo(self):
        return self.semestre_letivo
