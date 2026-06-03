# =============================================================================
# teste_ag_5_parametros.py
# =============================================================================
# OBJETIVO: Comparar como diferentes parâmetros afetam o AG.
#
# Os parâmetros do AG são como os "botões" que controlam o comportamento
# do algoritmo. Este teste roda o AG com configurações diferentes e
# compara os resultados.
#
# O que você vai aprender:
#   - O efeito de diferentes taxas de crossover e mutação
#   - O efeito de diferentes tamanhos de população
#   - Como escolher bons parâmetros para o seu problema
# =============================================================================

from Disciplina import Disciplina
from Professor import Professor
from Sala import Sala
from Turma import Turma
from Populacao import Populacao
from AlgoritmoGenetico import AlgoritmoGenetico

# --- Dados fixos do cenário ---
def criar_configuracoes():
    """
    Cria os objetos do cenário de teste.
    Chamamos essa função várias vezes para garantir que cada experimento
    começa do zero (sem estado compartilhado entre execuções).
    """
    salas = [
        Sala(1, 30, False),
        Sala(2, 30, False),
        Sala(3, 25, True),
        Sala(4, 25, True),
    ]

    prof1 = Professor(1, "Gabriel Ramos")
    prof1.setHorarios_Bloqueados(("SEG", "M", "AB"))
    prof1.setHorarios_Bloqueados(("SEX", "N", "CD"))

    prof2 = Professor(2, "Helena Pires")
    prof2.setHorarios_Bloqueados(("TER", "N", "AB"))
    prof2.setHorarios_Bloqueados(("QUA", "M", "CD"))

    prof3 = Professor(3, "Igor Matos")
    prof3.setHorarios_Bloqueados(("QUI", "M", "AB"))

    turma1 = Turma("S1", "M")
    turma2 = Turma("S2", "T")
    turma3 = Turma("S3", "N")

    mat1 = Disciplina("mat1", 1, "matematica 1", 2, False)
    fis1 = Disciplina("fis1", 1, "fisica 1",     2, False)
    poo  = Disciplina("poo",  2, "poo",           2, True)
    pest = Disciplina("pest", 2, "programacao",   2, True)
    port = Disciplina("port", 1, "portugues",     2, False)

    configuracoes = [
        {
            'professor': prof1,
            'alocacoes': [(mat1, turma1), (fis1, turma2)],
            'salas':     salas
        },
        {
            'professor': prof2,
            'alocacoes': [(poo, turma1), (pest, turma3)],
            'salas':     salas
        },
        {
            'professor': prof3,
            'alocacoes': [(port, turma2), (port, turma3)],
            'salas':     salas
        },
    ]
    return configuracoes


def rodar_experimento(nome, tamanho_pop, taxa_crossover, taxa_mutacao, tamanho_torneio, geracoes):
    """Roda um experimento completo e retorna o melhor fitness obtido."""
    configuracoes = criar_configuracoes()

    populacao = Populacao(tamanho=tamanho_pop, configuracoes=configuracoes)
    populacao.gerar()
    populacao.avaliar()

    fitness_inicial = populacao.melhor.fitness

    ag = AlgoritmoGenetico(
        populacao       = populacao,
        taxa_crossover  = taxa_crossover,
        taxa_mutacao    = taxa_mutacao,
        tamanho_torneio = tamanho_torneio
    )

    # Suprime a saída detalhada do AG para este teste de comparação
    import io, sys
    saida_original = sys.stdout
    sys.stdout = io.StringIO()
    ag.evoluir(geracoes)
    sys.stdout = saida_original

    fitness_final = populacao.melhor.fitness
    return fitness_inicial, fitness_final


print("=" * 60)
print("TESTE 5 — Comparando Parâmetros do AG")
print("=" * 60)
print("Cada experimento roda 20 gerações. Comparamos o fitness final.")
print("-" * 60)

GERACOES = 20

# Experimento 1: configuração padrão
print("\nExperimento 1: configuração padrão")
print("  pop=8 | crossover=0.8 | mutação=0.1 | torneio=3")
fi, ff = rodar_experimento("padrão", 8, 0.8, 0.1, 3, GERACOES)
print("  Fitness inicial: " + str(fi) + " → Fitness final: " + str(ff))

# Experimento 2: mutação mais alta
print("\nExperimento 2: mutação alta")
print("  pop=8 | crossover=0.8 | mutação=0.4 | torneio=3")
fi, ff = rodar_experimento("mutação alta", 8, 0.8, 0.4, 3, GERACOES)
print("  Fitness inicial: " + str(fi) + " → Fitness final: " + str(ff))

# Experimento 3: crossover baixo
print("\nExperimento 3: crossover baixo (mais exploração aleatória)")
print("  pop=8 | crossover=0.3 | mutação=0.1 | torneio=3")
fi, ff = rodar_experimento("crossover baixo", 8, 0.3, 0.1, 3, GERACOES)
print("  Fitness inicial: " + str(fi) + " → Fitness final: " + str(ff))

# Experimento 4: população maior
print("\nExperimento 4: população maior (mais diversidade)")
print("  pop=20 | crossover=0.8 | mutação=0.1 | torneio=3")
fi, ff = rodar_experimento("pop maior", 20, 0.8, 0.1, 3, GERACOES)
print("  Fitness inicial: " + str(fi) + " → Fitness final: " + str(ff))

# Experimento 5: torneio menor (menos pressão seletiva)
print("\nExperimento 5: torneio pequeno (menos pressão seletiva)")
print("  pop=8 | crossover=0.8 | mutação=0.1 | torneio=2")
fi, ff = rodar_experimento("torneio 2", 8, 0.8, 0.1, 2, GERACOES)
print("  Fitness inicial: " + str(fi) + " → Fitness final: " + str(ff))

print("\n" + "=" * 60)
print("Dicas para interpretar os resultados:")
print("  - Fitness menor = horário melhor")
print("  - Mutação alta → mais exploração, mas pode desconstruir boas soluções")
print("  - Crossover baixo → menos recombinação, evolução mais lenta")
print("  - População maior → mais diversidade, mas demora mais por geração")
print("  - Torneio menor → mais diversidade mantida na população")
print("=" * 60)
