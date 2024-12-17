class Aviao:
    
    cor = "Azul"

    def __init__(self, modelo, velocidade_maxima, capacidade):
        self.modelo = modelo
        self.velocidade_maxima = velocidade_maxima
        self.capacidade = capacidade


avioes = [
    Aviao("BOIENG456", "1500 km/h", 400),
    Aviao("Embraer Praetor 600", "863 km/h", 14),
    Aviao("Antonov An-2", "258 km/h", 12),
]


for aviao in avioes:
    print(
        f"O avião de modelo {aviao.modelo} possui uma velocidade máxima de {aviao.velocidade_maxima}, "
        f"capacidade para {aviao.capacidade} passageiros e é da cor {aviao.cor}."
    )
