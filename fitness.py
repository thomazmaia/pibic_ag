# =============================================================================
# fitness.py
# =============================================================================
# A função fitness é o "juiz" do algoritmo genético.
# Ela recebe um indivíduo (que é uma lista de grades de todos os professores)
# e devolve um número chamado "pontuação de punição".
#
# Regra principal:
#   - Quanto MENOR a pontuação, MELHOR é o horário.
#   - Uma pontuação 0 significa que nenhuma restrição foi violada.
#
# Como funciona:
#   Percorremos todas as grades de todos os professores e verificamos
#   se alguma regra foi quebrada. Para cada regra quebrada, somamos
#   uma pontuação de punição. No final, retornamos a soma total.
# =============================================================================

from Horario import DIAS, TURNOS

# -----------------------------------------------------------------------------
# Pesos de punição
# Cada número representa o "quanto prejudica" violar aquela restrição.
# Restrições rígidas (obrigatórias) têm peso alto: 10
# Restrições flexíveis (desejáveis) têm pesos menores.
# -----------------------------------------------------------------------------

PESO_RIGIDA = 50   # viola uma regra obrigatória
PESO_FLEX_1 =  5   # mesma turma em slots seguidos com o mesmo professor
PESO_FLEX_2 =  3   # mais de 2 aulas da mesma turma no mesmo dia
PESO_FLEX_3 =  3   # horário livre não priorizado no início da manhã ou fim da tarde
PESO_FLEX_4 =  1   # tarde ou noite preenchida antes da manhã
PESO_FLEX_5 =  4   # janela (buraco) no horário do professor
PESO_FLEX_6 =  2   # As aulas de uma turma devem ficar concentradas numa mesma sala de aula;


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def calcular_fitness(grades):
    """
    Recebe uma lista de objetos Horario (um por professor)
    e retorna a pontuação total de punições.

    Quanto menor o número retornado, melhor é o horário.
    """

    pontuacao = 0

    # --- Restrições rígidas (obrigatórias) ---
    pontuacao = pontuacao + rigida_sala_dupla_ocupacao(grades)
    pontuacao = pontuacao + rigida_turma_em_dois_lugares(grades)
    pontuacao = pontuacao + rigida_disciplina_professor_unico(grades)
    pontuacao = pontuacao + rigida_dias_concentrados(grades)
    pontuacao = pontuacao + rigida_horario_bloqueado(grades)
    pontuacao = pontuacao + rigida_sala_incompativel(grades)
    pontuacao = pontuacao + rigida_max_aulas_por_dia(grades)
    pontuacao = pontuacao + rigida_noite_manha(grades)

    # caso uma aula prevista pela carga horária não tenha sido alocada, é uma violação grave
    pontuacao = pontuacao + rigida_aulas_nao_alocadas(grades)

    # --- Restrições flexíveis (desejáveis) ---
    pontuacao = pontuacao + flex1_aulas_seguidas_mesma_turma(grades)
    pontuacao = pontuacao + flex2_muitas_aulas_mesma_turma_no_dia(grades)
    pontuacao = pontuacao + flex3_horarios_livres_posicao(grades)
    pontuacao = pontuacao + flex4_manha_antes_tarde_noite(grades)
    pontuacao = pontuacao + flex5_janela_no_horario(grades)
    pontuacao = pontuacao + flex6_mesma_sala_turma(grades)

    return pontuacao


# =============================================================================
# RESTRIÇÕES RÍGIDAS
# Cada função abaixo verifica UMA regra obrigatória.
# Se a regra for violada, somamos PESO_RIGIDA (10) por cada violação.
# =============================================================================

def rigida_sala_dupla_ocupacao(grades): # RR8
    """
    Regra: Duas aulas não podem acontecer na mesma sala ao mesmo tempo.

    Como verificamos:
    Para cada slot (dia + turno + slot), olhamos as grades de todos os
    professores e coletamos quais salas estão sendo usadas naquele momento.
    Se a mesma sala aparecer mais de uma vez, há conflito.
    """
    pontuacao = 0

    for dia in DIAS:
        for turno in TURNOS:
            for slot in TURNOS[turno]:

                # Coleta os números das salas usadas neste slot por todos os professores
                salas_em_uso = list()

                for horario in grades:
                    aula = horario.grade[dia][turno][slot]
                    if aula is not None:
                        salas_em_uso.append(aula.sala.num_sala)

                # Verifica duplicatas: compara cada sala com todas as outras
                for i in range(len(salas_em_uso)):
                    for j in range(i + 1, len(salas_em_uso)):
                        if salas_em_uso[i] == salas_em_uso[j]:
                            pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao


