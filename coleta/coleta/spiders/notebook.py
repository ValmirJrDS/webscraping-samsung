import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]"]

   # Método parse - função principal que processa a resposta das requisições
    def parse(self, response):
        # Extrai todos os elementos HTML que contêm os produtos usando um seletor CSS
        # Procura por divs com a classe 'ui-search-result__wrapper'
        products = response.css('div.ui-search-result__wrapper')

        # Itera sobre cada produto encontrado na página
        for product in products:
            # Para cada produto, extrai e retorna um dicionário com as informações desejadas
            # Neste caso, está extraindo apenas a marca do notebook
            yield {
                # Extrai o texto dentro do elemento span com a classe 'poly-component__brand'
                'brand': product.css('span.poly-component__brand::text').get()
                # O método get() retorna o primeiro elemento encontrado ou None se não existir
            }
            
        # OBS: O uso de 'yield' permite que o Scrapy processe os itens um por um,
        # economizando memória em comparação com o retorno de uma lista completa

        
