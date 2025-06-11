# -*- coding: utf-8 -*-
# Importação de bibliotecas
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
# Caminho para o arquivo CSV
caminho_arquivo = "C:/Users/victo/AppData/Local/Programs/Python/Python313/ecommerce_estatistica (1).csv"
# Leitura com tratamento de colunas quebradas e aspas
df = pd.read_csv(
  caminho_arquivo,
  sep=',',
  quoting=1,
  quotechar='"',
  engine='python',
  on_bad_lines='skip'
)
# Pré-processamento
df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
df.dropna(subset=['Preço'], inplace=True)
top_10_marcas = df['Marca'].value_counts().nlargest(10).index
df_top_marcas = df[df['Marca'].isin(top_10_marcas)]
# Inicia o app Dash
app = dash.Dash(__name__)
app.title = "Dashboard E-commerce"
# Layout do app com abas
app.layout = html.Div([
  html.H1("Dashboard E-commerce", style={'textAlign': 'center'}),
  dcc.Tabs([
    dcc.Tab(label='Histograma de Vendas por Marca', children=[
      dcc.Graph(
        figure=px.histogram(df_top_marcas, x='Marca', y='Qtd_Vendidos')
        .update_layout(title='Marca vs Quantidade de vendas', xaxis_title='Marca', yaxis_title='Qtd_Vendidos')
      )
    ]),
    dcc.Tab(label='Dispersão Desconto vs Vendas', children=[
      dcc.Graph(
        figure=px.scatter(df_top_marcas, x='Qtd_Vendidos', y='Desconto', color='Marca')
        .update_layout(title='Desconto vs Quantidade de vendas', xaxis_title='Qtd_Vendidos', yaxis_title='Desconto')
      )
    ]),
    dcc.Tab(label='Mapa de Calor Nota x Avaliações', children=[
      dcc.Graph(
        figure=px.density_heatmap(df_top_marcas, x='N_Avaliações', y='Nota')
        .update_layout(title='Nota vs N_Avaliações', xaxis_title='N_Avaliações', yaxis_title='Nota')
      )
    ]),
    dcc.Tab(label='Material por Gênero', children=[
      dcc.Graph(
        figure=px.bar(df_top_marcas, x='Gênero', y='Material', color='Material')
        .update_layout(title='Material por Gênero', xaxis_title='Gênero', yaxis_title='Material')
      )
    ]),
    dcc.Tab(label='Pizza: Nota por Marca', children=[
      dcc.Graph(
        figure=px.pie(df_top_marcas, values='Nota', names='Marca')
        .update_layout(title='Nota por Marcas')
      )
    ]),
    dcc.Tab(label='Densidade Nota vs Preço', children=[
      dcc.Graph(
        figure=px.density_contour(df_top_marcas, x='Preço', y='Nota')
        .update_layout(title='Densidade de Nota vs Preço', xaxis_title='Preço', yaxis_title='Nota')
      )
    ]),
    dcc.Tab(label='Regressão Preço vs Nota', children=[
      dcc.Graph(
        figure=px.scatter(df_top_marcas, x='Preço', y='Nota', color='Marca')
        .update_layout(title='Regressão por Marca: Preço vs Nota', xaxis_title='Preço', yaxis_title='Nota')
      )
    ]),
  ])
])

# Roda o servidor local
if __name__ == '__main__':
  app.run(debug=True)