def rigida_turma_em_dois_lugares(grades):
    """
    Regra: Uma turma não pode ter duas aulas ao mesmo tempo
    (com professores diferentes).

    Como verificamos:
    Para cada slot, olhamos as grades de todos os professores e coletamos
    quais turmas estão tendo aula. Se a mesma turma aparecer mais de uma
    vez, ela estaria em dois lugares ao mesmo tempo — impossível.
    """
    pontuacao = 0

    for dia in DIAS:
        for turno in TURNOS:
            for slot in TURNOS[turno]:

                turmas_em_aula = list()

                for horario in grades:
                    aula = horario.grade[dia][turno][slot]
                    if aula is not None:
                        turmas_em_aula.append(aula.turma.cod)

                for i in range(len(turmas_em_aula)):
                    for j in range(i + 1, len(turmas_em_aula)):
                        if turmas_em_aula[i] == turmas_em_aula[j]:
                            pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao

def rigida_disciplina_professor_unico(grades):
    """
    Regra:
    Uma disciplina deve pertencer a apenas um professor.
    """

    pontuacao = 0

    professores_por_disciplina = {}

    for horario in grades:

        professor = horario.professor.nome

        for dia in DIAS:
            for turno in TURNOS:
                for slot in TURNOS[turno]:

                    aula = horario.grade[dia][turno][slot]

                    if aula is not None:

                        cod_disciplina = aula.disciplina.cod

                        if cod_disciplina not in professores_por_disciplina:
                            professores_por_disciplina[cod_disciplina] = set()

                        professores_por_disciplina[cod_disciplina].add(professor)

    for disciplina in professores_por_disciplina:

        if len(professores_por_disciplina[disciplina]) > 1:
            pontuacao += PESO_RIGIDA

    return pontuacao

def rigida_dias_concentrados(grades):

    pontuacao = 0

    for horario in grades:

        if not horario.professor.getDias_concentrados():
            continue

        dias_utilizados = []

        for i, dia in enumerate(DIAS):

            possui_aula = False

            for turno in TURNOS:
                for slot in TURNOS[turno]:

                    if horario.grade[dia][turno][slot] is not None:
                        possui_aula = True
                        break

                if possui_aula:
                    break

            if possui_aula:
                dias_utilizados.append(i)

        dias_utilizados.sort()

        for i in range(len(dias_utilizados) - 1):

            atual = dias_utilizados[i]
            prox = dias_utilizados[i + 1]

            if prox - atual > 1:
                pontuacao += PESO_RIGIDA

    return pontuacao

def rigida_horario_bloqueado(grades):
    """
    Regra: Professor não pode dar aula em horário que ele bloqueou.

    Isso já é evitado na geração aleatória, mas o crossover e a mutação
    podem quebrar essa regra acidentalmente. Por isso verificamos aqui.
    """
    pontuacao = 0

    for horario in grades:
        bloqueados = horario.professor.getHorarios_Bloqueados()

        for dia in DIAS:
            for turno in TURNOS:
                for slot in TURNOS[turno]:
                    aula = horario.grade[dia][turno][slot]
                    if aula is not None:
                        if (dia, turno, slot) in bloqueados:
                            pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao


def rigida_sala_incompativel(grades):
    """
    Regra: Disciplinas técnicas (e_tecnica=True) devem ficar em laboratório.
           Disciplinas comuns (e_tecnica=False) devem ficar em sala normal.
    """
    pontuacao = 0

    for horario in grades:
        for dia in DIAS:
            for turno in TURNOS:
                for slot in TURNOS[turno]:
                    aula = horario.grade[dia][turno][slot]
                    if aula is not None:
                        if aula.sala.laboratorio != aula.disciplina.e_tecnica:
                            pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao


def rigida_max_aulas_por_dia(grades):
    """
    Regra: Um professor não pode ter mais de 6 aulas em um mesmo dia.
    Como cada slot representa 2 aulas (par AB, CD...), o limite é 3 slots por dia.
    """
    LIMITE_SLOTS = 3

    pontuacao = 0

    for horario in grades:
        for dia in DIAS:

            slots_com_aula = 0

            for turno in TURNOS:
                for slot in TURNOS[turno]:
                    if horario.grade[dia][turno][slot] is not None:
                        slots_com_aula = slots_com_aula + 1

            if slots_com_aula > LIMITE_SLOTS:
                pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao


