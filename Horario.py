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

        for sala in self.salas:
            sala.limpar_ocupacao()

        # RR7
        if not self.check_horas_livres_minimas():
            print(f"{self.professor.nome} excedeu o limite de horários bloqueados.")
            return

        todas_alocacoes = self.alocacoes.copy()

        # MAIS IMPORTANTE:
        # ordena disciplinas maiores primeiro
        todas_alocacoes.sort(
            key=lambda x: x[0].carga_horaria,
            reverse=True
        )

        bloqueados = self.professor.getHorarios_Bloqueados()

        for alocacao in todas_alocacoes:

            disciplina = alocacao[0]

            carga = disciplina.carga_horaria

            aulas_alocadas = 0

            tentativas = []

            # gera TODOS os slots possíveis
            for dia in DIAS:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:

                        tentativas.append((dia, turno, slot))

            random.shuffle(tentativas)

            for dia, turno, slot in tentativas:

                if aulas_alocadas >= carga:
                    break

                # ocupado
                if self.grade[dia][turno][slot] is not None:
                    continue

                # bloqueado
                if (dia, turno, slot) in bloqueados:
                    continue

                # RR11
                dia_atual = DIAS.index(dia)

                if self.check_noite_manha(dia_atual, turno, slot):
                    continue

                # RR10
                if self.check_aulas_no_dia(dia) >= 6:
                    continue

                salas_compativeis = self.check_salas(
                    dia,
                    turno,
                    slot,
                    disciplina
                )

                if len(salas_compativeis) == 0:
                    continue

                sala = random.choice(salas_compativeis)

                self.grade[dia][turno][slot] = Aula(alocacao, sala)

                sala.ocupar(dia, turno, slot)

                aulas_alocadas += 1

            if aulas_alocadas < carga:

                print(
                    f"Não foi possível alocar completamente "
                    f"{disciplina.nome}"
                )
    
    # Funções Auxiliares:

    def check_horas_livres_minimas(self):

        bloqueados = self.professor.getHorarios_Bloqueados()

        horas_bloqueadas = 0

        for dia, turno, slot in bloqueados:

            if turno in ["M", "T"]:
                horas_bloqueadas += 2

        return horas_bloqueadas <= 20

    def horario_grade(self, dia, turno, slot):  # retorna um objeto do tipo Aula
        
        aula = self.grade[dia][turno][slot]
        if aula is None:
            print("Slot vazio\n")
        else:
            if aula.sala.laboratorio == True:
                print(f"Matéria: {aula.disciplina.nome}\nTurma: {aula.turma.cod}\nLaboratório: {aula.sala.num_sala}\n")
            else:
                print(f"Matéria: {aula.disciplina.nome}\nTurma: {aula.turma.cod}\nSala: {aula.sala.num_sala}\n")

    def get_indices_dias_utilizados(self):
        dias_utilizados = set()

        for indice_dia, dia in enumerate(DIAS):

            possui_aula = False

            for turno in TURNOS:
                for slot in TURNOS[turno]:

                    aula = self.grade[dia][turno][slot]

                    if aula is not None:
                        possui_aula = True
                        break

                if possui_aula:
                    break

            if possui_aula:
                dias_utilizados.add(indice_dia)

        return sorted(dias_utilizados)
    
    def check_dias_concentrados(self):

        dias_utilizados = self.get_indices_dias_utilizados()

        # 0 ou 1 dia sempre é concentrado
        if len(dias_utilizados) <= 1:
            return True

        # verifica buracos
        for i in range(len(dias_utilizados) - 1):

            atual = dias_utilizados[i]
            proximo = dias_utilizados[i + 1]

            if proximo - atual > 1:
                return False

        return True

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
