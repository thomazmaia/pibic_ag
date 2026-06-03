# =============================================================================
# teste_ag_1_fitness.py
# =============================================================================
# OBJETIVO: Entender como a função fitness avalia um horário.
#
# Este teste cria situações propositalmente erradas e corretas,
# e verifica se a função fitness detecta as violações.
#
# O que você vai aprender:
#   - O que é a função fitness
#   - Como ela identifica conflitos de sala e de turma
#   - Por que fitness menor = horário melhor
# =============================================================================

from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Horario import Horario
from Aula import Aula
from fitness import calcular_fitness

print("=" * 55)
print("TESTE 1 — Entendendo a Função Fitness")
print("=" * 55)

# Criamos os objetos básicos
sala_comum = Sala(1, 30, False)
sala_lab   = Sala(2, 20, True)
sala_extra = Sala(3, 30, False)

turma_1a = Turma("1A", "M")
turma_2b = Turma("2B", "M")

mat1 = Disciplina("mat1", 1, "matematica 1", 2, False)
fis1 = Disciplina("fis1", 1, "fisica 1",     2, False)
pest = Disciplina("pest", 3, "programacao",  2, True)

prof1 = Professor(1, "Professor A")
prof2 = Professor(2, "Professor B")

# ---------------------------------------------------------------
# CENÁRIO 1: horário sem nenhum conflito
# Esperamos fitness = 0 (ou muito baixo)
# ---------------------------------------------------------------
print("\n--- Cenário 1: Sem conflitos ---")

grade_a = Horario(prof1, [(mat1, turma_1a)], [sala_comum])
grade_a.grade["SEG"]["M"]["AB"] = Aula((mat1, turma_1a), sala_comum)

grade_b = Horario(prof2, [(fis1, turma_2b)], [sala_extra])
grade_b.grade["TER"]["M"]["AB"] = Aula((fis1, turma_2b), sala_extra)

fitness = calcular_fitness([grade_a, grade_b])
print("Fitness: " + str(fitness))
print("Esperado: 0 ou próximo de 0")

# ---------------------------------------------------------------
# CENÁRIO 2: dois professores na mesma sala ao mesmo tempo
# Esperamos +10 de punição (restrição rígida)
# ---------------------------------------------------------------
print("\n--- Cenário 2: Conflito de sala (dois profs na sala 1, SEG-M-AB) ---")

grade_a = Horario(prof1, [(mat1, turma_1a)], [sala_comum])
grade_a.grade["SEG"]["M"]["AB"] = Aula((mat1, turma_1a), sala_comum)  # sala 1

grade_b = Horario(prof2, [(fis1, turma_2b)], [sala_comum])
grade_b.grade["SEG"]["M"]["AB"] = Aula((fis1, turma_2b), sala_comum)  # sala 1 também!

fitness = calcular_fitness([grade_a, grade_b])
print("Fitness: " + str(fitness))
print("Esperado: >= 10 (punição por sala dupla)")

# ---------------------------------------------------------------
# CENÁRIO 3: mesma turma com dois professores ao mesmo tempo
# Esperamos +10 de punição
# ---------------------------------------------------------------
print("\n--- Cenário 3: Conflito de turma (turma 1A com dois profs ao mesmo tempo) ---")

grade_a = Horario(prof1, [(mat1, turma_1a)], [sala_comum])
grade_a.grade["SEG"]["M"]["AB"] = Aula((mat1, turma_1a), sala_comum)

grade_b = Horario(prof2, [(fis1, turma_1a)], [sala_extra])  # turma_1a de novo!
grade_b.grade["SEG"]["M"]["AB"] = Aula((fis1, turma_1a), sala_extra)

fitness = calcular_fitness([grade_a, grade_b])
print("Fitness: " + str(fitness))
print("Esperado: >= 10 (punição por turma em dois lugares)")

# ---------------------------------------------------------------
# CENÁRIO 4: disciplina técnica em sala comum (erro de sala)
# Esperamos +10 de punição
# ---------------------------------------------------------------
print("\n--- Cenário 4: Disciplina técnica em sala comum ---")

grade_a = Horario(prof1, [(pest, turma_1a)], [sala_comum])
grade_a.grade["SEG"]["M"]["AB"] = Aula((pest, turma_1a), sala_comum)  # pest é técnica mas sala é comum!

fitness = calcular_fitness([grade_a])
print("Fitness: " + str(fitness))
print("Esperado: >= 10 (punição por sala incompatível)")

print("\n" + "=" * 55)
print("Conclusão: quanto MAIOR o fitness, PIOR o horário.")
print("O AG vai tentar encontrar horários com fitness = 0.")
print("=" * 55)
