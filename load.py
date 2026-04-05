from sqlalchemy import create_engine
from transform import (
    df_products_clean,
    df_users_clean,
    df_carts_clean,
    df_posts_clean,
    df_comments_clean,
    df_recipes_clean,
    df_todos_clean
)

# Credenciais do PostgreSQL
usuario = "postgres"
senha   = "" #sua senha aqui
host    = "localhost"
porta   = "5432"
banco   = "projeto_dados"

# Conexão
engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")

def load(df, nome_tabela: str):
    df.to_sql(
        name      = nome_tabela,
        con       = engine,
        if_exists = "replace",
        index     = False
    )
    print(f"Tabela '{nome_tabela}' carregada com sucesso!")

# Carrega
load(df_products_clean, "produtos")
load(df_users_clean,    "usuarios")
load(df_carts_clean,    "carrinhos")
load(df_posts_clean,    "posts")
load(df_comments_clean, "comentarios")
load(df_recipes_clean,  "receitas")
load(df_todos_clean,    "tarefas")

print("Todas as tabelas foram carregadas com sucesso!")