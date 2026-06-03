# =============================================================================
# Populacao.py
# =============================================================================
# A população é o conjunto de todos os indivíduos do algoritmo genético.
# Cada indivíduo é uma solução candidata (horário completo da escola).
#
# O algoritmo genético trabalha com a população inteira, evoluindo-a ao longo
# de várias gerações. A cada geração:
#   1. Avaliamos o fitness de cada indivíduo
#   2. Selecionamos os melhores para gerar filhos
#   3. Aplicamos crossover e mutação nos filhos
#   4. Substituímos a população antiga pela nova
#
# Esta classe cuida dos passos 1 e 2 (avaliação e seleção).
# O crossover, a mutação e o laço principal estão em AlgoritmoGenetico.py.
# =============================================================================

import random
from Individuo import Individuo
from Horario import Horario
from fitness import calcular_fitness


class Populacao:

    def __init__(self, tamanho, configuracoes):
        """
        tamanho       : quantos indivíduos a população terá.
        configuracoes : lista de dicionários, um por professor.
                        Cada dicionário tem:
                          'professor' : objeto Professor
                          'alocacoes' : lista de tuplas (Disciplina, Turma)
                          'salas'     : lista de objetos Sala disponíveis

        Exemplo de configuracoes:
            [
                {
                    'professor': prof1,
                    'alocacoes': [(mat1, turma1), (fis1, turma2)],
                    'salas':     [sala1, sala2]
                },
                {
                    'professor': prof2,
                    'alocacoes': [(port1, turma1)],
                    'salas':     [sala1]
                },
            ]
        """
        self.tamanho       = tamanho
        self.configuracoes = configuracoes
        self.individuos    = list()

        # Guarda o melhor indivíduo encontrado em toda a evolução
        self.melhor = None

    # -------------------------------------------------------------------------
    # GERAÇÃO DA POPULAÇÃO INICIAL
    # -------------------------------------------------------------------------

    def gerar(self):
        """
        Cria todos os indivíduos da população gerando grades aleatórias.

        Para cada indivíduo:
          - Criamos uma grade (Horario) para cada professor
          - Cada grade é gerada aleatoriamente respeitando as restrições rígidas
          - Juntamos todas as grades num único objeto Individuo
        """
        self.individuos = list()

        for i in range(self.tamanho):

            grades = list()  # lista de Horario, um por professor

            for config in self.configuracoes:
                horario = Horario(
                    config['professor'],
                    config['alocacoes'],
                    config['salas']
                )
                horario.gerar_individuo_aleatorio()
                grades.append(horario)

            individuo = Individuo(grades)
            self.individuos.append(individuo)

        print("População gerada com " + str(self.tamanho) + " indivíduos.")

    # -------------------------------------------------------------------------
    # AVALIAÇÃO
    # -------------------------------------------------------------------------

    def avaliar(self):
        """
        Calcula o fitness de cada indivíduo.

        Percorre todos os indivíduos, chama calcular_fitness() passando
        todas as grades daquele indivíduo, e guarda o resultado.

        Também atualiza self.melhor com o indivíduo de menor fitness.
        """
        for individuo in self.individuos:
            individuo.fitness = calcular_fitness(individuo.grades)

        self._atualizar_melhor()

    def _atualizar_melhor(self):
        """
        Percorre os indivíduos e guarda o de menor fitness em self.melhor.
        Chamado automaticamente após avaliar().
        """
        for individuo in self.individuos:
            if self.melhor is None:
                self.melhor = individuo
            else:
                if individuo.fitness < self.melhor.fitness:
                    self.melhor = individuo

    # -------------------------------------------------------------------------
    # SELEÇÃO POR TORNEIO
    # -------------------------------------------------------------------------

    def selecionar_por_torneio(self, tamanho_torneio):
        """
        Seleciona um indivíduo usando o método de torneio.

        Como funciona:
          1. Escolhemos aleatoriamente 'tamanho_torneio' indivíduos da população
          2. Comparamos os fitness desses indivíduos
          3. O indivíduo com MENOR fitness vence o torneio e é retornado

        Por que torneio?
          É simples de entender e implementar. Os melhores têm mais chance
          de serem selecionados, mas os piores também têm alguma chance —
          isso mantém a diversidade da população.

        tamanho_torneio: quantos indivíduos participam de cada torneio.
                         Valores comuns: 2, 3 ou 5.
        """
        # Sorteia os participantes do torneio aleatoriamente
        participantes = list()
        for i in range(tamanho_torneio):
            participante = random.choice(self.individuos)
            participantes.append(participante)

        # Encontra o vencedor (menor fitness)
        vencedor = participantes[0]
        for i in range(1, len(participantes)):
            if participantes[i].fitness < vencedor.fitness:
                vencedor = participantes[i]

        return vencedor

    # -------------------------------------------------------------------------
    # INFORMAÇÕES
    # -------------------------------------------------------------------------

    def estatisticas(self):
        """
        Exibe um resumo da população atual: menor, maior e média de fitness.
        Útil para acompanhar a evolução do AG a cada geração.
        """
        if len(self.individuos) == 0:
            print("População vazia.")
            return

        menor = self.individuos[0].fitness
        maior = self.individuos[0].fitness
        total = 0

        for individuo in self.individuos:
            if individuo.fitness is None:
                print("Aviso: chame avaliar() antes de ver estatísticas.")
                return
            if individuo.fitness < menor:
                menor = individuo.fitness
            if individuo.fitness > maior:
                maior = individuo.fitness
            total = total + individuo.fitness

        media = total / len(self.individuos)

        print("  Indivíduos      : " + str(len(self.individuos)))
        print("  Melhor fitness  : " + str(menor))
        print("  Pior fitness    : " + str(maior))
        print("  Média fitness   : " + str(round(media, 1)))

    def __repr__(self):
        resultado = "População com " + str(len(self.individuos)) + " indivíduos:\n"
        for i in range(len(self.individuos)):
            resultado = resultado + "  Indivíduo " + str(i + 1) + ": fitness = " + str(self.individuos[i].fitness) + "\n"
        return resultado
