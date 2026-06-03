from Aula import Aula
from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
import random

DIAS = ["SEG", "TER", "QUA", "QUI", "SEX"]
TURNOS = {
    "M" : ["AB", "CD"],
    "T" : ["AB", "CD"],
    "N" : ["AB", "CD"],
}
 
# Restrições rígidas que faltam:
# 5. O horário do professor deve ser alocado concentrado ou não, conforme sua escolha dentro dos 4 dias restantes;
# 7. O horário de cada professor deve começar com pelo menos 20h livres;
# 8. O horário também deve atender disciplinas a serem eu cursadas por alunos concludentes;
# 10. As aulas de uma turma devem ficar concentradas numa mesma sala de aula;

class Horario:
# horario.grade["SEG"]["M"]["AB"] -> retorna um objeto do tipo Aula
# horario.grade["SEG"]["M"]["AB"].turma -> retorna um objeto Turma
# horario.grade["SEG"]["M"]["AB"].vazio() -> retorna True se o slot tiver livre    

    def __init__(self, 
                professor: Professor, 
                alocacoes: list,
                salas: list
                 ):
        self.professor = professor
        self.alocacoes = alocacoes
        self.salas = salas

        self.grade = self.inicializar_grade()
        
    def inicializar_grade(self):
        grade = {}

        for dia in DIAS:
            grade[dia] = {}

            for turno in TURNOS:
                grade[dia][turno] = {}

                for slot in TURNOS[turno]:
                    grade[dia][turno][slot] = None

        return grade
    
    def gerar_individuo_aleatorio(self):
        todas_alocacoes = self.alocacoes.copy()
        random.shuffle(todas_alocacoes)

        # Limpa a ocupacao das salas antes de gerar, evitando que slots ocupados num individuo anterior bloqueiem este.
        for sala in self.salas:
            sala.limpar_ocupacao()

        # Monta lista apenas com slots NAO bloqueados pelo professor
        bloqueados = self.professor.getHorarios_Bloqueados()
        slots_disponiveis = []

        for dia in DIAS:
            for turno in TURNOS:
                for slot in TURNOS[turno]:
                    if (dia, turno, slot) not in bloqueados:
                        slots_disponiveis.append((dia, turno, slot))

        #  embaralha os slots
        random.shuffle(slots_disponiveis)

        # Aloca cada alocacao em um slot disponivel
        for i in range(len(todas_alocacoes)):
            if i >= len(slots_disponiveis):
                print(f"Aviso: slots do professor {self.professor} insuficientes para todas as alocacoes.")
                break
 
            alocacao = todas_alocacoes[i]
            dia, turno, slot = slots_disponiveis[i]
            disciplina = alocacao[0]

            # Verifica se a disciplina já possui um professor atribuido
            if disciplina.professor is not None: 
                print(f"A disciplina {disciplina}, já possui um professor")
                continue

            # Filtra salas compativeis com o tipo da disciplina (lab ou nao)
            salas_compativeis = self.check_salas(dia, turno, slot, disciplina)

            if len(salas_compativeis) == 0:
                continue
            
            # Verifica se ontem teve aula a noite para bloquear o slot M-AB 
            dia_atual = DIAS.index(dia)
            if self.check_noite_manha(dia_atual, turno, slot):
                continue

            # Verifica se o professor já possui 6 aulas no dia atual
            if self.check_aulas_no_dia(dia) >= 6:
                continue

            sala = random.choice(salas_compativeis)
            self.grade[dia][turno][slot] = Aula(alocacao, sala)
            sala.ocupar(dia, turno, slot) # Ocupa aquela sala naquele horário
    
    def funcao_fitness(self):
        pontuacao = 0
        
        for aula in self.grade:
            pass
        # for dia in DIAS:
        #     for turno in TURNOS:
        #         for slot in TURNOS[turno]:
                    
        #             if 

    def horario_grade(self, dia, turno, slot):  # retorna um objeto do tipo Aula
        
        aula = self.grade[dia][turno][slot]
        if aula is None:
            print("Slot vazio\n")
        else:
            if aula.sala.laboratorio == True:
                print(f"Matéria: {aula.disciplina.nome}\nTurma: {aula.turma.cod}\nLaboratório: {aula.sala.num_sala}\n")
            else:
                print(f"Matéria: {aula.disciplina.nome}\nTurma: {aula.turma.cod}\nSala: {aula.sala.num_sala}\n")
    
    # Funções Auxiliares:

    def check_salas(self, dia, turno, slot, disciplina):
        salas_compativeis = []

        for sala in self.salas:

            # sala ocupada → ignora
            if sala.esta_ocupada(dia, turno, slot):
                continue

            # compatibilidade lab / não lab
            if sala.laboratorio == disciplina.e_tecnica:
                salas_compativeis.append(sala)

        return salas_compativeis

    def check_noite_manha(self, dia_atual, turno, slot):
        # Verifica se há aula de noite no dia anterior
        if turno == "M" and slot == "AB":
            if dia_atual == 0:
                pass
            else:
                dia_anterior = DIAS[dia_atual - 1]
                
                for slot in TURNOS["N"]:
                    if self.grade[dia_anterior]['N'][slot] is not None:
                        return True
        
        # Verifica se há aula de manhã no horário AB no próximo dia
        if turno == "N":
            if dia_atual < len(DIAS) - 1:
                dia_seguinte = DIAS[dia_atual + 1]

                # verifica se já existe M-AB no dia seguinte
                if self.grade[dia_seguinte]["M"]["AB"] is not None:
                    return True
        return False
    
    def check_aulas_no_dia(self, dia):
        total = 0

        for turno in TURNOS:
            for slot in TURNOS[turno]:
                if self.grade[dia][turno][slot] is not None:
                    total += 2  # cada slot vale 2 aulas

        return total
    
    def __repr__(self):
        # Cabecalho
        resultado = "\nGrade — Prof. " + self.professor.nome + "\n"
        resultado = resultado + f"{'':>8}"
        for dia in DIAS:
            resultado = resultado + f"{dia:^22}"
        resultado = resultado + "\n"
 
        # Linhas por turno e slot
        for turno in TURNOS:
            for slot in TURNOS[turno]:
                rotulo = turno + "-" + slot
                resultado = resultado + f"{rotulo:>8}"
 
                for dia in DIAS:
                    aula = self.grade[dia][turno][slot]
                    if aula is None:
                        celula = "—"
                    else:
                        celula = aula.disciplina.cod + "/" + aula.turma.cod
                    resultado = resultado + f"{celula:^22}"
 
                resultado = resultado + "\n"
 
            resultado = resultado + "\n"
 
        return resultado