def rigida_noite_manha(grades):
    """
    Regra: Professor que dá aula à noite não pode dar aula no M-AB
    do dia seguinte (precisa de pelo menos 20h de descanso entre turnos).

    Verificamos: se o professor tem aula na noite de um dia E no M-AB
    do dia seguinte, é uma violação.
    """
    pontuacao = 0

    for horario in grades:
        for i in range(len(DIAS) - 1):
            dia_atual   = DIAS[i]
            dia_seguinte = DIAS[i + 1]

            # Verifica se há qualquer aula à noite no dia atual
            tem_aula_noite = False
            for slot in TURNOS["N"]:
                if horario.grade[dia_atual]["N"][slot] is not None:
                    tem_aula_noite = True

            # Verifica se há aula no M-AB do dia seguinte
            tem_aula_manha_ab = horario.grade[dia_seguinte]["M"]["AB"] is not None

            if tem_aula_noite and tem_aula_manha_ab:
                pontuacao = pontuacao + PESO_RIGIDA

    return pontuacao

def rigida_aulas_nao_alocadas(grades):
    """
    Regra:
    Todas as aulas previstas pela carga horária
    devem ser alocadas.

    Se faltarem slots, aplica punição.
    """

    pontuacao = 0

    for horario in grades:

        for alocacao in horario.alocacoes:

            disciplina = alocacao[0]

            # Quantos slots deveriam existir
            slots_necessarios = disciplina.carga_horaria // 2

            # Quantos slots realmente existem
            slots_alocados = 0

            for dia in DIAS:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:

                        aula = horario.grade[dia][turno][slot]

                        if aula is not None:

                            if aula.disciplina.cod == disciplina.cod:
                                slots_alocados += 1

            # Quantos faltaram
            faltando = slots_necessarios - slots_alocados

            if faltando > 0:

                # punição por slot faltando
                pontuacao += faltando * PESO_RIGIDA

    return pontuacao

# =============================================================================
# RESTRIÇÕES FLEXÍVEIS
# Cada função abaixo verifica UMA regra desejável (não obrigatória).
# Se a regra não for seguida, somamos uma punição menor.
# =============================================================================

def flex1_aulas_seguidas_mesma_turma(grades):
    """
    Regra flexível: Evitar dois slots seguidos da mesma turma com o mesmo
    professor no mesmo turno (exceto turno da noite, onde é permitido).

    Exemplo ruim: professor A com turma S1A no M-AB e logo no M-CD.
    """
    pontuacao = 0

    for horario in grades:
        for dia in DIAS:
            for turno in TURNOS:

                if turno == "N":
                    continue  # à noite é permitido

                slots = TURNOS[turno]

                for i in range(len(slots) - 1):
                    aula_atual     = horario.grade[dia][turno][slots[i]]
                    aula_seguinte  = horario.grade[dia][turno][slots[i + 1]]

                    if aula_atual is not None and aula_seguinte is not None:
                        if aula_atual.turma.cod == aula_seguinte.turma.cod:
                            pontuacao = pontuacao + PESO_FLEX_1

    return pontuacao


def flex2_muitas_aulas_mesma_turma_no_dia(grades):
    """
    Regra flexível: Evitar mais de 2 aulas da mesma turma com o mesmo professor
    no mesmo dia (exceto turno da noite).
    """
    pontuacao = 0

    for horario in grades:
        for dia in DIAS:

            # Conta quantas vezes cada turma aparece na grade do professor neste dia
            contagem_por_turma = {}

            for turno in TURNOS:
                if turno == "N":
                    continue

                for slot in TURNOS[turno]:
                    aula = horario.grade[dia][turno][slot]
                    if aula is not None:
                        cod = aula.turma.cod
                        if cod not in contagem_por_turma:
                            contagem_por_turma[cod] = 0
                        contagem_por_turma[cod] += 1

            for cod in contagem_por_turma:
                if contagem_por_turma[cod] > 1:
                    pontuacao += PESO_FLEX_2

    return pontuacao


