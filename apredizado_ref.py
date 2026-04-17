# -*- coding: utf-8 -*-
"""Aprendizado por Reforço - Q-Learning (Corrigido)"""

import random

class Aprendizado_por_reforco:
    # ATRIBUTO DE CLASSE REMOVIDO - estava causando compartilhamento indevido
    # posicao_rec_pun = []  # <-- REMOVIDO (era o bug)

    def __init__(self, greedy: float, taxa_desc: float, alpha: float = 0.1):
        """
        Inicializa o agente de Q-Learning
        greedy: taxa de exploração (ε) - probabilidade de explorar
        taxa_desc: fator de desconto (γ) - valor futuro
        alpha: taxa de aprendizado - quanto atualizar a cada passo
        """
        self.greedy = greedy
        self.taxa_desc = taxa_desc
        self.alpha = alpha
        self.posicao_rec_pun = []  # <-- AGORA É ATRIBUTO DE INSTÂNCIA (CORRETO)
        self.mapa = None
        self.acoes = [0, 1, 2, 3]  # cima, baixo, esquerda, direita
        self.nomes_acoes = {0: "CIMA", 1: "BAIXO", 2: "ESQUERDA", 3: "DIREITA"}
        self.simbolos = {0: "↑", 1: "↓", 2: "←", 3: "→"}

    def gerar_mapa(self,
                   quant_linhas: int,
                   quant_colunas: int,
                   quant_negativos: int,
                   quant_positivos: int,
                   valor_negativo: float,
                   valor_positivo: float):
        """
        Gera o mapa com recompensas positivas e negativas
        Mantendo a estrutura original: cada célula tem [cima, baixo, esq, dir]
        """
        mapa = []

        # Inicializa mapa com [0,0,0,0] para cada célula
        for linha in range(quant_linhas):
            nova_linha = []
            for coluna in range(quant_colunas):
                nova_linha.append([0, 0, 0, 0])  # [cima, baixo, esquerda, direita]
            mapa.append(nova_linha)

        total_celulas = quant_linhas * quant_colunas
        posicoes_disponiveis = [(i, j) for i in range(quant_linhas)
                                         for j in range(quant_colunas)]

        random.shuffle(posicoes_disponiveis)

        # Adiciona valores negativos (punições)
        valor_negativo_original = valor_negativo
        valores_aplicados_negativos = []

        print(f"\n📉 Distribuindo {quant_negativos} punições de valor total {valor_negativo}:")
        for i in range(quant_negativos):
            if i == quant_negativos - 1:
                valor_aplicado = valor_negativo_original - sum(valores_aplicados_negativos)
            else:
                valor_max = abs(valor_negativo_original) - abs(sum(valores_aplicados_negativos))
                if valor_max > 0:
                    valor_aplicado = -random.randint(1, valor_max)
                else:
                    valor_aplicado = valor_negativo_original - sum(valores_aplicados_negativos)

            linha, coluna = posicoes_disponiveis.pop()
            self.posicao_rec_pun.append((linha, coluna))
            # Nas células especiais, todos os 4 valores são iguais (recompensa/punição)
            for acao in range(4):
                mapa[linha][coluna][acao] = valor_aplicado
            valores_aplicados_negativos.append(valor_aplicado)
            print(f"  Punição {i+1}: {valor_aplicado} na posição ({linha}, {coluna})")

        # Adiciona valores positivos (recompensas)
        valor_positivo_original = valor_positivo
        valores_aplicados_positivos = []

        print(f"\n📈 Distribuindo {quant_positivos} recompensas de valor total {valor_positivo}:")
        for i in range(quant_positivos):
            if i == quant_positivos - 1:
                valor_aplicado = valor_positivo_original - sum(valores_aplicados_positivos)
            else:
                valor_max = valor_positivo_original - sum(valores_aplicados_positivos)
                if valor_max > 0:
                    valor_aplicado = random.randint(1, valor_max)
                else:
                    valor_aplicado = valor_positivo_original - sum(valores_aplicados_positivos)

            linha, coluna = posicoes_disponiveis.pop()
            self.posicao_rec_pun.append((linha, coluna))
            # Nas células especiais, todos os 4 valores são iguais (recompensa/punição)
            for acao in range(4):
                mapa[linha][coluna][acao] = valor_aplicado
            valores_aplicados_positivos.append(valor_aplicado)
            print(f"  Recompensa {i+1}: +{valor_aplicado} na posição ({linha}, {coluna})")

        self.mapa = mapa
        print("\n" + "="*70)
        print("✅ MAPA GERADO COM SUCESSO!")
        print("="*70)

        return mapa

    def inicio_mapa(self, mapa):
        """Escolhe uma posição inicial aleatória que não seja recompensa/punição"""
        while True:
            linha = random.randint(0, len(mapa) - 1)
            coluna = random.randint(0, len(mapa[0]) - 1)

            if (linha, coluna) not in self.posicao_rec_pun:
                return (linha, coluna)

    def mover(self, estado, acao):
        """
        Executa uma ação e retorna o novo estado
        estado: tupla (linha, coluna)
        acao: 0=cima, 1=baixo, 2=esquerda, 3=direita
        """
        linha, coluna = estado

        if acao == 0:  # cima
            return (max(0, linha - 1), coluna)
        elif acao == 1:  # baixo
            return (min(len(self.mapa) - 1, linha + 1), coluna)
        elif acao == 2:  # esquerda
            return (linha, max(0, coluna - 1))
        elif acao == 3:  # direita
            return (linha, min(len(self.mapa[0]) - 1, coluna + 1))

    def obter_recompensa(self, estado, acao=None):
        """
        Retorna a recompensa do estado atual
        Se ação for fornecida, pega o valor específico para aquela ação
        """
        linha, coluna = estado

        if (linha, coluna) in self.posicao_rec_pun:
            if acao is not None:
                return self.mapa[linha][coluna][acao]
            return self.mapa[linha][coluna][0]  # Todos são iguais em terminais

        # Para células normais, retorna 0 (recompensa imediata)
        return 0

    def melhor_acao(self, estado):
        """Retorna a melhor ação para um dado estado baseado no mapa"""
        linha, coluna = estado
        # CORREÇÃO: Em caso de empate, escolhe aleatoriamente (evita viés)
        valores = self.mapa[linha][coluna]
        max_valor = max(valores)
        melhores_indices = [i for i, v in enumerate(valores) if v == max_valor]
        return random.choice(melhores_indices)

    def escolher_acao(self, estado, episodio):
        """
        Política ε-greedy: explora com probabilidade greedy,
        explota com probabilidade 1-greedy
        """
        if random.random() < self.greedy:
            # Exploração: ação aleatória
            return random.choice(self.acoes)
        else:
            # Explotação: melhor ação baseada nos valores atuais do mapa
            return self.melhor_acao(estado)

    def atualizar_valores(self, estado, acao, recompensa, novo_estado):
        """
        Atualiza os valores do mapa usando a fórmula do Q-Learning:
        Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
        """
        l, c = estado
        nl, nc = novo_estado

        valor_atual = self.mapa[l][c][acao]

        # Pega o melhor valor do próximo estado (max Q(s',a'))
        valores_proximo = self.mapa[nl][nc]
        max_futuro = max(valores_proximo)

        # Calcula novo valor usando fórmula do Q-Learning
        novo_valor = valor_atual + self.alpha * (
            recompensa + self.taxa_desc * max_futuro - valor_atual
        )

        # ATUALIZA O VALOR NO MAPA!
        self.mapa[l][c][acao] = round(novo_valor, 2)

        return novo_valor

    def mostrar_mapa_compacto(self, titulo=""):
        """Mostra o mapa de forma compacta para ver evolução"""
        if self.mapa is None:
            return

        if titulo:
            print(f"\n{titulo}")

        for i in range(len(self.mapa)):
            linha_str = []
            for j in range(len(self.mapa[0])):
                valores = self.mapa[i][j]
                if (i, j) in self.posicao_rec_pun:
                    # Célula terminal
                    if valores[0] > 0:
                        linha_str.append(f"[+{valores[0]:5.1f}]")
                    else:
                        linha_str.append(f"[{valores[0]:6.1f}]")
                else:
                    # Célula normal mostra o maior valor (max Q)
                    max_valor = max(valores)
                    melhor_dir = self.simbolos[valores.index(max_valor)]
                    linha_str.append(f"[{melhor_dir}{max_valor:5.1f}]")
            print(" ".join(linha_str))

    def treinar_com_evolucao(self, episodios=50, max_passos=20, mostrar_a_cada=10):
        """
        Treina e mostra a EVOLUÇÃO da matriz a cada N episódios
        """
        if self.mapa is None:
            raise ValueError("Gere o mapa primeiro usando gerar_mapa()!")

        print("\n" + "="*80)
        print("🎯 INICIANDO TREINAMENTO COM VISUALIZAÇÃO DA EVOLUÇÃO")
        print("="*80)

        # Mostra estado inicial
        self.mostrar_mapa_compacto("📊 MAPA INICIAL (antes do treinamento):")

        historico_recompensas = []

        for ep in range(episodios):
            estado = self.inicio_mapa(self.mapa)
            recompensa_total = 0
            passos = 0
            episodio_concluido = False

            while not episodio_concluido and passos < max_passos:
                # Escolhe ação
                acao = self.escolher_acao(estado, ep)

                # Executa ação
                novo_estado = self.mover(estado, acao)

                # Observa recompensa
                recompensa = self.obter_recompensa(novo_estado, acao)

                # ATUALIZA OS VALORES NO MAPA!
                valor_antigo = self.mapa[estado[0]][estado[1]][acao]
                novo_valor = self.atualizar_valores(estado, acao, recompensa, novo_estado)

                # Para depuração, podemos ver atualizações individuais
                if False:  # Mude para True se quiser ver cada atualização
                    print(f"  Passo {passos}: Estado {estado}, Ação {self.nomes_acoes[acao]}, "
                          f"Valor {valor_antigo:.2f} -> {novo_valor:.2f}, Recompensa {recompensa}")

                # Atualiza para próximo passo
                estado = novo_estado
                recompensa_total += recompensa
                passos += 1

                if recompensa != 0:
                    episodio_concluido = True

            historico_recompensas.append(recompensa_total)

            # Reduz exploração gradualmente
            if ep % 100 == 0 and ep > 0:
                self.greedy = max(0.01, self.greedy * 0.95)

            # MOSTRA A EVOLUÇÃO A CADA N EPISÓDIOS
            if (ep + 1) % mostrar_a_cada == 0:
                print(f"\n📈 Após {ep+1} episódios (greedy={self.greedy:.2f}):")
                self.mostrar_mapa_compacto()

        print("\n" + "="*80)
        print("✅ TREINAMENTO CONCLUÍDO!")
        if historico_recompensas:
            print(f"Recompensa média final: {sum(historico_recompensas[-10:])/10:.2f}")

        return historico_recompensas

    def mostrar_mapa_detalhado(self, titulo="VALORES ATUAIS DO MAPA"):
        """
        Exibe os valores do mapa de forma detalhada (4 valores por célula)
        """
        if self.mapa is None:
            print("Mapa não gerado ainda!")
            return

        print("\n" + "="*80)
        print(f"📍 {titulo}")
        print("="*80)

        # Cabeçalho
        print("     ", end="")
        for j in range(len(self.mapa[0])):
            print(f"   Coluna {j}    ", end="")
        print()

        # Linhas do mapa
        for i in range(len(self.mapa)):
            print(f"L{i}   ", end="")
            for j in range(len(self.mapa[0])):
                valores = self.mapa[i][j]
                if (i, j) in self.posicao_rec_pun:
                    # Célula terminal (recompensa/punição)
                    print(f"[{valores[0]:6.1f}] ", end="")
                else:
                    # Célula normal mostra 4 valores
                    print(f"[↑{valores[0]:4.1f} ↓{valores[1]:4.1f} ", end="")
                    print(f"←{valores[2]:4.1f} →{valores[3]:4.1f}] ", end="")
            print()  # Nova linha

        print("="*80)

    def mostrar_politica(self):
        """Mostra a melhor ação em cada estado baseado nos valores atuais"""
        if self.mapa is None:
            print("Mapa não gerado ainda!")
            return

        print("\n" + "="*50)
        print("🎯 POLÍTICA ATUAL (melhor ação por célula):")
        print("="*50)

        for i in range(len(self.mapa)):
            linha_politica = []
            for j in range(len(self.mapa[0])):
                if (i, j) in self.posicao_rec_pun:
                    if self.obter_recompensa((i, j)) > 0:
                        linha_politica.append("  ⚡  ")  # Recompensa
                    else:
                        linha_politica.append("  💀  ")  # Punição
                else:
                    melhor_acao = self.melhor_acao((i, j))
                    linha_politica.append(f"  {self.simbolos[melhor_acao]}  ")
            print("".join(linha_politica))
        print("="*50)


