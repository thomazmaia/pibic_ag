from Disciplina import Disciplina
from Turma import Turma
from Sala import Sala

class Aula:

    def __init__(self,
                 alocacao : tuple, 
                 sala : Sala
                 ):
        
        # alocacao -> tuple[Disciplina, Turma]
        self.disciplina = alocacao[0]
        self.turma = alocacao[1]
        self.sala = sala

    def vazio(self):
            return self.disciplina is None        

    def __repr__(self):
        return f"{self.disciplina} | {self.turma} | {self.sala}"
