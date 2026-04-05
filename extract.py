import requests
import pandas as pd

BASE_URL = "https://dummyjson.com" #Api de teste para produtos, usuários e outros dados fictícios

def extract(resource: str) -> pd.DataFrame:
    all_records = []
    skip = 0
    limit = 100

    while True:
        url = f"{BASE_URL}/{resource}"
        response = requests.get(url, params={"limit": limit, "skip": skip})

        if response.status_code == 200:
            data = response.json()

            records = data[resource]
            total   = data["total"]

            all_records.extend(records)
            skip += limit

            print(f"[{resource}] extraídos {len(all_records)}/{total}")

            if skip >= total:
                break

        else:
            print(f"Erro ao chamar a API: status {response.status_code}")
            break

    return pd.DataFrame(all_records)

# Extrai todos os recursos
df_products = extract("products")
df_users    = extract("users")
df_carts    = extract("carts")
df_posts    = extract("posts")
df_comments = extract("comments")
df_recipes  = extract("recipes")
df_todos    = extract("todos")

print("Extração concluída!")

print("PRODUCTS:", df_products.shape)
print("USERS:",    df_users.shape)
print("CARTS:",    df_carts.shape)
print("POSTS:",    df_posts.shape)
print("COMMENTS:", df_comments.shape)
print("RECIPES:",  df_recipes.shape)
print("TODOS:",    df_todos.shape)

print("Todas as extrações foram concluídas com sucesso!")
