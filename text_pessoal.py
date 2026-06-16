from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao
from AlgoritmoGenetico import AlgoritmoGenetico

import matplotlib.pyplot as plt



print("=" * 60)
print("TESTE — Escola Completa (10 professores, 8 turmas)")
print("=" * 60)

# --- Salas ---
salas = [
    Sala(1, 35, False),
    Sala(2, 35, False),
    Sala(3, 35, False),
    Sala(4, 30, False),
    Sala(5, 25, False),
    Sala(6, 20, False),
    Sala(7, 35, False),
    Sala(8, 35, False),
    Sala(9, 35, False),
    Sala(10, 30, False),
    Sala(11, 25, False),
    Sala(12, 20, False),

    Sala(13, 30, True),
    Sala(14, 30, True),
    Sala(15, 30, True),
    Sala(16, 30, True),
    Sala(17, 30, True),
    Sala(18, 30, True),
]

# --- Professores com seus bloqueios ---
prof1 = Professor(1001, "Thomaz Maia")
prof1.setHorarios_Bloqueados(("SEX", "M", "AB"))
prof1.setHorarios_Bloqueados(("SEX", "M", "CD"))
prof1.setHorarios_Bloqueados(("SEX", "T", "AB"))
prof1.setHorarios_Bloqueados(("SEX", "T", "CD"))
prof1.setHorarios_Bloqueados(("SEX", "N", "AB"))
prof1.setHorarios_Bloqueados(("SEX", "N", "CD"))
prof1.setDias_concentrados(True)

prof2 = Professor(1002, "Maria Silva")
prof2.setHorarios_Bloqueados(("TER", "N", "AB"))
prof2.setHorarios_Bloqueados(("QUA", "M", "CD"))
prof2.setHorarios_Bloqueados(("QUI", "T", "AB"))

prof3 = Professor(1003, "Carlos Oliveira")
prof3.setHorarios_Bloqueados(("QUA", "N", "AB"))
prof3.setHorarios_Bloqueados(("QUI", "M", "CD"))

prof4 = Professor(1004, "Ana Costa")
prof4.setHorarios_Bloqueados(("TER", "M", "AB"))
prof4.setHorarios_Bloqueados(("QUI", "N", "CD"))
prof4.setHorarios_Bloqueados(("SEX", "T", "AB"))
prof4.setHorarios_Bloqueados(("SEX", "N", "CD"))
prof4.setDias_concentrados(True)

prof5 = Professor(1005, "Luiz Santos")
prof5.setHorarios_Bloqueados(("SEG", "N", "AB"))
prof5.setHorarios_Bloqueados(("TER", "T", "CD"))
prof5.setHorarios_Bloqueados(("QUA", "M", "AB"))

prof6 = Professor(1006, "Alan Bezerra")
prof6.setHorarios_Bloqueados(("SEG", "M", "AB"))
prof6.setHorarios_Bloqueados(("SEG", "M", "CD"))
prof6.setHorarios_Bloqueados(("SEG", "T", "AB"))
prof6.setHorarios_Bloqueados(("SEG", "T", "CD"))

prof7 = Professor(1007, "Helton Bezerra")
prof7.setHorarios_Bloqueados(("TER", "M", "AB"))
prof7.setHorarios_Bloqueados(("TER", "M", "CD"))
prof7.setHorarios_Bloqueados(("TER", "T", "AB"))
prof7.setHorarios_Bloqueados(("TER", "T", "CD"))

prof8 = Professor(1008, "Francisco Elder")
prof8.setHorarios_Bloqueados(("QUI", "M", "AB"))
prof8.setHorarios_Bloqueados(("QUI", "M", "CD"))
prof8.setHorarios_Bloqueados(("QUI", "T", "AB"))
prof8.setHorarios_Bloqueados(("QUI", "T", "CD"))

prof9 = Professor(1009, "Roger Sarmento")
prof9.setHorarios_Bloqueados(("TER", "N", "AB"))
prof9.setHorarios_Bloqueados(("TER", "N", "CD"))
prof9.setHorarios_Bloqueados(("QUA", "M", "AB"))
prof9.setDias_concentrados(True)

