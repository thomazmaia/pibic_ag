class Sala:

    def __init__(self,
                 num_sala: int,
                 capacidade: int,
                 laboratorio: bool):

        self.num_sala = num_sala
        self.capacidade = capacidade
        self.laboratorio = laboratorio

        # ocupações da sala
        self.ocupacoes = {}

    def ocupar(self, dia, turno, slot):

        if dia not in self.ocupacoes:
            self.ocupacoes[dia] = {}

        if turno not in self.ocupacoes[dia]:
            self.ocupacoes[dia][turno] = {}

        self.ocupacoes[dia][turno][slot] = True

    def esta_ocupada(self, dia, turno, slot):

        return (
            dia in self.ocupacoes and
            turno in self.ocupacoes[dia] and
            slot in self.ocupacoes[dia][turno]
        )

    def limpar_ocupacao(self):
        # Deve ser chamado antes de gerar cada novo individuo,
        # para que a ocupacao de uma grade nao contamine a proxima.
        self.ocupacoes = {}

    def __repr__(self):
        return f"Sala {self.num_sala}"