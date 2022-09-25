from statistics import mean
import json

# Map
## 1. Deixar tudo maiúsculo str.upper
# Exemplo: str.upper("oioi") -> 'OIOI'
## 2. Split de nome e sobrenomes
# Exemplo
# str.split("Oi tudo bem?") -> ['Oi', 'tudo', 'bem?']

# reduce
# Contar quantidade de nomes

# mapper
# Contar quantos Joãos há na lista

# Rodar
# python main.py nomes.txt > joaos.txt

from mrjob.job import MRJob
from mrjob.step import MRStep


class Pokemon(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_dano, reducer=self.reducer_dano)
        ]

    def mapper_tipo(self, _, linha):
      pokemons = json.loads(linha)
      yield pokemons['tipos'][0],1

    def reducer_tipo(self, chave, valores):
        yield (chave, sum(valores))

    def mapper_dano(self, _, linha):
      pokemons = json.loads(linha)
      for key, value in pokemons['dano_recebido'].items():
        yield key, value

    def reducer_dano(self, chave, valores):
        yield (chave, mean(valores))

if __name__ == '__main__':
    Pokemon.run()