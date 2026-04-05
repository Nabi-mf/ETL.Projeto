import pandas as pd
from extract import df_products, df_users, df_carts, df_posts, df_comments, df_recipes, df_todos

def transform_product(df: pd.DataFrame) -> pd.DataFrame:
     #1 Selecionando só os que importam:
    df = df[[
        "id",
        "title",
        "category",
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "brand",
        "availabilityStatus"
    ]]
    #2 Renomeia para nomes mais claros
    #df[[Colunas]] - filtrar só as colunas que listei

    df = df.rename(columns={
        'title': 'nome_produto',
        'discountPercentage': 'desconto_pct',
        'availabilityStatus': 'status_estoque',
        'price': 'preco',
        'rating': 'avaliacao',
        'stock': 'estoque',
        'category': 'categoria',
        'brand': 'marca'
    })
     # 3. Remove linhas com valores nulos
    df = df.dropna()
    return df

def transform_user(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[
        'id',
        'firstName',
        'lastName',
        'email',
        'gender',
        'age'
    ]]

    df = df.rename(columns={
        'firstName': 'nome',
        'lastName': 'sobrenome',
        'email': 'email',
        'gender': 'genero',
        'age': 'idade'
    })
    df = df.dropna()
    return df

def transform_carts(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['id', 'userId', 'total', 'discountedTotal', 'totalProducts', 'totalQuantity']]
    df = df.rename(columns={
        'userId':          'id_usuario',
        'total':           'valor_total',
        'discountedTotal': 'valor_com_desconto',
        'totalProducts':   'qtd_produtos',
        'totalQuantity':   'qtd_itens'
    })
    df = df.dropna()
    return df

def transform_posts(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['id', 'title', 'userId', 'views']]
    df = df.rename(columns={
        'title':  'titulo',
        'userId': 'id_usuario'
    })
    df = df.dropna()
    return df

def transform_comments(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['id', 'body', 'postId', 'likes']]
    df = df.rename(columns={
        'body':   'comentario',
        'postId': 'id_post'
    })
    df = df.dropna()
    return df

def transform_recipes(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['id', 'name', 'cuisine', 'difficulty', 
             'caloriesPerServing', 'rating', 'prepTimeMinutes', 'cookTimeMinutes']]
    df = df.rename(columns={
        'name':               'nome_receita',
        'cuisine':            'culinaria',
        'difficulty':         'dificuldade',
        'caloriesPerServing': 'calorias_porcao',
        'prepTimeMinutes':    'tempo_preparo_min',
        'cookTimeMinutes':    'tempo_cozimento_min'
    })
    df = df.dropna()
    return df

def transform_todos(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['id', 'todo', 'completed', 'userId']]
    df = df.rename(columns={
        'todo':      'tarefa',
        'completed': 'concluido',
        'userId':    'id_usuario'
    })
    df = df.dropna()
    return df

df_products_clean = transform_product(df_products)
df_users_clean    = transform_user(df_users)
df_carts_clean    = transform_carts(df_carts)
df_posts_clean    = transform_posts(df_posts)
df_comments_clean = transform_comments(df_comments)
df_recipes_clean  = transform_recipes(df_recipes)
df_todos_clean    = transform_todos(df_todos)

print("PRODUCTS:", df_products_clean.shape)
print("USERS:",    df_users_clean.shape)
print("CARTS:",    df_carts_clean.shape)
print("POSTS:",    df_posts_clean.shape)
print("COMMENTS:", df_comments_clean.shape)
print("RECIPES:",  df_recipes_clean.shape)
print("TODOS:",    df_todos_clean.shape)

print("Todas as transformações foram concluídas com sucesso!")