def flex3_horarios_livres_posicao(grades):
    """
    Regra flexível: Priorizar deixar o M-AB (início da manhã) e o T-CD
    (fim da tarde) livres. Punimos quando esses slots estão ocupados
    enquanto outros slots do mesmo turno estão vazios.
    """
    pontuacao = 0

    for horario in grades:
        for dia in DIAS:

            # Se M-AB está ocupado mas M-CD está vazio, a ordem está errada
            m_ab = horario.grade[dia]["M"]["AB"]
            m_cd = horario.grade[dia]["M"]["CD"]
            if m_ab is not None and m_cd is None:
                pontuacao = pontuacao + PESO_FLEX_3

            # Se T-CD está ocupado mas T-AB está vazio, a ordem está errada
            t_ab = horario.grade[dia]["T"]["AB"]
            t_cd = horario.grade[dia]["T"]["CD"]
            if t_cd is not None and t_ab is None:
                pontuacao = pontuacao + PESO_FLEX_3

    return pontuacao


def flex4_manha_antes_tarde_noite(grades):
    """
    Regra flexível: Preferir preencher a manhã antes de usar a tarde ou a noite.
    Se a manhã ainda tem slots vazios mas a tarde/noite já tem aula, punimos.
    """
    pontuacao = 0

    for horario in grades:
        for dia in DIAS:

            # Conta slots vazios na manhã
            slots_vazios_manha = 0
            for slot in TURNOS["M"]:
                if horario.grade[dia]["M"][slot] is None:
                    slots_vazios_manha = slots_vazios_manha + 1

            # Se a manhã está cheia, sem problema
            if slots_vazios_manha == 0:
                continue

            # Se há vaga na manhã mas tarde ou noite têm aula, punimos
            for turno in ["T", "N"]:
                for slot in TURNOS[turno]:
                    if horario.grade[dia][turno][slot] is not None:
                        pontuacao = pontuacao + PESO_FLEX_4

    return pontuacao


def flex5_janela_no_horario(grades):
    """
    Regra flexível: Evitar 'janelas' no horário do professor.
    Uma janela é um slot vazio entre dois slots com aula no mesmo dia.

    Exemplo ruim: M-AB com aula, M-CD vazio, T-AB com aula.
                  O professor fica esperando sem nada para fazer.

    Como verificamos:
    Montamos a sequência de todos os slots do dia em ordem e procuramos
    pelo padrão: slot com aula → slot vazio → slot com aula.
    """
    pontuacao = 0

    # Sequência de todos os slots de um dia, em ordem
    sequencia_do_dia = list()
    for turno in TURNOS:
        for slot in TURNOS[turno]:
            sequencia_do_dia.append((turno, slot))

    for horario in grades:
        for dia in DIAS:

            # Monta lista: 1 se tem aula, 0 se está vazio
            ocupacao = list()
            for (turno, slot) in sequencia_do_dia:
                if horario.grade[dia][turno][slot] is not None:
                    ocupacao.append(1)
                else:
                    ocupacao.append(0)

            # Encontra o primeiro e o último slot com aula no dia
            primeiro_com_aula = -1
            ultimo_com_aula   = -1

            for i in range(len(ocupacao)):
                if ocupacao[i] == 1:
                    if primeiro_com_aula == -1:
                        primeiro_com_aula = i
                    ultimo_com_aula = i

            # Se não tem nenhuma aula no dia, não há janela possível
            if primeiro_com_aula == -1:
                continue

            # Conta os slots vazios entre o primeiro e o último com aula
            for i in range(primeiro_com_aula, ultimo_com_aula):
                if ocupacao[i] == 0:
                    pontuacao = pontuacao + PESO_FLEX_5

    return pontuacao

def flex6_mesma_sala_turma(grades):

    pontuacao = 0

    salas_por_turma = {}

    for horario in grades:

        for dia in DIAS:
            for turno in TURNOS:
                for slot in TURNOS[turno]:

                    aula = horario.grade[dia][turno][slot]

                    if aula is None:
                        continue

                    turma = aula.turma.cod
                    sala = aula.sala.num_sala

                    if turma not in salas_por_turma:
                        salas_por_turma[turma] = set()

                    salas_por_turma[turma].add(sala)

    for turma in salas_por_turma:

        quantidade_salas = len(salas_por_turma[turma])

        if quantidade_salas > 1:

            pontuacao += (quantidade_salas - 1) * PESO_FLEX_6

    return pontuacao