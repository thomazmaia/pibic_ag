# =============================================================================
# teste_ag_3_crossover_mutacao.py
# =============================================================================
# OBJETIVO: Entender como crossover e mutação funcionam.
#
# O que você vai aprender:
#   - O que é crossover (cruzamento entre dois pais)
#   - O que é mutação (mudança aleatória em um filho)
#   - Como o fitness dos filhos se compara ao dos pais
# =============================================================================

from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao
from AlgoritmoGenetico import AlgoritmoGenetico

print("=" * 55)
print("TESTE 3 — Crossover e Mutação")
print("=" * 55)

# --- Dados do cenário ---
salas = [
    Sala(1, 30, False),
    Sala(2, 30, False),
    Sala(3, 30, True),
]

prof1 = Professor(1, "Carlos Melo")
prof2 = Professor(2, "Diana Faria")

turma1 = Turma("T1", "M")
turma2 = Turma("T2", "N")

mat1  = Disciplina("mat1", 1, "matematica", 2, False)
fis1  = Disciplina("fis1", 1, "fisica",     2, False)
pest  = Disciplina("pest", 2, "programacao", 2, True)

configuracoes = [
    {
        'professor': prof1,
        'alocacoes': [(mat1, turma1), (fis1, turma2)],
        'salas':     salas
    },
    {
        'professor': prof2,
        'alocacoes': [(pest, turma1)],
        'salas':     salas
    },
]

populacao = Populacao(tamanho=6, configuracoes=configuracoes)
populacao.gerar()
populacao.avaliar()

print("\nPopulação inicial:")
populacao.estatisticas()

# Criamos o AG com taxa de crossover alta e mutação baixa
ag = AlgoritmoGenetico(
    populacao       = populacao,
    taxa_crossover  = 0.9,   # 90% de chance de cruzar
    taxa_mutacao    = 0.1,   # 10% de chance de mutar
    tamanho_torneio = 2
)

# --- Testando crossover manualmente ---
print("\n--- Testando crossover entre dois indivíduos ---")

pai1 = populacao.selecionar_por_torneio(2)
pai2 = populacao.selecionar_por_torneio(2)

print("Fitness do pai 1: " + str(pai1.fitness))
print("Fitness do pai 2: " + str(pai2.fitness))

filho1, filho2 = ag.crossover(pai1, pai2)
filho1.fitness = __import__('fitness').calcular_fitness(filho1.grades)
filho2.fitness = __import__('fitness').calcular_fitness(filho2.grades)

print("Fitness do filho 1: " + str(filho1.fitness))
print("Fitness do filho 2: " + str(filho2.fitness))
print("(Os filhos herdam partes dos dois pais — podem ser melhores ou piores)")

# --- Testando mutação manualmente ---
print("\n--- Testando mutação em um indivíduo ---")

individuo_antes = populacao.selecionar_por_torneio(2)
fitness_antes = individuo_antes.fitness
print("Fitness antes da mutação: " + str(fitness_antes))

ag.mutacao(individuo_antes)
individuo_antes.fitness = __import__('fitness').calcular_fitness(individuo_antes.grades)
print("Fitness após a mutação:   " + str(individuo_antes.fitness))
print("(A mutação troca dois slots aleatórios — pode melhorar ou piorar)")

print("\n" + "=" * 55)
print("Lembre-se:")
print("  Crossover combina boas partes de dois pais.")
print("  Mutação introduz novidade para escapar de mínimos locais.")
print("=" * 55)