prof10 = Professor(1010, "Tiago Estevam")
prof10.setHorarios_Bloqueados(("SEG", "N", "AB"))
prof10.setHorarios_Bloqueados(("SEG", "N", "CD"))
prof10.setHorarios_Bloqueados(("QUA", "M", "AB"))
prof10.setDias_concentrados(True)


# --- Turmas ---
turma1 = Turma("S1A", "M")
turma2 = Turma("S1B", "M")
turma3 = Turma("S2",  "M")
turma4 = Turma("S3A", "M")
turma5 = Turma("S3B", "M")
turma6 = Turma("S4",  "M")
turma7 = Turma("S5",  "M")
turma8 = Turma("S6",  "M")

# --- Disciplinas ---

# prof 1
pest = Disciplina("pest",  3, "prog estruturada", 2, True)
web1 = Disciplina("web1", 4, "des web 1",        2, True)
mat1  = Disciplina("mat1",  1, "matematica 1",   2, False)
mat2  = Disciplina("mat2",  2, "matematica 2",    2, False)

# prof 2
engen = Disciplina("engen", 3, "eng software",    2, True)
quim1  = Disciplina("quim1", 1, "quimica 1",       2, False)
quim2 = Disciplina("quim2", 2, "quimica 2",       2, False)


# prof 3
fis1  = Disciplina("fis1",  1, "fisica 1",        2, False)
fis2  = Disciplina("fis2",  2, "fisica 2",        2, False)
fis3  = Disciplina("fis3",  3, "fisica 3",        2, False)
fis4  = Disciplina("fis4",  4, "fisica 4",        2, False)

# prof 4
port1 = Disciplina("port1", 1, "portugues 1",     2, False)
port2 = Disciplina("port2", 2, "portugues 2",     2, False)
hist_africa = Disciplina("hist_africa", 3, "historia africa", 2, False)
quim3 = Disciplina("quim3", 3, "quimica 3",       2, False)

# prof 5
hist1 = Disciplina("hist1", 1, "historia 1",      2, False)
hist2 = Disciplina("hist2", 2, "historia 2",      2, False)
hist3 = Disciplina("hist3", 4, "historia 3",      2, False)
hist4 = Disciplina("hist4", 5, "historia 4",      2, False)

# prof 6
port3 = Disciplina("port3", 3, "portugues 3",     2, False)
port5 = Disciplina("port5", 5, "portugues 5",     2, False)
ling_sinais = Disciplina("ling_sinais", 3, "linguagem de sinais", 2, False)

# prof 7
ingl1 = Disciplina("ingl1", 1, "ingles 1",        2, False)
ingl2 = Disciplina("ingl2", 2, "ingles 2",        2, False)
ingl3 = Disciplina("ingl3", 5, "ingles 3",        2, False)
ingl4 = Disciplina("ingl4", 6, "ingles 4",        2, False)

# prof 8
redacao1 = Disciplina("redacao1", 5, "redação 1",             2, True)
redacao2 = Disciplina("redacao2", 6, "redação 2",             2, True)
port4 = Disciplina("port4", 4, "portugues 4",     2, False)


# prof 9
bd = Disciplina("bd", 3, "banco de dados", 2, True)
poo   = Disciplina("poo",   4, "prog orientada",  2, True)
mat3  = Disciplina("mat3",  3, "matematica 3",    2, False)
mat4  = Disciplina("mat4",  4, "matematica 4",    2, False)

# prof 10
geo1 = Disciplina("geo1", 1, "geografia 1",     2, False)
geo2 = Disciplina("geo2", 2, "geografia 2",     2, False)
geo3 = Disciplina("geo3", 3, "geografia 3",     2, False)
geo4 = Disciplina("geo4", 5, "geografia 4",     2, False)
geo5 = Disciplina("geo5", 6, "geografia 5",     2, False)

# --- Alocações: cada professor recebe APENAS as suas disciplinas ---

# turma1 = Turma("S1A", "M")
# turma2 = Turma("S1B", "M")
# turma3 = Turma("S2",  "M")
# turma4 = Turma("S3A", "M")
# turma5 = Turma("S3B", "M")
# turma6 = Turma("S4",  "M")
# turma7 = Turma("S5",  "M")
# turma8 = Turma("S6",  "M")