if __name__ == "__main__":
    # Configuração do problema
    print("🤖 Inicializando agente de Q-Learning...")

    # Cria agente com parâmetros
    rl = Aprendizado_por_reforco(
        greedy=0.5,      # Taxa de exploração alta no início para ver mudanças
        taxa_desc=0.9,   # Fator de desconto
        alpha=0.2        # Taxa de aprendizado mais alta para mudanças visíveis
    )

    # Gera um mapa para teste
    print("🗺️ Gerando mapa 6x6...")
    mapa = rl.gerar_mapa(
        quant_linhas=6,
        quant_colunas=6,
        quant_negativos=2,   # 2 punições
        quant_positivos=3,    # 3 recompensas
        valor_negativo=-100,
        valor_positivo=500
    )

    # Mostra o mapa INICIAL detalhado
    rl.mostrar_mapa_detalhado("📊 MAPA INICIAL (valores detalhados)")

    # Mostra política inicial
    rl.mostrar_politica()

    # Treina MOSTRANDO A EVOLUÇÃO a cada 5 episódios
    print("\n" + "="*80)
    print("🔄 INICIANDO TREINAMENTO COM EVOLUÇÃO VISÍVEL")
    print("="*80)

    historico = rl.treinar_com_evolucao(
        episodios=30,      # 30 episódios
        max_passos=15,
        mostrar_a_cada=5   # Mostra a cada 5 episódios
    )

    # Mostra o mapa FINAL detalhado
    rl.mostrar_mapa_detalhado("📊 MAPA FINAL (após treinamento)")

    # Mostra a política final
    print("\n🎯 Política final:")
    rl.mostrar_politica()

    # Gráfico simples da evolução das recompensas
    print("\n📈 Evolução das recompensas por episódio:")
    print("-" * 50)
    for i, recomp in enumerate(historico):
        if i % 5 == 0:  # Mostra a cada 5 episódios
            bars = int((recomp + 10) * 2)  # Normaliza para visualização
            print(f"Ep {i:2}: {recomp:5.1f} {'█' * max(0, bars)}")