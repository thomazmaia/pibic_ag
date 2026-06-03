# =============================================================================
# teste_ag_4_evolucao_simples.py
# =============================================================================
# OBJETIVO: Ver o AG evoluindo por completo em um cenário simples.
#
# Este teste roda o AG do início ao fim e mostra como o fitness
# melhora ao longo das gerações.
#
# O que você vai aprender:
#   - Como montar tudo junto (população + AG)
#   - Como o fitness muda de geração para geração
#   - Como ver o melhor horário encontrado
# =============================================================================

from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao
from AlgoritmoGenetico import AlgoritmoGenetico

print("=" * 55)
print("TESTE 4 — Evolução Simples (2 professores)")
print("=" * 55)

# --- Dados do cenário: escola pequena com 2 professores ---
salas = [
    Sala(1, 35, False),
    Sala(2, 35, False),
    Sala(3, 25, True),
]

prof1 = Professor(101, "Eduardo Neves")
prof1.setHorarios_Bloqueados(("SEG", "M", "AB"))
prof1.setHorarios_Bloqueados(("SEG", "M", "CD"))

prof2 = Professor(102, "Fernanda Costa")
prof2.setHorarios_Bloqueados(("SEX", "N", "AB"))
prof2.setHorarios_Bloqueados(("SEX", "N", "CD"))

turma_a = Turma("1A", "M")
turma_b = Turma("2A", "T")

mat = Disciplina("mat", 1, "matematica",   2, False)
fis = Disciplina("fis", 1, "fisica",       2, False)
poo = Disciplina("poo", 2, "programacao",  2, True)
geo = Disciplina("geo", 1, "geografia",    2, False)

configuracoes = [
    {
        'professor': prof1,
        'alocacoes': [(mat, turma_a), (fis, turma_b)],
        'salas':     salas
    },
    {
        'professor': prof2,
        'alocacoes': [(poo, turma_a), (geo, turma_b)],
        'salas':     salas
    },
]

# --- Criando e avaliando a população inicial ---
print("\nCriando população inicial com 10 indivíduos...")
populacao = Populacao(tamanho=10, configuracoes=configuracoes)
populacao.gerar()
populacao.avaliar()

print("\nPopulação ANTES da evolução:")
populacao.estatisticas()
print("Melhor fitness inicial: " + str(populacao.melhor.fitness))

# --- Criando o AG e evoluindo ---
ag = AlgoritmoGenetico(
    populacao       = populacao,
    taxa_crossover  = 0.85,
    taxa_mutacao    = 0.15,
    tamanho_torneio = 3
)

ag.evoluir(numero_de_geracoes=30)

# --- Resultado final ---
print("\nPopulação APÓS a evolução:")
populacao.estatisticas()

print("\n--- Melhor horário encontrado ---")
print(populacao.melhor)

print("\n--- Histórico resumido do melhor fitness ---")
historico = ag.historico_melhor_fitness
# Mostra apenas a cada 5 gerações para não poluir a saída
for i in range(len(historico)):
    if (i + 1) % 5 == 0 or i == 0:
        print("  Geração " + str(i + 1) + ": " + str(historico[i]))
