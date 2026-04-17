"""
app.py — Interface Gradio para Hugging Face Spaces
Importa os 3 algoritmos e expõe abas interativas.
"""

import gradio as gr
import io, sys, random

from A_estrela import AlgoritmoAEstrela
from Algoritmos_genetico import AlgoritmoGenetico, criar_combinacoes, TAMANHO_POPULACAO
from aprendizado_ref import Aprendizado_por_reforco


# ──────────────────────────────────────────────
# Utilitário: captura print() como string
# ──────────────────────────────────────────────
def capturar_saida(func, *args, **kwargs):
    buf = io.StringIO()
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = sys.__stdout__
    return buf.getvalue()


# ──────────────────────────────────────────────
# ABA 1 — A*
# ──────────────────────────────────────────────
def rodar_a_estrela(linhas, colunas, obstaculos, li, ci, lf, cf):
    def _run():
        alg = AlgoritmoAEstrela(
            num_linhas=int(linhas), num_colunas=int(colunas),
            quant_obstaculo=int(obstaculos),
            linha_inicio=int(li), coluna_inicio=int(ci),
            linha_fim=int(lf), coluna_fim=int(cf)
        )
        alg.mostrar_mapa()
        caminho = alg.run()
        if caminho:
            alg.mostrar_caminho(caminho)
        else:
            print("❌ Nenhum caminho encontrado.")
    return capturar_saida(_run)


# ──────────────────────────────────────────────
# ABA 2 — Algoritmo Genético
# ──────────────────────────────────────────────
def rodar_genetico(geracoes, crossover_tipo):
    def _run():
        pop = criar_combinacoes(TAMANHO_POPULACAO)
        ag = AlgoritmoGenetico(pop)
        ag.run_main(num_geracoes=int(geracoes), tipo_crossover=crossover_tipo)
        ag.mostrar_evolucao()
    return capturar_saida(_run)


# ──────────────────────────────────────────────
# ABA 3 — Q-Learning
# ──────────────────────────────────────────────
def rodar_qlearning(linhas, colunas, negativos, positivos, val_neg, val_pos,
                    greedy, desconto, alpha, episodios):
    def _run():
        rl = Aprendizado_por_reforco(
            greedy=float(greedy),
            taxa_desc=float(desconto),
            alpha=float(alpha)
        )
        rl.gerar_mapa(
            quant_linhas=int(linhas), quant_colunas=int(colunas),
            quant_negativos=int(negativos), quant_positivos=int(positivos),
            valor_negativo=float(val_neg), valor_positivo=float(val_pos)
        )
        rl.mostrar_mapa_detalhado("MAPA INICIAL")
        rl.mostrar_politica()
        rl.treinar_com_evolucao(episodios=int(episodios), max_passos=20, mostrar_a_cada=max(1, int(episodios)//5))
        rl.mostrar_mapa_detalhado("MAPA FINAL")
        rl.mostrar_politica()
    return capturar_saida(_run)


# ──────────────────────────────────────────────
# Interface Gradio
# ──────────────────────────────────────────────
with gr.Blocks(title="🤖 Algoritmos de IA", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🤖 Suite de Algoritmos de IA
    Três algoritmos clássicos de IA implementados em Python. Ajuste os parâmetros e execute!
    """)

    with gr.Tab("🗺️ A* — Busca de Caminho"):
        gr.Markdown("### Encontra o menor caminho num grid com obstáculos (8 direções + diagonais)")
        with gr.Row():
            with gr.Column():
                a_linhas    = gr.Slider(4, 15, value=8,  step=1, label="Linhas")
                a_colunas   = gr.Slider(4, 15, value=8,  step=1, label="Colunas")
                a_obs       = gr.Slider(0, 30, value=12, step=1, label="Obstáculos")
                with gr.Row():
                    a_li = gr.Number(value=0, label="Linha Início",  precision=0)
                    a_ci = gr.Number(value=0, label="Coluna Início", precision=0)
                with gr.Row():
                    a_lf = gr.Number(value=7, label="Linha Fim",  precision=0)
                    a_cf = gr.Number(value=7, label="Coluna Fim", precision=0)
                btn_a = gr.Button("▶ Executar A*", variant="primary")
            with gr.Column():
                out_a = gr.Textbox(label="Saída", lines=30, max_lines=50)
        btn_a.click(rodar_a_estrela, [a_linhas, a_colunas, a_obs, a_li, a_ci, a_lf, a_cf], out_a)

    with gr.Tab("🧬 Algoritmo Genético"):
        gr.Markdown("### Otimiza combinações de roupas (camisa + calça + tênis) usando evolução simulada")
        with gr.Row():
            with gr.Column():
                g_geracoes  = gr.Slider(10, 100, value=30, step=5, label="Gerações")
                g_crossover = gr.Radio(["Single", "Double", "Uniforme"], value="Single", label="Tipo de Crossover")
                btn_g = gr.Button("▶ Executar Genético", variant="primary")
            with gr.Column():
                out_g = gr.Textbox(label="Saída", lines=30, max_lines=50)
        btn_g.click(rodar_genetico, [g_geracoes, g_crossover], out_g)

    with gr.Tab("🤖 Q-Learning"):
        gr.Markdown("### Agente aprende navegação num grid com recompensas e punições via Q-Learning")
        with gr.Row():
            with gr.Column():
                q_linhas   = gr.Slider(3, 8, value=4, step=1, label="Linhas do Mapa")
                q_colunas  = gr.Slider(3, 8, value=4, step=1, label="Colunas do Mapa")
                q_neg      = gr.Slider(1, 5, value=2, step=1, label="Qtd. Punições")
                q_pos      = gr.Slider(1, 5, value=2, step=1, label="Qtd. Recompensas")
                q_val_neg  = gr.Number(value=-50,  label="Valor Total Negativo")
                q_val_pos  = gr.Number(value=100,  label="Valor Total Positivo")
                q_greedy   = gr.Slider(0.0, 1.0, value=0.5,  step=0.05, label="ε Exploração (greedy)")
                q_desc     = gr.Slider(0.0, 1.0, value=0.9,  step=0.05, label="γ Desconto")
                q_alpha    = gr.Slider(0.01, 1.0, value=0.2, step=0.01, label="α Taxa Aprendizado")
                q_ep       = gr.Slider(10, 200, value=50, step=10, label="Episódios")
                btn_q = gr.Button("▶ Executar Q-Learning", variant="primary")
            with gr.Column():
                out_q = gr.Textbox(label="Saída", lines=35, max_lines=60)
        btn_q.click(
            rodar_qlearning,
            [q_linhas, q_colunas, q_neg, q_pos, q_val_neg, q_val_pos,
             q_greedy, q_desc, q_alpha, q_ep],
            out_q
        )

demo.launch()
