import pandas as pd

dados_vendas = [
    {"Anime": "Naruto", "Unidades Vendidas": 1000, "Preço Unitário": 15},
    {"Anime": "One Piece", "Unidades Vendidas": 900, "Preço Unitário": 20},
    {"Anime": "Bleach", "Unidades Vendidas": 750, "Preço Unitário": 18},
    {"Anime": "Dragon Ball", "Unidades Vendidas": 1200, "Preço Unitário": 25},
    {"Anime": "My Hero Academia", "Unidades Vendidas": 800, "Preço Unitário": 22}
]

df_vendas = pd.DataFrame(dados_vendas)
df_vendas["Total Vendas"] = df_vendas["Unidades Vendidas"] * df_vendas["Preço Unitário"]
df_vendas.to_excel("vendas_animes.xlsx", index=False)

print(df_vendas)
