# =============================================================================
# teste_ag_2_populacao.py
# =============================================================================
# OBJETIVO: Entender como a população é criada e avaliada.
#
# O que você vai aprender:
#   - O que é uma população no AG
#   - Como criar indivíduos aleatórios
#   - Como avaliar a população com a função fitness
#   - Como ver as estatísticas da população
# =============================================================================

from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao

print("=" * 55)
print("TESTE 2 — Criando e Avaliando uma População")
print("=" * 55)

# --- Dados do cenário ---
salas = [
    Sala(1, 30, False),
    Sala(2, 30, False),
    Sala(3, 30, True),
]

prof1 = Professor(1, "Ana Souza")
prof1.setHorarios_Bloqueados(("SEG", "M", "AB"))
prof1.setHorarios_Bloqueados(("SEG", "M", "CD"))

prof2 = Professor(2, "Bruno Lima")
prof2.setHorarios_Bloqueados(("SEX", "N", "AB"))
prof2.setHorarios_Bloqueados(("SEX", "N", "CD"))

turma1 = Turma("T1", "M")
turma2 = Turma("T2", "M")

mat1 = Disciplina("mat1", 1, "matematica", 2, False)
fis1 = Disciplina("fis1", 1, "fisica",     2, False)
poo  = Disciplina("poo",  2, "poo",        2, True)

# As configurações dizem ao AG quais alocações cada professor tem
configuracoes = [
    {
        'professor': prof1,
        'alocacoes': [(mat1, turma1), (fis1, turma2)],
        'salas':     salas
    },
    {
        'professor': prof2,
        'alocacoes': [(poo, turma1)],
        'salas':     salas
    },
]

# --- Criando a população ---
print("\nCriando população com 6 indivíduos...")
populacao = Populacao(tamanho=6, configuracoes=configuracoes)
populacao.gerar()

print("\nAvaliando a população (calculando fitness de cada indivíduo)...")
populacao.avaliar()

print("\nResumo da população:")
print(populacao)

print("Estatísticas:")
populacao.estatisticas()

print("\nMelhor indivíduo encontrado:")
print("  Fitness: " + str(populacao.melhor.fitness))

print("\n--- Testando a seleção por torneio ---")
print("Realizando 5 torneios com 3 participantes cada:\n")
for i in range(5):
    vencedor = populacao.selecionar_por_torneio(tamanho_torneio=3)
    print("  Torneio " + str(i + 1) + " — vencedor com fitness: " + str(vencedor.fitness))

print("\n" + "=" * 55)
print("Observe que os vencedores tendem a ter fitness menor.")
print("Isso é a seleção natural do AG em ação!")
print("=" * 55)
