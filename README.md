# 📘 1 - Coleta de Dados com Scrapy — Mercado Livre Notebooks
# 📘 2 - Hospedagem do BD no Digital Ocean para utilização em projetos de N8N

Este guia documenta o passo a passo completo de um projeto real de scraping de produtos (notebooks) no site do Mercado Livre, utilizando **Scrapy**, uma das ferramentas mais poderosas de coleta de dados com Python.

---

## 🔧 Etapa 1 — Instalar o Scrapy

```bash
pip install scrapy
```

Instalamos o Scrapy, que é um framework robusto para criação de spiders (robôs de coleta de dados). Ele permite navegar por páginas HTML, extrair dados com seletores CSS ou XPath, lidar com paginação, entre outros.

---

## 🏗️ Etapa 2 — Criar o Projeto

```bash
scrapy startproject mercadolivre
```

Esse comando cria a estrutura inicial do projeto, com os diretórios:
- `spiders/`: onde ficam os crawlers
- `settings.py`: onde configuramos o comportamento do bot
- `items.py`: (opcional) definição da estrutura de dados
- `middlewares.py`: interceptadores de requisição/resposta

---

## 📂 Etapa 3 — Entrar no Projeto

```bash
cd mercadolivre
```

---

## 🧬 Etapa 4 — Criar a Spider

```bash
scrapy genspider notebook mercadolivre.com.br
```

Criamos uma spider chamada `notebook` voltada para o domínio do Mercado Livre. A spider será criada dentro de `mercadolivre/spiders/notebook.py`.

---

## 🐚 Etapa 5 — Testar no Shell do Scrapy

```bash
scrapy shell
```

Esse modo nos dá um ambiente interativo para testar seletores, verificar HTML da página e debugar.

---

## 🔍 Etapa 6 — Tentar fazer um `fetch()`

```python
fetch("https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]")
```

Esse comando busca a página desejada. Se o retorno for `403 Forbidden`, significa que o site está bloqueando o acesso automatizado.

---

## 🕵️ Etapa 7 — Adicionar o User-Agent

### O que é `User-Agent`?

É uma string que identifica o tipo de cliente que está acessando o site (navegador, sistema, etc). Sites como o Mercado Livre bloqueiam robôs, mas permitem navegadores comuns.

```python
# settings.py
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
```

Com isso, nosso bot finge ser um navegador legítimo.

---

## 🧠 Etapa 8 — Revisar Middlewares (opcional)

```python
# settings.py (mantido padrão nesse projeto)
DOWNLOADER_MIDDLEWARES = {
   # pode ser customizado caso precise alterar headers, usar proxy, etc.
}
```

---

## 🧪 Etapa 9 — Retestando com `scrapy shell`

```python
fetch("https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]")
response
response.text
```

Verificamos se conseguimos acessar o HTML corretamente e começamos a testar os seletores.

---

## 🔎 Etapa 10 — Testar seletores

```python
response.css('div.ui-search-result__wrapper')
```

```python
len(response.css('div.ui-search-result__wrapper'))
```

```python
products = response.css('div.ui-search-result__wrapper')
products[0].css('span.poly-component__brand::text').get()
```

Encontramos os dados e validamos que conseguimos extrair marca, nome, preço, avaliações, etc.

---

## 🧱 Etapa 11 — Transformar os testes em código

Criamos o crawler programático com os seletores testados, salvando os dados como JSON.

```bash
scrapy crawl notebook -o data.json
```

---

## 💸 Etapa 12 — Coletar os preços corretamente

```python
prices = products[0].css('span.andes-money-amount__fraction::text').getall()
```

Isso retorna todos os valores de preços (antigo, novo, desconto, etc). Precisamos selecionar corretamente:

```python
old_price = prices[0] if len(prices) > 0 else None
new_price = prices[1] if len(prices) > 1 else None
```

---

## 📁 Etapa 13 — Salvar os dados fora da pasta do projeto

```bash
scrapy crawl notebook -o ../data/data.json
```

