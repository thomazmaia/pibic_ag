# =============================================================================
# Individuo.py
# =============================================================================
# No algoritmo genético, um "indivíduo" é uma solução candidata para o problema.
#
# No nosso caso: um indivíduo é o horário COMPLETO da escola para uma semana.
# Isso significa: a grade de horários de TODOS os professores juntos.
#
# Por que todos juntos?
# Porque precisamos verificar conflitos entre professores:
#   - Dois professores não podem usar a mesma sala ao mesmo tempo.
#   - A mesma turma não pode ter duas aulas simultâneas.
# Essas verificações só são possíveis olhando todas as grades ao mesmo tempo.
#
# O atributo "fitness" guarda a pontuação de punições do indivíduo.
# Começa como None e é preenchido quando chamamos Populacao.avaliar().
# =============================================================================

class Individuo:

    def __init__(self, grades):
        # grades é uma lista de objetos Horario, um por professor
        self.grades  = grades

        # A pontuação fitness começa como None (ainda não calculada).
        # Será preenchida pela função calcular_fitness() do arquivo fitness.py.
        # Quanto MENOR o fitness, MELHOR é o indivíduo.
        self.fitness = None

    def __repr__(self):
        resultado = ""
        for horario in self.grades:
            resultado = resultado + str(horario)
        resultado = resultado + "Fitness: " + str(self.fitness) + "\n"
        return resultado
