import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output
import base64
from io import BytesIO

# Configurações do Pandas (opcionais para o Dash, mas bom para depuração)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 30)

# Carrega os dados
df = pd.read_csv('ecommerce_estatistica.csv')
# print(df.head()) # Removido para o Dash, mas útil para depurar

# Função para gerar um gráfico Matplotlib/Seaborn e retornar como imagem Base64
def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig) # Importante: fecha a figura para liberar memória
    data = base64.b64encode(buf.getbuffer()).decode("utf-8")
    return f"data:image/png;base64,{data}"

def cria_graficos(df):
    # Remover símbolos como "%" e converter para float
    df['Desconto'] = df['Desconto'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)

    # --- GRÁFICO 1: HISTOGRAMA DE PREÇOS ---
    fig_hist_preco, ax_hist_preco = plt.subplots(figsize = (10,6))
    ax_hist_preco.hist(df['Preço'], bins = 10, color = '#E02D13', alpha = 0.8)
    ax_hist_preco.set_title('Histograma - Distribuição de Preços')
    ax_hist_preco.set_xlabel('Preços')
    ax_hist_preco.set_xticks(ticks = range (0, int(df['Preço'].max()) + 30, 30))
    ax_hist_preco.set_ylabel('Frequência')
    img_hist_preco = plot_to_base64(fig_hist_preco)

    # --- GRÁFICO 2: HISTOGRAMA DE DESCONTO ---
    fig_hist_desconto, ax_hist_desconto = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Desconto'], bins=30, kde=True, color='#863e9c', alpha=0.6, ax=ax_hist_desconto)
    ax_hist_desconto.set_xlabel('% de Desconto')
    ax_hist_desconto.set_ylabel('Frequência')
    ax_hist_desconto.set_title('Distribuição dos Descontos')
    img_hist_desconto = plot_to_base64(fig_hist_desconto)

    # --- GRÁFICO 3: DISPERSÃO PREÇO VS. NOTA ---
    fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Preço', y='Nota', data=df, ax=ax_scatter)
    ax_scatter.set_title('Gráfico de Dispersão: Preço vs. Nota')
    ax_scatter.set_xlabel('Preço (R$)')
    ax_scatter.set_ylabel('Nota')
    ax_scatter.grid(True)
    img_scatter = plot_to_base64(fig_scatter)

    # --- GRÁFICO 4: MAPA DE CALOR ---
    corr = df[['Qtd_Vendidos_Cod', 'Temporada_Cod', 'Preço', 'Nota', 'N_Avaliações_MinMax',]].corr()
    fig_heatmap, ax_heatmap = plt.subplots(figsize = (10,6))
    sns.heatmap(corr, annot = True, cmap='rocket', ax=ax_heatmap)
    ax_heatmap.set_title('Correlação - Valor do Produto')
    fig_heatmap.tight_layout()
    img_heatmap = plot_to_base64(fig_heatmap)

    # --- GRÁFICO 5: BARRAS DE GÊNERO ---
    fig_bar_genero, ax_bar_genero = plt.subplots(figsize=(10,6))
    df['Gênero'].value_counts().plot(kind='bar', color='#E02D13', ax=ax_bar_genero)
    ax_bar_genero.set_title('Distribuição de Gênero')
    ax_bar_genero.set_xlabel('Gênero')
    ax_bar_genero.set_ylabel('Frequência')
    ax_bar_genero.tick_params(axis='x', rotation=45)
    img_bar_genero = plot_to_base64(fig_bar_genero)

    # --- GRÁFICO 6: PIZZA DE GÊNERO ---
    x_pie = df['Gênero'].value_counts().index
    y_pie = df['Gênero'].value_counts().values
    fig_pie, ax_pie = plt.subplots(figsize=(12, 8))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    max_index = np.argmax(y_pie)
    explode = [0.1 if i == max_index else 0.02 for i in range(len(y_pie))]
    wedges, texts, autotexts = ax_pie.pie(
        y_pie,
        autopct='%.1f%%',
        startangle=90,
        colors=colors[:len(x_pie)],
        explode=explode,
        shadow=True,
        pctdistance=0.85,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    ax_pie.legend(wedges, [f'{label}: {value}' for label, value in zip(x_pie, y_pie)],
               title="Categorias",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    ax_pie.set_title('Distribuição por Categoria', fontsize=18, fontweight='bold', pad=30)
    ax_pie.axis('equal')
    fig_pie.tight_layout()
    img_pie = plot_to_base64(fig_pie)

    # --- GRÁFICO 7: DENSIDADE DE DESCONTO ---
    fig_kde_desconto, ax_kde_desconto = plt.subplots(figsize=(10, 6))
    sns.kdeplot(df['Desconto'].dropna(), fill=True, color='#863e9c', ax=ax_kde_desconto)
    ax_kde_desconto.set_xlabel('% de Desconto')
    ax_kde_desconto.set_ylabel('Densidade')
    ax_kde_desconto.set_title('Distribuição da Variável Desconto')
    img_kde_desconto = plot_to_base64(fig_kde_desconto)

    # --- GRÁFICO 8: REGRESSÃO PREÇO VS. NOTA ---
    fig_reg_preco_nota, ax_reg_preco_nota = plt.subplots(figsize=(10, 6))
    sns.regplot(x='Preço', y='Nota', data=df, ax=ax_reg_preco_nota)
    ax_reg_preco_nota.set_title('Gráfico de Regressão: Preço vs. Nota')
    ax_reg_preco_nota.set_xlabel('Preço (R$)')
    ax_reg_preco_nota.set_ylabel('Nota')
    img_reg_preco_nota = plot_to_base64(fig_reg_preco_nota)

    # Retorna todas as strings Base64
    return {
        'hist_preco': img_hist_preco,
        'hist_desconto': img_hist_desconto,
        'scatter_preco_nota': img_scatter,
        'heatmap_corr': img_heatmap,
        'bar_genero': img_bar_genero,
        'pie_genero': img_pie,
        'kde_desconto': img_kde_desconto,
        'reg_preco_nota': img_reg_preco_nota,
    }

# CRIAR DASH
def cria_app(df):
    app = Dash(__name__)

    # Gera todos os gráficos uma vez ao iniciar o aplicativo

    graficos_base64 = cria_graficos(df.copy()) # Passa uma cópia para evitar Side Effects

    app.layout = html.Div([
        html.H1("Dashboard de Estatísticas de E-commerce", style={'textAlign': 'center'}),
        html.Hr(),

        html.Div([
            html.H2("Histograma - Distribuição de Preços"),
            html.Img(src=graficos_base64['hist_preco'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Distribuição dos Descontos"),
            html.Img(src=graficos_base64['hist_desconto'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Gráfico de Dispersão: Preço vs. Nota"),
            html.Img(src=graficos_base64['scatter_preco_nota'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Mapa de Calor - Correlação"),
            html.Img(src=graficos_base64['heatmap_corr'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Distribuição de Gênero"),
            html.Img(src=graficos_base64['bar_genero'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Distribuição por Categoria (Gênero)"),
            html.Img(src=graficos_base64['pie_genero'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Distribuição da Variável Desconto (KDE)"),
            html.Img(src=graficos_base64['kde_desconto'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

            html.H2("Gráfico de Regressão: Preço vs. Nota"),
            html.Img(src=graficos_base64['reg_preco_nota'], style={'width': '80%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.Br(),

        ], style={'padding': '20px'})
    ])
    return app

if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)