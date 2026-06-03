from Semestre import Semestre

class Aluno:

    def __init__(self,
                 matricula : int,
                 nome : str,
                 semestre: Semestre
                 ):

        self.matricula = matricula
        self.nome = nome
        self.id_semestre = semestre.getSemestreLetivo()

    def __repr__(self):
        return f"{self.nome} ({self.matricula})"
