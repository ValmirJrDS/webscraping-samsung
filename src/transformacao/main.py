# Vamos importar o que precisamos 
import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path

# Definir o caminho para o arquivo JSONL
df = pd.read_json('../../data/data.jsonl', lines=True)


# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None
print(df)
# Adicionar a coluna _source com um valor fixo
df['_source'] = 'https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]'
# # Adicionar a coluna _data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()
# # Tratar nulos
df['old_price'] = df['old_price'].fillna('0')
df['new_price'] = df['new_price'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('0')

# Garantir que estão como strings antes de usar .str
df['old_price'] = df['old_price'].astype(str).str.replace('.', '', regex=False)
df['new_price'] = df['new_price'].astype(str).str.replace('.', '', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace('[\(\)]', '', regex=True)
# Converter para numéricos
df['old_price'] = df['old_price'].astype(float)
df['new_price'] = df['new_price'].astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float)
df['reviews_amount'] = df['reviews_amount'].astype(int)
# Salvar os dados em uma tabela
# Manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    (df['old_price'] >= 1000) & (df['old_price'] <= 10000) &
    (df['new_price'] >= 1000) & (df['new_price'] <= 10000)
]
# Conectar (ou criar) banco local
conn = sqlite3.connect('../../data/mercadolivre.db')
df.to_sql('notebook', conn, if_exists='replace', index=False)

# Encerrar conexão
conn.close()