import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 1. SIMULAÇÃO DA ORIGEM DOS DADOS (Base fictícia da DataVision)
dados = {
    'Mes': ['Jan', 'Jan', 'Fev', 'Fev', 'Mar', 'Mar', 'Abr', 'Abr', 'Mai', 'Mai', 'Jun', 'Jun'],
    'Cliente': ['Ana', 'Carlos', 'Beatriz', 'Daniel', 'Ana', 'Eduardo', 'Fernanda', 'Carlos', 'Gabriel', 'Helena', 'Igor', 'Beatriz'],
    'Produto': ['Consultoria BI', 'Treinamento Python', 'Consultoria BI', 'Auditoria Dados', 'Treinamento Python', 'Consultoria BI', 'Dashboards Custom', 'Consultoria BI', 'Auditoria Dados', 'Treinamento Python', 'Consultoria BI', 'Dashboards Custom'],
    'Categoria': ['Serviços', 'Educação', 'Serviços', 'Análise', 'Educação', 'Serviços', 'Desenvolvimento', 'Serviços', 'Análise', 'Educação', 'Serviços', 'Desenvolvimento'],
    'Valor': [5000, 2500, 5500, 4000, 2500, 6000, 7500, 5000, 4200, 2800, 6500, 8000]
}

df = pd.DataFrame(dados)

# 2. PROCESSAMENTO COM PANDAS (Cálculo dos KPIs)
qtd_clientes = df['Cliente'].nunique()
total_vendas = len(df)
faturamento_total = df['Valor'].sum()
produto_mais_vendido = df['Produto'].mode()[0]

# Agrupamentos para os gráficos
ordem_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
faturamento_mensal = df.groupby('Mes')['Valor'].sum().reindex(ordem_meses)
media_mensal = faturamento_mensal.mean()
vendas_categoria = df['Categoria'].value_counts()

# 3. INTERFACE DESKTOP COM TKINTER
janela = tk.Tk()
janela.title("DataVision Consultoria - Painel Gerencial")
janela.geometry("1050x650")
janela.configure(bg="#F0F2F5")

# Cabeçalho
frame_topo = tk.Frame(janela, bg="#1E293B", height=60)
frame_topo.pack(fill="x")
lbl_titulo = tk.Label(frame_topo, text="DATAVISION CONSULTORIA | DASHBOARD EXECUTIVO", font=("Segoe UI", 16, "bold"), bg="#1E293B", fg="white")
lbl_titulo.pack(pady=15)

# Área dos Cartões KPI
frame_kpis = tk.Frame(janela, bg="#F0F2F5")
frame_kpis.pack(fill="x", padx=20, pady=15)

def criar_cartao(parent, titulo, valor, cor_borda):
    card = tk.Frame(parent, bg="white", highlightbackground=cor_borda, highlightthickness=2, padx=15, pady=15)
    card.pack(side="left", expand=True, fill="both", padx=8)
    tk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bg="white", fg="#64748B").pack(anchor="w")
    tk.Label(card, text=valor, font=("Segoe UI", 18, "bold"), bg="white", fg="#0F172A").pack(anchor="w", pady=(5, 0))

criar_cartao(frame_kpis, "CLIENTES CADASTRADOS", f"{qtd_clientes} clientes", "#3B82F6")
criar_cartao(frame_kpis, "TOTAL DE VENDAS", f"{total_vendas} vendas", "#10B981")
criar_cartao(frame_kpis, "FATURAMENTO TOTAL", f"R$ {faturamento_total:,.2f}", "#8B5CF6")
criar_cartao(frame_kpis, "PRODUTO MAIS VENDIDO", produto_mais_vendido, "#F59E0B")

# Área dos Gráficos (Matplotlib integrado)
frame_graficos = tk.Frame(janela, bg="#F0F2F5")
frame_graficos.pack(fill="both", expand=True, padx=20, pady=10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=100)
fig.patch.set_facecolor('#F0F2F5')

# Gráfico 1: Faturamento Mensal + Linha de Média
ax1.plot(faturamento_mensal.index, faturamento_mensal.values, marker='o', color='#2563EB', linewidth=2.5, label='Faturamento')
ax1.axhline(media_mensal, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Média (R$ {media_mensal:,.0f})')
ax1.set_title("Faturamento Mensal vs. Média", fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylabel("Valor (R$)")
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()
ax1.set_facecolor('white')

# Gráfico 2: Vendas por Categoria
cores_barras = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']
ax2.bar(vendas_categoria.index, vendas_categoria.values, color=cores_barras)
ax2.set_title("Quantidade de Vendas por Categoria", fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_ylabel("Qtd. Vendas")
ax2.grid(axis='y', linestyle=':', alpha=0.6)
ax2.set_facecolor('white')

plt.tight_layout(pad=2.5)

# Embutindo o gráfico no Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

janela.mainloop()
