from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao
from AlgoritmoGenetico import AlgoritmoGenetico

print("=" * 60)
print("TESTE 6 — Escola Completa (5 professores, 5 turmas)")
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

# --- Turmas ---
turma1 = Turma("S1A", "M")
turma2 = Turma("S3",  "N")
turma3 = Turma("S1B", "M")
turma4 = Turma("S2",  "N")
turma5 = Turma("S4",  "M")

# --- Disciplinas ---

# pest = Disciplina("pest",  3, "prog estruturada", 2, True)
# web1 = Disciplina("web1", 4, "des web 1",        2, True)
# artes = Disciplina("artes", 1, "artes",            2, False)
# eufonia_tuba = Disciplina("eufonia_tuba", 2, "eufonia tuba", 1, False)
# leit_musical = Disciplina("leit_musical", 2, "leitura musical", 2, False)


# prof 1
mat1  = Disciplina("mat1",  1, "matematica 1",   2, False)
mat2  = Disciplina("mat2",  2, "matematica 2",    2, False)
mat3  = Disciplina("mat3",  3, "matematica 3",    2, False)
mat4  = Disciplina("mat4",  4, "matematica 4",    2, False)

# prof 2
pest  = Disciplina("pest",  3, "prog estruturada", 2, True)
engen = Disciplina("engen", 3, "eng software",    2, True)
poo   = Disciplina("poo",   3, "prog orientada",  2, True)

# prof 3
fis1  = Disciplina("fis1",  1, "fisica 1",        2, False)
fis2  = Disciplina("fis2",  2, "fisica 2",        2, False)
fis3  = Disciplina("fis3",  3, "fisica 3",        2, False)
fis4  = Disciplina("fis4",  4, "fisica 4",        2, False)

# prof 4
port1 = Disciplina("port1", 1, "portugues 1",     2, False)
port2 = Disciplina("port2", 2, "portugues 2",     2, False)
port3 = Disciplina("port3", 3, "portugues 3",     2, False)
port4 = Disciplina("port4", 4, "portugues 4",     2, False)
ingl1 = Disciplina("ingl1", 1, "ingles 1",        2, False)
ingl2 = Disciplina("ingl2", 2, "ingles 2",        2, False)

# prof 5
hist1 = Disciplina("hist1", 1, "historia 1",      2, False)
hist2 = Disciplina("hist2", 2, "historia 2",      2, False)
hist3 = Disciplina("hist3", 3, "historia 3",      2, False)
hist4 = Disciplina("hist4", 4, "historia 4",      2, False)
ingl3 = Disciplina("ingl3", 3, "ingles 3",        2, False)
ingl4 = Disciplina("ingl4", 4, "ingles 4",        2, False)

# --- Alocações: cada professor recebe APENAS as suas disciplinas ---
alocacoes_prof1 = [(mat1, turma1), (mat2, turma4), (mat3, turma2), (mat4, turma5)]
alocacoes_prof2 = [(pest, turma2), (engen, turma2), (poo, turma2)]
alocacoes_prof3 = [(fis1, turma1), (fis2, turma4), (fis3, turma2), (fis4, turma5)]
alocacoes_prof4 = [(port1, turma3), (port2, turma4), (port3, turma2), (port4, turma5), (ingl1, turma3), (ingl2, turma4)]
alocacoes_prof5 = [(hist1, turma3), (hist2, turma4), (hist3, turma2), (hist4, turma5), (ingl3, turma2), (ingl4, turma5)]

configuracoes = [
    {'professor': prof1, 'alocacoes': alocacoes_prof1, 'salas': salas}, # Thomaz
    {'professor': prof2, 'alocacoes': alocacoes_prof2, 'salas': salas}, # Maria
    {'professor': prof3, 'alocacoes': alocacoes_prof3, 'salas': salas}, # Carlos
    {'professor': prof4, 'alocacoes': alocacoes_prof4, 'salas': salas}, # Ana
    {'professor': prof5, 'alocacoes': alocacoes_prof5, 'salas': salas}, # Luiz
]

populacao = Populacao(tamanho=50, configuracoes=configuracoes)
populacao.gerar()
populacao.avaliar()

populacao.estatisticas()

ag = AlgoritmoGenetico(
    populacao       = populacao,
    taxa_crossover  = 0.9,
    taxa_mutacao    = 0.1,
    tamanho_torneio = 10
)

ag.evoluir(numero_de_geracoes=1000)

populacao.estatisticas()

print("\n--- Melhor horário encontrado ---")
print(populacao.melhor)

print("\n--- Evolução do melhor fitness ---")
historico = ag.historico_melhor_fitness
for i in range(len(historico)):
    if (i + 1) % 10 == 0 or i == 0:
        print("  Geração " + str(i + 1) + ": fitness = " + str(historico[i]))

# 1. Se inscrever no CONNEPI
# 2. Baixar o modelo (https://docs.google.com/document/d/1M6N3LYp6ECwbxcCcYJtKniB0h9iQNGPB/edit)
# 3. Ir preenchendo o modelo com informações básicas (título, nomes, etc)
# 4. Escrever introdução contendo: introdução + objetivos + breve revisão bibliográfica sobre otimização (time tabling) e AG
# 5. Preencher mais professores/disciplinas/horário para gerar mais conflitos com restrições.
# 6. Pesquisar biblioteca para gerar gráficos (Ex: matplotlib)
# 7. Gerar resultados. Gráficos variando os parâmetros (varia um e mantém os outros). Para cada configuração escolhida, rodar umas 15 vezes e tirar a média.
# 8. Documentar os resultados
# 9. Escerver a metodologia. Basicamente é explicar as restrições e como foi adaptado o problema de criação de horário para os códigos em Python usando AG.
# 10. Escrevr os resultados obtidos
# 11. Escrever conclusões.