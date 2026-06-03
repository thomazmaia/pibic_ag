from Aluno import Aluno
from Professor import Professor
from Sala import Sala

class Disciplina:

    def __init__(self, 
                 cod : str, 
                 semestre : int, 
                 nome : str, 
                 carga_horaria : int, 
                 e_tecnica : bool
                 ):
        
        #Definidos por parâmetros
        self.cod = cod.upper()
        self.semestre = semestre
        self.nome = nome.capitalize()
        self.carga_horaria = carga_horaria
        self.e_tecnica = e_tecnica    

        #Definidos por função
        self.horarios = list()
        self.pre_requisitos = list()
        self.professor = None
        self.alunos = list()
        self.sala = None
        

    def addHorario(self, horario : tuple):
        self.horarios.append(horario)
        print(f"Horários {horario} adicionados à disciplina {self.nome}")


    def addAluno(self, aluno : Aluno):
        self.alunos.append(aluno)
        print(f"{aluno.nome} adicionado à disciplina {self.nome}")


    def addProfessor(self, professor : Professor):
        #Prevenção caso o professor tenha um horário bloqueado que coincida com o horário da disciplina
        for horario_bloqueado in professor.getHorarios_Bloqueados():
            if horario_bloqueado in self.horarios:
                print(f"Professor {professor.nome} não pode ser adicionado neste horário!"
                      f" O horário {horario_bloqueado} está bloqueado para ele.")
                return

        #Prevençao caso a disciplina já tenha um professor atribuído
        if self.professor is not None:
            print(f"A disciplina já tem um professor atribuído: {self.professor.nome}")
            return

        self.professor = professor

        # print(f"Professor {self.professor.nome} adicionado à disciplina {self.nome}")


    def addSala(self, sala : Sala):
        if sala.laboratorio != self.e_tecnica:
            print(f"Esta sala não é adequada para {self.nome}")
            return

        self.sala = sala


    def __repr__(self):
        #Caso a disciplina não tenha um professor atribuído.
        if self.professor is None:
            professor_aux = "Sem professor"
        else:
            professor_aux = self.professor.nome
        
        if not self.alunos:
            alunos_aux = "Sem alunos"
        else:
            alunos_aux = self.alunos

        if not self.horarios:
            horarios_aux = "Sem horários"
        else:
            horarios_aux = self.horarios

        if self.sala is None:
            sala_aux = "Sem sala"
        else:
            sala_aux = self.sala.num_sala

        # Isso aqui vai ser chamado quando tu fizer "print(nome_da_disciplina)"
        
        return f"{self.nome}"
