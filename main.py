"""
main.py - Ponto de entrada para testar os 3 algoritmos de IA

Importa:
  - A_estrela.py           → Algoritmo A* (busca de caminho)
  - Algoritmos_genetico.py → Algoritmo Genético (otimização de looks)
  - aprendizado_ref.py     → Q-Learning / Aprendizado por Reforço
"""

from A_estrela import AlgoritmoAEstrela
from Algoritmos_genetico import AlgoritmoGenetico, criar_combinacoes, TAMANHO_POPULACAO
from aprendizado_ref import Aprendizado_por_reforco


def testar_a_estrela():
    print("\n" + "="*60)
    print("  🗺️  TESTE — ALGORITMO A*")
    print("="*60)
    alg = AlgoritmoAEstrela(
        num_linhas=8, num_colunas=8,
        quant_obstaculo=12,
        linha_inicio=0, coluna_inicio=0,
        linha_fim=7, coluna_fim=7
    )
    alg.mostrar_mapa()
    caminho = alg.run()
    if caminho:
        alg.mostrar_caminho(caminho)
    else:
        print("❌ Caminho não encontrado.")


def testar_genetico():
    print("\n" + "="*60)
    print("  🧬  TESTE — ALGORITMO GENÉTICO")
    print("="*60)
    populacao = criar_combinacoes(TAMANHO_POPULACAO)
    ag = AlgoritmoGenetico(populacao)
    ag.run_main(num_geracoes=30, tipo_crossover="Single")
    ag.mostrar_evolucao()


def testar_qlearning():
    print("\n" + "="*60)
    print("  🤖  TESTE — Q-LEARNING (Aprendizado por Reforço)")
    print("="*60)
    rl = Aprendizado_por_reforco(greedy=0.5, taxa_desc=0.9, alpha=0.2)
    rl.gerar_mapa(
        quant_linhas=4, quant_colunas=4,
        quant_negativos=2, quant_positivos=2,
        valor_negativo=-50, valor_positivo=100
    )
    rl.mostrar_mapa_detalhado("MAPA INICIAL")
    rl.mostrar_politica()
    rl.treinar_com_evolucao(episodios=30, max_passos=15, mostrar_a_cada=10)
    rl.mostrar_mapa_detalhado("MAPA FINAL")
    rl.mostrar_politica()


if __name__ == "__main__":
    print("🚀 SUITE DE TESTES — 3 ALGORITMOS DE IA")
    print("Escolha o que deseja executar:")
    print("  1 → A* (busca de caminho)")
    print("  2 → Algoritmo Genético")
    print("  3 → Q-Learning")
    print("  0 → Executar TODOS")

    escolha = input("\nOpção: ").strip()

    if escolha == "1":
        testar_a_estrela()
    elif escolha == "2":
        testar_genetico()
    elif escolha == "3":
        testar_qlearning()
    elif escolha == "0":
        testar_a_estrela()
        testar_genetico()
        testar_qlearning()
    else:
        print("Opção inválida. Executando todos...")
        testar_a_estrela()
        testar_genetico()
        testar_qlearning()