alocacoes_prof1 = [(pest, turma4), (web1, turma6), (mat1, turma2), (mat2, turma3)]
alocacoes_prof2 = [(engen, turma5),(quim1, turma1), (quim2, turma2)]
alocacoes_prof3 = [(fis1, turma1), (fis2, turma3), (fis3, turma4), (fis4, turma6)]
alocacoes_prof4 = [(port1, turma1), (port2, turma3), (hist_africa, turma4), (quim3, turma4)]
alocacoes_prof5 = [(hist1, turma1), (hist2, turma3), (hist3, turma6), (hist4, turma7)]
alocacoes_prof6 = [(port3, turma4), (port5, turma7), (ling_sinais, turma5)]
alocacoes_prof7 = [(ingl1, turma2), (ingl2, turma3), (ingl3, turma7), (ingl4, turma8)]
alocacoes_prof8 = [(redacao1, turma7), (redacao2, turma8), (port4, turma6)]
alocacoes_prof9 = [(bd, turma5), (poo, turma6), (mat3, turma5), (mat4, turma6)]
alocacoes_prof10 = [(geo1, turma2), (geo2, turma3), (geo3, turma4), (geo4, turma6), (geo5, turma7)]

configuracoes = [
    {'professor': prof1, 'alocacoes': alocacoes_prof1, 'salas': salas}, # Thomaz
    {'professor': prof2, 'alocacoes': alocacoes_prof2, 'salas': salas}, # Maria
    {'professor': prof3, 'alocacoes': alocacoes_prof3, 'salas': salas}, # Carlos
    {'professor': prof4, 'alocacoes': alocacoes_prof4, 'salas': salas}, # Ana
    {'professor': prof5, 'alocacoes': alocacoes_prof5, 'salas': salas}, # Luiz
    {'professor': prof6, 'alocacoes': alocacoes_prof6, 'salas': salas}, # Alan
    {'professor': prof7, 'alocacoes': alocacoes_prof7, 'salas': salas}, # Helton
    {'professor': prof8, 'alocacoes': alocacoes_prof8, 'salas': salas}, # Francisco
    {'professor': prof9, 'alocacoes': alocacoes_prof9, 'salas': salas}, # Roger
    {'professor': prof10, 'alocacoes': alocacoes_prof10, 'salas': salas}, # Tiago
]

populacao = Populacao(tamanho=50, configuracoes=configuracoes)
populacao.gerar()
populacao.avaliar()

populacao.estatisticas()

ag = AlgoritmoGenetico(
    populacao       = populacao,
    taxa_crossover  = 0.87,
    taxa_mutacao    = 0.1,
    tamanho_torneio = 10
)

ag.evoluir(numero_de_geracoes=750)

populacao.estatisticas()

print("\n--- Melhor horário encontrado ---")
print(populacao.melhor)

print("\n--- Evolução do melhor fitness ---")
historico = ag.historico_melhor_fitness

for i in range(len(historico)):
    if (i + 1) % 10 == 0 or i == 0:
        print("  Geração " + str(i + 1) + ": fitness = " + str(historico[i]))

plt.figure(figsize=(10, 5))

plt.plot(
    range(1, len(historico) + 1),
    historico,
    marker='o'
)

plt.title("Evolução do Melhor Fitness")
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.grid(True)

plt.tight_layout()
plt.savefig("evolucao_fitness.png", dpi=300)
plt.show()
# Não feitos:




# 8. Documentar os resultados
# 9. Escerver a metodologia. Basicamente é explicar as restrições e como foi adaptado o problema de criação de horário para os códigos em Python usando AG.
# 10. Escrevr os resultados obtidos
# 11. Escrever conclusões.


# Feitos

# 4. Escrever introdução contendo: introdução + objetivos + breve revisão bibliográfica sobre otimização (time tabling) e AG
# 5. Preencher mais professores/disciplinas/horário para gerar mais conflitos com restrições.
# 6. Pesquisar biblioteca para gerar gráficos (Ex: matplotlib)
# 7. Gerar resultados. Gráficos variando os parâmetros (varia um e mantém os outros). Para cada configuração escolhida, rodar umas 15 vezes e tirar a média.