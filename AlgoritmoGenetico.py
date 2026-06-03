# =============================================================================
# AlgoritmoGenetico.py
# =============================================================================
# Este arquivo contém o coração do projeto: o algoritmo genético (AG).
#
# O AG funciona como a evolução natural:
#   - Começa com uma população de soluções aleatórias (geração 0)
#   - Avalia quão boa é cada solução (fitness)
#   - Seleciona as melhores soluções para "se reproduzirem"
#   - Gera novos filhos combinando partes das soluções dos pais (crossover)
#   - Aplica pequenas mudanças aleatórias nos filhos (mutação)
#   - Repete o processo por várias gerações
#
# Ao final, a solução com menor fitness é o nosso melhor horário encontrado.
#
# Operações implementadas:
#   1. crossover()  — combina dois pais para gerar dois filhos
#   2. mutacao()    — troca dois slots aleatórios na grade de um filho
#   3. evoluir()    — o laço principal que repete tudo por N gerações
# =============================================================================

import random
from Individuo import Individuo
from Horario import Horario, DIAS, TURNOS
from Aula import Aula
from Populacao import Populacao
from fitness import calcular_fitness


class AlgoritmoGenetico:

    def __init__(self, populacao, taxa_crossover, taxa_mutacao, tamanho_torneio):
        """
        populacao        : objeto Populacao já criado e avaliado.
        taxa_crossover   : probabilidade de aplicar crossover (ex: 0.8 = 80%).
        taxa_mutacao     : probabilidade de aplicar mutação (ex: 0.1 = 10%).
        tamanho_torneio  : quantos indivíduos competem em cada torneio (ex: 3).
        """
        self.populacao       = populacao
        self.taxa_crossover  = taxa_crossover
        self.taxa_mutacao    = taxa_mutacao
        self.tamanho_torneio = tamanho_torneio

        # Histórico do melhor fitness a cada geração (útil para análise)
        self.historico_melhor_fitness = list()

    # =========================================================================
    # CROSSOVER
    # =========================================================================

    def crossover(self, pai1, pai2):
        """
        Combina dois indivíduos (pais) para gerar dois novos indivíduos (filhos).

        Como funciona (crossover por dia):
          - Escolhemos aleatoriamente um ponto de corte entre os dias da semana.
          - O filho 1 herda os dias ANTES do corte do pai 1, e os dias DEPOIS do pai 2.
          - O filho 2 faz o inverso.

        Exemplo com ponto de corte na QUA:
          Pai 1:  SEG TER | QUA QUI SEX
          Pai 2:  SEG TER | QUA QUI SEX
          Filho1: SEG TER (do pai1) + QUA QUI SEX (do pai2)
          Filho2: SEG TER (do pai2) + QUA QUI SEX (do pai1)

        Por que isso funciona?
          Se o pai 1 tem um bom horário na segunda e terça, e o pai 2 tem um
          bom horário de quarta a sexta, o filho pode herdar o melhor dos dois.
        """
        # Se não aplicar crossover, retorna cópias dos pais sem modificação
        if random.random() > self.taxa_crossover:
            filho1 = self._copiar_individuo(pai1)
            filho2 = self._copiar_individuo(pai2)
            return filho1, filho2

        # Escolhe o ponto de corte (entre 1 e len(DIAS)-1 para garantir mistura)
        ponto_de_corte = random.randint(1, len(DIAS) - 1)

        # Dias que cada filho herda de cada pai
        dias_do_pai1 = DIAS[:ponto_de_corte]   # ex: ["SEG", "TER"]
        dias_do_pai2 = DIAS[ponto_de_corte:]    # ex: ["QUA", "QUI", "SEX"]

        # Cria as grades dos filhos copiando os dias corretos de cada pai
        grades_filho1 = list()
        grades_filho2 = list()

        for i in range(len(pai1.grades)):
            horario_pai1 = pai1.grades[i]
            horario_pai2 = pai2.grades[i]

            # Cria dois novos Horarios vazios para os filhos
            novo_horario1 = Horario(
                horario_pai1.professor,
                horario_pai1.alocacoes,
                horario_pai1.salas
            )
            novo_horario2 = Horario(
                horario_pai2.professor,
                horario_pai2.alocacoes,
                horario_pai2.salas
            )

            # Filho 1: dias do pai1 antes do corte + dias do pai2 depois
            for dia in dias_do_pai1:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        aula = horario_pai1.grade[dia][turno][slot]
                        novo_horario1.grade[dia][turno][slot] = self._copiar_aula(aula)

            for dia in dias_do_pai2:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        aula = horario_pai2.grade[dia][turno][slot]
                        novo_horario1.grade[dia][turno][slot] = self._copiar_aula(aula)

            # Filho 2: o inverso
            for dia in dias_do_pai1:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        aula = horario_pai2.grade[dia][turno][slot]
                        novo_horario2.grade[dia][turno][slot] = self._copiar_aula(aula)

            for dia in dias_do_pai2:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        aula = horario_pai1.grade[dia][turno][slot]
                        novo_horario2.grade[dia][turno][slot] = self._copiar_aula(aula)

            grades_filho1.append(novo_horario1)
            grades_filho2.append(novo_horario2)

        filho1 = Individuo(grades_filho1)
        filho2 = Individuo(grades_filho2)

        return filho1, filho2

    # =========================================================================
    # MUTAÇÃO
    # =========================================================================

    def mutacao(self, individuo):
        """
        Aplica uma pequena mudança aleatória em um indivíduo.

        Como funciona:
          - Para cada grade (professor) do indivíduo, sorteamos se haverá mutação.
          - Se sim, escolhemos dois slots aleatórios e trocamos o conteúdo deles.

        Por que mutação?
          O crossover combina soluções existentes, mas pode não explorar partes
          do espaço de soluções que nunca apareceram. A mutação introduz novidade,
          evitando que o AG fique preso numa solução boa mas não ótima.

        Taxa de mutação baixa (ex: 10%) é o usual. Alta demais torna o AG
        aleatório; baixa demais faz ele convergir rápido demais.
        """
        for horario in individuo.grades:

            # Sorteia se este professor sofrerá mutação
            if random.random() > self.taxa_mutacao:
                continue

            # Monta lista de todos os slots possíveis
            todos_os_slots = list()
            for dia in DIAS:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        todos_os_slots.append((dia, turno, slot))

            # Escolhe dois slots aleatórios
            slot_a = random.choice(todos_os_slots)
            slot_b = random.choice(todos_os_slots)

            # Troca o conteúdo dos dois slots
            dia_a, turno_a, slot_a_nome = slot_a
            dia_b, turno_b, slot_b_nome = slot_b

            aula_a = horario.grade[dia_a][turno_a][slot_a_nome]
            aula_b = horario.grade[dia_b][turno_b][slot_b_nome]

            horario.grade[dia_a][turno_a][slot_a_nome] = aula_b
            horario.grade[dia_b][turno_b][slot_b_nome] = aula_a

    # =========================================================================
    # LAÇO PRINCIPAL — EVOLUÇÃO
    # =========================================================================

    def evoluir(self, numero_de_geracoes):
        """
        Executa o laço principal do algoritmo genético.

        A cada geração:
          1. Selecionamos pais pelo método de torneio
          2. Aplicamos crossover para gerar filhos
          3. Aplicamos mutação nos filhos
          4. Calculamos o fitness dos filhos
          5. Substituímos a população pelos filhos
          6. Guardamos o melhor indivíduo encontrado até agora

        numero_de_geracoes: quantas vezes o ciclo se repete.
        """
        print("\n" + "=" * 50)
        print("Iniciando evolução por " + str(numero_de_geracoes) + " gerações")
        print("=" * 50)

        for geracao in range(numero_de_geracoes):

            nova_populacao = list()

            # Geramos novos indivíduos até completar o tamanho da população
            while len(nova_populacao) < self.populacao.tamanho:

                # --- PASSO 1: SELEÇÃO ---
                # Escolhemos dois pais pelo torneio
                pai1 = self.populacao.selecionar_por_torneio(self.tamanho_torneio)
                pai2 = self.populacao.selecionar_por_torneio(self.tamanho_torneio)

                # --- PASSO 2: CROSSOVER ---
                # Combinamos os pais para gerar dois filhos
                filho1, filho2 = self.crossover(pai1, pai2)

                # --- PASSO 3: MUTAÇÃO ---
                # Aplicamos pequenas mudanças aleatórias nos filhos
                self.mutacao(filho1)
                self.mutacao(filho2)

                # --- PASSO 4: AVALIAÇÃO DOS FILHOS ---
                # Calculamos o fitness de cada filho
                filho1.fitness = calcular_fitness(filho1.grades)
                filho2.fitness = calcular_fitness(filho2.grades)

                nova_populacao.append(filho1)
                nova_populacao.append(filho2)

            # --- PASSO 5: SUBSTITUI A POPULAÇÃO ---
            # A nova geração substitui a antiga
            self.populacao.individuos = nova_populacao[:self.populacao.tamanho]

            # --- PASSO 6: ATUALIZA O MELHOR ---
            self.populacao._atualizar_melhor()

            # Registra o melhor fitness desta geração no histórico
            self.historico_melhor_fitness.append(self.populacao.melhor.fitness)

            # Exibe progresso a cada 10 gerações
            if (geracao + 1) % 10 == 0 or geracao == 0:
                print("Geração " + str(geracao + 1) + " | Melhor fitness: " + str(self.populacao.melhor.fitness))

        print("=" * 50)
        print("Evolução concluída!")
        print("Melhor fitness final: " + str(self.populacao.melhor.fitness))
        print("=" * 50)

    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================

    def _copiar_aula(self, aula):
        """
        Cria uma cópia independente de um objeto Aula.
        Necessário no crossover para que pai e filho não compartilhem
        o mesmo objeto em memória (o que causaria bugs ao mutar).
        """
        if aula is None:
            return None
        return Aula((aula.disciplina, aula.turma), aula.sala)

    def _copiar_individuo(self, individuo):
        """
        Cria uma cópia completa de um indivíduo (todas as grades).
        Usado quando o crossover não é aplicado.
        """
        novas_grades = list()

        for horario in individuo.grades:
            novo_horario = Horario(
                horario.professor,
                horario.alocacoes,
                horario.salas
            )
            for dia in DIAS:
                for turno in TURNOS:
                    for slot in TURNOS[turno]:
                        aula = horario.grade[dia][turno][slot]
                        novo_horario.grade[dia][turno][slot] = self._copiar_aula(aula)

            novas_grades.append(novo_horario)

        novo_individuo = Individuo(novas_grades)
        novo_individuo.fitness = individuo.fitness
        return novo_individuo

    def exibir_historico(self):
        """
        Exibe o histórico do melhor fitness a cada geração.
        Útil para visualizar se o AG está melhorando ao longo do tempo.
        """
        print("\nHistórico do melhor fitness por geração:")
        for i in range(len(self.historico_melhor_fitness)):
            print("  Geração " + str(i + 1) + ": " + str(self.historico_melhor_fitness[i]))
