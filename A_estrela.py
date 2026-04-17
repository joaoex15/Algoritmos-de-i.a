from typing import List, Tuple, Optional
import numpy as np
import random


class No:
    """Nó para o algoritmo A*"""
    def __init__(self, posicao: Tuple[int, int], g: float = 0, h: float = 0, pai: Optional['No'] = None):
        self.posicao = posicao  # (linha, coluna)
        self.g = g              # Custo do início até este nó
        self.h = h              # Heurística (distância estimada até o fim)
        self.f = g + h          # Custo total estimado
        self.pai = pai          # Nó pai para reconstrução do caminho

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        if isinstance(other, No):
            return self.posicao == other.posicao
        return False


class AlgoritmoAEstrela:
    def __init__(self, num_linhas: int, num_colunas: int, quant_obstaculo: int,
                 linha_inicio: int, coluna_inicio: int,
                 linha_fim: int, coluna_fim: int):
        self.num_linhas = num_linhas
        self.num_colunas = num_colunas
        self.quant_obstaculo = quant_obstaculo
        self.linha_inicio = linha_inicio
        self.coluna_inicio = coluna_inicio
        self.linha_fim = linha_fim
        self.coluna_fim = coluna_fim
        self.mapa = self.gerar_mapa()
        
        # CORREÇÃO: Constantes para movimentos
        self.MOVIMENTO_RETA = 1      # Custo para cima, baixo, esquerda, direita
        self.MOVIMENTO_DIAGONAL = 1.414  # Custo para diagonais (raiz de 2)

    def gerar_mapa(self) -> np.ndarray:
        """Gera o mapa com obstáculos aleatórios"""
        matriz = np.zeros((self.num_linhas, self.num_colunas), dtype=int)
        
        obstaculos_colocados = 0
        tentativas_maximas = self.quant_obstaculo * 10
        tentativas = 0
        
        while obstaculos_colocados < self.quant_obstaculo and tentativas < tentativas_maximas:
            linha = random.randint(0, self.num_linhas - 1)
            coluna = random.randint(0, self.num_colunas - 1)
            
            # CORREÇÃO: Não colocar obstáculo no início ou fim
            if (linha, coluna) == (self.linha_inicio, self.coluna_inicio):
                tentativas += 1
                continue
            if (linha, coluna) == (self.linha_fim, self.coluna_fim):
                tentativas += 1
                continue
            
            # Evitar obstáculos duplicados
            if matriz[linha][coluna] == 0:
                matriz[linha][coluna] = 1
                obstaculos_colocados += 1
            
            tentativas += 1
        
        print(f"✅ Mapa gerado com {obstaculos_colocados} obstáculos")
        return matriz

    def get_mapa(self) -> np.ndarray:
        return self.mapa

    def mostrar_mapa(self):
        """Mostra o mapa de forma visual"""
        print("\n" + "="*50)
        print("🗺️ MAPA:")
        print("   " + " ".join(f"{j:2}" for j in range(self.num_colunas)))
        
        for i in range(self.num_linhas):
            linha_str = f"{i:2} "
            for j in range(self.num_colunas):
                if (i, j) == (self.linha_inicio, self.coluna_inicio):
                    linha_str += " 🏁 "
                elif (i, j) == (self.linha_fim, self.coluna_fim):
                    linha_str += " 🎯 "
                elif self.mapa[i][j] == 1:
                    linha_str += " 🧱 "
                else:
                    linha_str += " ·  "
            print(linha_str)
        print("="*50)

    def heuristica(self, linha: int, coluna: int) -> float:
        """
        CORREÇÃO: Heurística de Chebyshev para movimentos diagonais
        Distância mínima considerando que pode mover em 8 direções
        """
        delta_linha = abs(linha - self.linha_fim)
        delta_coluna = abs(coluna - self.coluna_fim)
        
        # Distância de Chebyshev: max(dx, dy)
        # Mas com custo diferenciado para diagonais
        distancia_diagonal = min(delta_linha, delta_coluna)
        distancia_reta = max(delta_linha, delta_coluna) - distancia_diagonal
        
        return distancia_diagonal * self.MOVIMENTO_DIAGONAL + distancia_reta * self.MOVIMENTO_RETA

    def retorne_vizinhos(self, linha: int, coluna: int) -> List[Tuple[int, int, float]]:
        """
        Retorna lista de (linha, coluna, custo_do_movimento)
        Permite 8 direções com custos diferentes
        """
        vizinhos = []
        
        # 8 direções possíveis
        direcoes = [
            (-1, 0, self.MOVIMENTO_RETA),     # cima
            (1, 0, self.MOVIMENTO_RETA),      # baixo
            (0, -1, self.MOVIMENTO_RETA),     # esquerda
            (0, 1, self.MOVIMENTO_RETA),      # direita
            (-1, -1, self.MOVIMENTO_DIAGONAL), # cima-esquerda
            (-1, 1, self.MOVIMENTO_DIAGONAL),  # cima-direita
            (1, -1, self.MOVIMENTO_DIAGONAL),  # baixo-esquerda
            (1, 1, self.MOVIMENTO_DIAGONAL)    # baixo-direita
        ]
        
        for dx, dy, custo in direcoes:
            nl = linha + dx
            nc = coluna + dy
            
            if 0 <= nl < self.num_linhas and 0 <= nc < self.num_colunas:
                if self.mapa[nl][nc] == 0:  # Não é obstáculo
                    vizinhos.append((nl, nc, custo))
        
        return vizinhos

    def reconstruir_caminho(self, no: No) -> List[Tuple[int, int]]:
        """Reconstrói o caminho do nó final até o início"""
        caminho = []
        atual = no
        
        while atual is not None:
            caminho.append(atual.posicao)
            atual = atual.pai
        
        caminho.reverse()
        return caminho

    def run(self) -> List[Tuple[int, int]]:
        """
        Implementação CORRETA do algoritmo A*
        Retorna o caminho encontrado ou lista vazia se não existir
        """
        # Inicialização
        no_inicio = No((self.linha_inicio, self.coluna_inicio), g=0, 
                       h=self.heuristica(self.linha_inicio, self.coluna_inicio))
        
        # CORREÇÃO: Usar dicionários para acesso rápido
        lista_aberta = {no_inicio.posicao: no_inicio}
        lista_fechada = set()
        
        # Para rastrear os melhores g-scores
        g_score = {no_inicio.posicao: 0}
        
        print(f"\n🎯 Buscando caminho de ({self.linha_inicio},{self.coluna_inicio}) "
              f"até ({self.linha_fim},{self.coluna_fim})...")
        
        iteracao = 0
        while lista_aberta:
            iteracao += 1
            
            # Encontra o nó com menor f-score na lista aberta
            no_atual = min(lista_aberta.values(), key=lambda x: x.f)
            
            # Verifica se chegou ao destino
            if no_atual.posicao == (self.linha_fim, self.coluna_fim):
                caminho = self.reconstruir_caminho(no_atual)
                print(f"✅ Caminho encontrado em {iteracao} iterações!")
                print(f"📏 Distância total: {no_atual.g:.2f}")
                return caminho
            
            # Move da lista aberta para a fechada
            pos_atual = no_atual.posicao
            lista_aberta.pop(pos_atual)
            lista_fechada.add(pos_atual)
            
            # Explora vizinhos
            vizinhos = self.retorne_vizinhos(pos_atual[0], pos_atual[1])
            
            for nl, nc, custo_movimento in vizinhos:
                pos_vizinho = (nl, nc)
                
                if pos_vizinho in lista_fechada:
                    continue
                
                # Calcula novo g-score
                g_tentativo = no_atual.g + custo_movimento
                
                # Se o vizinho não está na lista aberta ou encontramos um caminho melhor
                if pos_vizinho not in lista_aberta or g_tentativo < g_score.get(pos_vizinho, float('inf')):
                    # Atualiza o melhor caminho para este vizinho
                    g_score[pos_vizinho] = g_tentativo
                    h_score = self.heuristica(nl, nc)
                    
                    no_vizinho = No(pos_vizinho, g=g_tentativo, h=h_score, pai=no_atual)
                    lista_aberta[pos_vizinho] = no_vizinho
        
        print("❌ Nenhum caminho encontrado!")
        return []  # Nenhum caminho encontrado

    def mostrar_caminho(self, caminho: List[Tuple[int, int]]):
        """Mostra o caminho encontrado de forma visual"""
        if not caminho:
            print("❌ Nenhum caminho para mostrar!")
            return
        
        print("\n" + "="*50)
        print("🗺️ CAMINHO ENCONTRADO:")
        print("   " + " ".join(f"{j:2}" for j in range(self.num_colunas)))
        
        # Cria uma matriz para visualização
        visual = [[' ·  ' for _ in range(self.num_colunas)] for _ in range(self.num_linhas)]
        
        # Marca obstáculos
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                if self.mapa[i][j] == 1:
                    visual[i][j] = ' 🧱 '
        
        # Marca início e fim
        visual[self.linha_inicio][self.coluna_inicio] = ' 🏁 '
        visual[self.linha_fim][self.coluna_fim] = ' 🎯 '
        
        # Marca o caminho
        for i, (linha, coluna) in enumerate(caminho[1:-1]):  # Exclui início e fim
            if i == 0:
                visual[linha][coluna] = ' ↓  '
            elif i == len(caminho) - 3:
                visual[linha][coluna] = ' ↑  '
            else:
                visual[linha][coluna] = ' ★  '
        
        # Mostra o mapa
        for i in range(self.num_linhas):
            linha_str = f"{i:2} "
            for j in range(self.num_colunas):
                linha_str += visual[i][j]
            print(linha_str)
        
        print("="*50)
        print(f"📏 Caminho com {len(caminho)} posições:")
        print(f"   {' -> '.join([f'({l},{c})' for l, c in caminho])}")


if __name__ == "__main__":
    # Teste do algoritmo
    print("🚀 Inicializando Algoritmo A*")
    
    # Criando um problema de exemplo
    algoritmo = AlgoritmoAEstrela(
        num_linhas=8,
        num_colunas=8,
        quant_obstaculo=12,
        linha_inicio=0,
        coluna_inicio=0,
        linha_fim=7,
        coluna_fim=7
    )
    
    algoritmo.mostrar_mapa()
    
    caminho = algoritmo.run()
    
    if caminho:
        algoritmo.mostrar_caminho(caminho)
    else:
        print("❌ Não foi possível encontrar um caminho!")