Organizamos os dados coletados na pasta `data/`, fora do diretório `mercadolivre`.

---

## 📦 Etapa 14 — Organizar o projeto em camadas

Criamos subpastas para manter a estrutura do pipeline mais clara e modular:

```
src/
│
├── coleta/          <- spiders, dados brutos
├── transformacao/   <- tratamento dos dados
├── dashboard/       <- visualizações e relatórios
```

---

## 🔁 Etapa 15 — Paginação

Adicionamos suporte para múltiplas páginas, buscando o botão “Próxima Página”:

```python
next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
yield scrapy.Request(url=next_page, callback=self.parse)
```

- `url` = link para a próxima página
- `callback` = função que será chamada ao carregar a nova página

---

## 🔐 Etapa 16 — Evitar bloqueio

Limitamos a quantidade de páginas para não abusar do site:

```python
page_count = 1
max_pages = 10
```

---

## 🤖 Etapa 17 — Respeitar `robots.txt`?

Por padrão:

```python
ROBOTSTXT_OBEY = True
```

Isso impede que o scraper acesse URLs proibidas no `robots.txt` do site. No Mercado Livre, várias URLs são bloqueadas por padrão. Podemos **desabilitar** isso em projetos internos:

```python
ROBOTSTXT_OBEY = False
```

---

## ✅ Etapa 18 — Rodar a coleta final

```bash
scrapy crawl notebook -o ../data/data.json
```

Agora, a spider coleta notebooks com nome, marca, preço, avaliações e vendedor, navegando por até 10 páginas.

---

## 🏁 Finalizamos a coleta!

# Logo que conclui a coleta e a a criação do Banco de Dados, subi o mesmo para o DIGITAL OCEAN. Segue abaixo a documentação de como fiz:

## 📊 Documentação de Implantação do Banco de Dados PostgreSQL

Esta documentação descreve o processo de configuração e resolução de problemas para implantar o **PostgreSQL** em uma máquina virtual, e os comandos necessários para iniciar o banco de dados a partir de um arquivo `.sql`.

---

### 🛠 Passo 1: Instalação do PostgreSQL

**1. Instalação do PostgreSQL:**

Para instalar o PostgreSQL na máquina:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**2. Verificação da versão instalada:**

```bash
psql --version
```

Saída esperada:

```bash
psql (PostgreSQL) 16.8 (Ubuntu 16.8-0ubuntu0.24.10.1)
```

---

### 🛠 Passo 2: Configuração de Acesso Externo

**1. Edite o arquivo de configuração `postgresql.conf` para permitir conexões externas:**

```bash
sudo vim /etc/postgresql/16/main/postgresql.conf
```

**2. Modifique a linha `listen_addresses` para permitir conexões de qualquer IP ou do IP específico da máquina que irá se conectar:**

De:

```conf
#listen_addresses = 'localhost'
```

Para:

```conf
listen_addresses = '*'
```

**3. Edite o arquivo `pg_hba.conf` para permitir autenticação de IPs externos:**

```bash
sudo vim /etc/postgresql/16/main/pg_hba.conf
```

**4. Adicione a seguinte linha ao final do arquivo para permitir conexões via IP:**

```conf
host all all 0.0.0.0/0 md5
```

---

### 🛠 Passo 3: Reiniciar o PostgreSQL

**1. Reinicie o serviço PostgreSQL para aplicar as mudanças de configuração:**

```bash
sudo systemctl restart postgresql
```

**2. Verifique o status do serviço para garantir que está funcionando corretamente:**

```bash
sudo systemctl status postgresql
```

Saída esperada (se o serviço estiver ativo e em execução):

```yaml
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: enabled)
     Active: active (running) since Thu 2025-04-24 14:09:31 UTC; 3min 38s ago
```

---

### 🛠 Passo 4: Verificação de Conexão de Rede

**1. Verifique se o PostgreSQL está escutando na porta 5432 (porta padrão do PostgreSQL):**

```bash
sudo ss -plnt | grep 5432
```

