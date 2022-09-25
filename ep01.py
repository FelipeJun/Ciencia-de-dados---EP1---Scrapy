import scrapy
from json import dump

class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'

  #para pegar os tipos do pokemon: pegar a href, fazendo um regex
  start_urls = ['https://www.serebii.net/pokedex/001.shtml']

  # www.serebii.net/pokedex/grass.shtml
  def get_atribbute_from_link(self, link):
    comeco = link.rfind("/") +1
    fim = link.rfind(".")
    return link[comeco:fim]
  
  def parse(self, response):
    id =  (response.css("td.fooinfo::text").getall()[3]).replace("#", '')
    tipos = response.css("td.footype").xpath(".//a/@href").getall()
    dano = response.css("td.footype::text").getall()[-15:]
    tipos_pokemon = response.css("td.cen").xpath(".//a/@href").getall()
    id_evolucao = ''

    for index, value in enumerate(dano):
      dano[index] = float(value.replace("*",""))

    for i in range(len(tipos_pokemon)):
      link = tipos_pokemon[i]
      tipos_pokemon[i] = self.get_atribbute_from_link(link)

    tipagem = []
    for i in range(len(tipos)):
      link = tipos[i]
      tipagem.append(self.get_atribbute_from_link(link)) 

    dano_recebido = {}
    for i in range(len(tipos)):
      dano_recebido[tipagem[i]] = dano[i]

    #vefica se é uma eevee ou alguma evolução sua 
    if id == '133':
      evolucoes = response.xpath("*//td[@class='pkmn']/a/@href").getall()[-3:] 
      for i in range(len(evolucoes)):
        link = evolucoes[i]
        id_evolucao += self.get_atribbute_from_link(link)+' '

    elif id in ['134','135','136']:
      id_evolucao = ''
    else:
      evolucoes = response.css("table.evochain").xpath(".//a/@href").getall()  
      for i in range(len(evolucoes)):
        link = evolucoes[i]
        evolucoes[i] = self.get_atribbute_from_link(link)
      valor = evolucoes.index(id)
      try:
        prox = evolucoes[valor+1]
        id_evolucao = prox
      except:
        pass
  
    yield {"id" :id,
      "nome" : response.css("td.fooinfo::text").getall()[2],
      "altura" : (response.css("td.fooinfo::text").getall()[6]).strip(),
      "peso" : (response.css("td.fooinfo::text").getall()[8]).strip(),
      "tipos": tipos_pokemon,
      "dano_recebido":dano_recebido,
      "id_evolucao":id_evolucao
    }
  
    prox_pagina = response.xpath("//td[@align='center']/a/@href").getall()[-1]

    if prox_pagina == None:
      print("PAGINA NAO ENCONTRADA")
    else:
      novo_request = response.urljoin(prox_pagina)
      yield scrapy.Request(novo_request, callback=self.parse)


