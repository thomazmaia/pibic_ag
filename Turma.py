from Aluno import Aluno

class Turma:
    def __init__(self,
                 cod : str, 
                 turno : str
                 ):
        self.cod = cod
        self.turno = turno
        self.alunos = list()

    def addAluno(self, aluno : Aluno):
        self.alunos.append(aluno)

    def __repr__(self):
        return f"{self.cod} - {self.turno}"