Caso não obtenha resultado, verifique novamente as configurações no `postgresql.conf` e `pg_hba.conf`.

**2. Verifique a conexão com a máquina externa via telnet:**

```bash
telnet valmirjuniored.ddns.net 5432
```

Se a conexão for recusada, reforce a configuração de rede (no firewall, na configuração do PostgreSQL e no arquivo de configuração do sistema operacional).

---

### 🛠 Passo 5: Criação de Credenciais para o n8n

**1. Criação de um novo usuário no PostgreSQL:**

Para permitir o acesso ao banco de dados, crie um novo usuário no PostgreSQL com os seguintes comandos:

```bash
sudo -u postgres psql
CREATE USER n8n_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mercadolivre TO n8n_user;
\q
```

**2. Verifique a criação do usuário:**

Dentro do `psql`:

```bash
sudo -u postgres psql
\du
```

Isso irá listar todos os usuários, e você deve ver o `n8n_user` listado.

---

### 🛠 Passo 6: Carregamento do Banco de Dados a Partir de um Arquivo `.sql`

**1. Carregue o arquivo `.sql` no banco de dados com o seguinte comando:**

```bash
sudo -u postgres psql mercadolivre < /path/to/mercadolivre.sql
```

Certifique-se de que o caminho para o arquivo `.sql` está correto.

**2. Verifique se os dados foram carregados corretamente:**

```bash
sudo -u postgres psql
\c mercadolivre
\dt
```

Isso irá mostrar as tabelas do banco de dados carregado.

---

## ⚠️ Resolução de Problemas Encontrados

**1. PostgreSQL não está escutando na porta 5432**

Sintoma: A conexão não foi estabelecida e o comando `telnet` retornou erro de conexão recusada.

Solução:
- Verifique os arquivos de configuração (`postgresql.conf` e `pg_hba.conf`) e corrija a linha `listen_addresses`.
- Reinicie o PostgreSQL para aplicar as alterações.
- Verifique o firewall e as regras de segurança do sistema operacional.

**2. Erro no arquivo `postgresql.conf` (invalid line)**

Sintoma: O serviço não foi iniciado corretamente e exibiu erro em uma linha específica do arquivo de configuração.

Solução:
- Edite o arquivo `postgresql.conf` e corrija a linha indicada na mensagem de erro (geralmente relacionado a parâmetros mal configurados, como `listen_addresses`).
- Reinicie o serviço PostgreSQL.

**3. Erro ao iniciar o PostgreSQL após editar os arquivos de configuração**

Sintoma: O PostgreSQL não inicializa após a modificação dos arquivos de configuração.

Solução:
- Verifique a sintaxe e formatação dos arquivos de configuração.
- Verifique os logs de erro com `journalctl -xeu postgresql@16-main.service` para obter mais detalhes e resolver problemas específicos.

---

## 💻 Resumo dos Comandos Utilizados

```bash
# Para instalar o PostgreSQL:
sudo apt update
sudo apt install postgresql postgresql-contrib

# Para editar os arquivos de configuração:
sudo vim /etc/postgresql/16/main/postgresql.conf
sudo vim /etc/postgresql/16/main/pg_hba.conf

# Para criar um novo usuário no PostgreSQL:
sudo -u postgres psql
CREATE USER n8n_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mercadolivre TO n8n_user;
\q

# Para carregar o arquivo SQL:
sudo -u postgres psql mercadolivre < /path/to/mercadolivre.sql

# Para verificar o status do PostgreSQL:
sudo systemctl status postgresql

# Para verificar a conexão na porta 5432:
sudo ss -plnt | grep 5432
```

Esta documentação deve servir como guia para qualquer nova implantação ou para a recuperação de possíveis falhas. Ela inclui o processo completo de configuração e as verificações essenciais para garantir que o PostgreSQL esteja funcionando corretamente.



O próximo passo é criar transformações (por exemplo, limpeza de preços e normalização dos nomes) e visualizações (como dashboards com Streamlit, Dash ou Power BI).



Quer seguir nessa linha agora?
