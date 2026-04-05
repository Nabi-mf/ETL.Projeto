# 🔄 ETL Pipeline — DummyJSON para PostgreSQL

> Pipeline ETL completo em Python que extrai dados da API DummyJSON, transforma e carrega no PostgreSQL — pronto para análise de dados e dashboards.

> A API simula um e-commerce completo com produtos, usuários, carrinhos, posts, receitas e tarefas

---

## 📌 Sobre o Projeto

Este projeto consome dados de 7 recursos da [DummyJSON API](https://dummyjson.com/), realiza a limpeza e organização dos dados, e os carrega em um banco PostgreSQL estruturado para análise de negócios.

```
🌐 API DummyJSON  →  📥 Extract  →  🔧 Transform  →  📤 Load  →  🗄️ PostgreSQL
```

---

## 🧱 Estrutura do Projeto

```
📁 projeto/
├── 📄 extract.py      # Busca os dados brutos da API
├── 📄 transform.py    # Limpa e organiza os dados
└── 📄 load.py         # Carrega os dados no PostgreSQL
```

---

## ⚙️ Tecnologias

| Tecnologia | Uso |
|---|---|
| 🐍 Python | Linguagem principal |
| 🐼 pandas | Manipulação dos dados |
| 🌐 requests | Requisições HTTP |
| 🔌 SQLAlchemy | Conexão com o banco |
| 🐘 PostgreSQL | Banco de dados de destino |
| 🧪 DummyJSON | Fonte dos dados |

---

## 📥 Extract

Responsável por **buscar os dados brutos da API** com paginação automática.

A API retorna 100 registros por vez. O extract faz um loop até buscar tudo:

```python
def extract(resource: str) -> pd.DataFrame:
    all_records = []
    skip = 0
    limit = 100

    while True:
        url = f"{BASE_URL}/{resource}"
        response = requests.get(url, params={"limit": limit, "skip": skip})

        if response.status_code == 200:
            # processa e avança para próxima página
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
```

### 📦 Recursos extraídos

| Recurso | Registros | Descrição |
|---|---|---|
| 🛍️ products | 194 | Produtos com preço, estoque e avaliação |
| 👤 users | 208 | Usuários com dados demográficos |
| 🛒 carts | 50 | Carrinhos de compra |
| 📝 posts | 251 | Publicações |
| 💬 comments | 340 | Comentários |
| 🍽️ recipes | 50 | Receitas culinárias |
| ✅ todos | 254 | Tarefas |

---

## 🔧 Transform

Responsável por **limpar e organizar** os dados brutos em 3 passos:

```
1️⃣ Seleciona   →  apenas as colunas que importam para análise
2️⃣ Renomeia    →  nomes claros em português
3️⃣ Limpa       →  remove linhas com valores nulos (dropna)
```

### 🗂️ Tabelas geradas

| Tabela | Colunas principais | ❓ Pergunta de negócio |
|---|---|---|
| 🛍️ produtos | id, nome, categoria, preco, desconto_pct, avaliacao, estoque, marca | Quais categorias têm maior valor em estoque? |
| 👤 usuarios | id, nome, sobrenome, email, genero, idade | Qual perfil de usuário compra mais? |
| 🛒 carrinhos | id, id_usuario, valor_total, valor_com_desconto, qtd_itens | Quanto cada usuário gastou? |
| 📝 posts | id, titulo, id_usuario, views | Quais posts têm mais visualizações? |
| 💬 comentarios | id, comentario, id_post, likes | Quais comentários têm mais engajamento? |
| 🍽️ receitas | id, nome, culinaria, dificuldade, calorias_porcao, avaliacao | Receitas com menor caloria e tempo? |
| ✅ tarefas | id, tarefa, concluido, id_usuario | Taxa de conclusão por usuário? |

---

## 📤 Load

Responsável por **carregar os DataFrames limpos no PostgreSQL**.

```python
def load(df, nome_tabela: str):
    df.to_sql(
        name      = nome_tabela,
        con       = engine,
        if_exists = "replace",  # recria a tabela a cada execução
        index     = False
    )
    print(f"✅ Tabela '{nome_tabela}' carregada com sucesso!")
```

---

## 🚀 Como Executar

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2️⃣ Instale as dependências
```bash
pip install requests pandas sqlalchemy psycopg2-binary
```

### 3️⃣ Configure as credenciais no `load.py`
```python
usuario = "postgres"
senha   = "sua_senha"
host    = "localhost"
porta   = "5432"
banco   = "projeto_dados"
```

### 4️⃣ Crie o banco no PostgreSQL
```sql
CREATE DATABASE projeto_dados;
```

### 5️⃣ Execute o pipeline
```bash
python load.py
```

Ao final você verá:
```
✅ Todas as tabelas foram carregadas com sucesso!
```

---

## 🗺️ Próximas Etapas

- [ ] 🗄️ Validar tabelas no pgAdmin com queries SQL
- [ ] 📊 Conectar PostgreSQL a uma ferramenta de BI (Power BI, Metabase ou Looker Studio)
- [ ] 📈 Responder as perguntas de negócio com dashboards

---

## ❓ Perguntas de Negócio 

As análises que este projeto busca responder com os dados carregados no PostgreSQL:

### 🛍️ Produtos
- Quais **categorias de produto** têm maior valor total em estoque?
- Quais produtos têm a **melhor avaliação** combinada com o **maior desconto**?
- Qual a **faixa de preço** mais comum entre os produtos disponíveis?
- Quais marcas têm produtos com **baixo estoque** e alta avaliação?

### 👤 Usuários
- Qual **gênero** realiza mais compras?
- Qual a **faixa etária** que mais aparece nos carrinhos?
- Qual a distribuição de usuários por **idade**?

### 🛒 Carrinhos
- Quais usuários têm o **maior valor total** de compras?
- Qual a **diferença média** entre valor total e valor com desconto?
- Qual a **média de itens** por carrinho?

### 📝 Posts & 💬 Comentários
- Quais posts têm o **maior número de visualizações**?
- Quais comentários receberam **mais curtidas**?
- Qual usuário **mais posta** conteúdo?

### 🍽️ Receitas
- Quais receitas têm **menor quantidade de calorias** por porção?
- Qual culinária tem o **menor tempo médio** de preparo e cozimento?
- Quais receitas fáceis têm a **melhor avaliação**?

### ✅ Tarefas
- Qual a **taxa de conclusão** de tarefas por usuário?
- Quantas tarefas estão **pendentes** vs **concluídas** no total?

---


---

## 👤 Autor

Feito por **Nabi-mf** — projeto de estudo em Engenharia e Análise de Dados.
