"""
Algoritmo Genético para Otimização de Combinações de Roupas
CORRIGIDO e OTIMIZADO
"""

import random
from typing import List, Tuple, Dict, Any

# Constantes
CAMISAS = ("Branca", "Preta", "Azul", "Vermelha", "Verde")  # Adicionei mais opções
CALCAS = ("Jeans", "Preta", "Bege", "Marrom", "Cinza")
TENIS = ("Cinza", "Preta", "Azul", "Branca", "Vermelho")

# Parâmetros do algoritmo
TAMANHO_POPULACAO = 100
TAXA_MUTACAO = 0.05  # 5% é mais realista
TAXA_ELITISMO = 0.1  # 10% dos melhores mantidos


def criar_combinacoes(quantidade: int) -> List[Tuple[str, str, str]]:
    """Cria combinações aleatórias de roupas"""
    combinacoes = []
    for _ in range(quantidade):
        combinacoes.append((
            random.choice(CAMISAS),
            random.choice(CALCAS),
            random.choice(TENIS)
        ))
    return combinacoes


def fitness(combinacoes: List[Tuple[str, str, str]]) -> List[float]:
    """
    Calcula pontuação para cada combinação
    CORREÇÃO: Normalizada entre 0 e 1
    """
    pontuacoes = []
    
    for combinacao in combinacoes:
        pontuacao = 0.0
        
        # 1. Camisa e calça não podem ser iguais (25%)
        if combinacao[0] != combinacao[1]:
            pontuacao += 0.25
        
        # 2. Tênis combina com pelo menos uma peça (25%)
        if combinacao[2] == combinacao[1] or combinacao[2] == combinacao[0]:
            pontuacao += 0.25
        
        # 3. Evitar look totalmente preto (25%)
        if not (combinacao[0] == combinacao[1] == combinacao[2] == "Preta"):
            pontuacao += 0.25
        
        # 4. Combinação especial: calça bege + tênis preto (25%)
        if combinacao[1] == "Bege" and combinacao[2] == "Preta":
            pontuacao += 0.25
        
        # Bônus: cores diferentes nas três peças
        if len(set(combinacao)) == 3:
            pontuacao += 0.1
        
        # Penalidade: look totalmente colorido demais (opcional)
        if combinacao[0] == "Vermelha" and combinacao[1] == "Azul" and combinacao[2] == "Verde":
            pontuacao -= 0.1
        
        pontuacoes.append(max(0.0, min(1.0, pontuacao)))  # Normaliza entre 0 e 1
    
    return pontuacoes


def selecao_torneio(populacao: List[Tuple[str, str, str]], 
                    pontuacoes: List[float], 
                    tamanho_torneio: int = 3) -> Tuple[str, str, str]:
    """
    Seleção por torneio (mais eficiente que elitismo puro)
    """
    melhores = []
    for _ in range(tamanho_torneio):
        idx = random.randint(0, len(populacao) - 1)
        melhores.append((populacao[idx], pontuacoes[idx]))
    
    return max(melhores, key=lambda x: x[1])[0]


def crossover(pai1: Tuple[str, str, str], 
              pai2: Tuple[str, str, str], 
              tipo: str = "Single") -> Tuple[Tuple[str, str, str], Tuple[str, str, str]]:
    """
    CORREÇÃO: Retorna dois filhos corretamente estruturados
    """
    if tipo == "Single":
        # Ponto de corte aleatório
        ponto = random.randint(1, 2)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
    
    elif tipo == "Double":
        # Dois pontos de corte
        ponto1 = random.randint(1, 2)
        ponto2 = random.randint(ponto1 + 1, 3)
        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]
    
    elif tipo == "Uniforme":
        # Cada gene tem 50% de chance de vir de cada pai
        filho1 = []
        filho2 = []
        for i in range(3):
            if random.random() < 0.5:
                filho1.append(pai1[i])
                filho2.append(pai2[i])
            else:
                filho1.append(pai2[i])
                filho2.append(pai1[i])
        filho1 = tuple(filho1)
        filho2 = tuple(filho2)
    
    else:  # Default para Single
        ponto = random.randint(1, 2)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
    
    return filho1, filho2


def mutacao(combinacao: Tuple[str, str, str], taxa: float) -> Tuple[str, str, str]:
    """
    CORREÇÃO: Mutação com taxa configurável
    """
    combinacao_lista = list(combinacao)
    
    for i in range(3):
        if random.random() < taxa:
            if i == 0:  # Camisa
                combinacao_lista[i] = random.choice(CAMISAS)
            elif i == 1:  # Calça
                combinacao_lista[i] = random.choice(CALCAS)
            else:  # Tênis
                combinacao_lista[i] = random.choice(TENIS)
    
    return tuple(combinacao_lista)


class AlgoritmoGenetico:
    def __init__(self, populacao_inicial: List[Tuple[str, str, str]]):
        self.populacao = populacao_inicial
        self.melhor_por_geracao = []
        self.pior_por_geracao = []
        self.media_por_geracao = []

    def avaliar_populacao(self) -> List[float]:
        """Avalia toda a população e retorna as pontuações"""
        return fitness(self.populacao)

    def run_main(self, num_geracoes: int, tipo_crossover: str = "Single") -> Dict[int, List[Tuple[Tuple[str, str, str], float]]]:
        """
        Executa o algoritmo genético principal
        CORREÇÃO: Retorna estrutura correta e mantém tamanho da população
        """
        registros = {}
        tamanho_elite = max(1, int(TAMANHO_POPULACAO * TAXA_ELITISMO))
        
        print("="*70)
        print("🧬 INICIANDO ALGORITMO GENÉTICO")
        print(f"População: {TAMANHO_POPULACAO} | Gerações: {num_geracoes}")
        print(f"Elitismo: {tamanho_elite} | Mutação: {TAXA_MUTACAO:.0%}")
        print(f"Crossover: {tipo_crossover}")
        print("="*70)
        
        for geracao in range(num_geracoes):
            # Avalia população
            pontuacoes = self.avaliar_populacao()
            
            # Registra estatísticas
            melhor_idx = pontuacoes.index(max(pontuacoes))
            pior_idx = pontuacoes.index(min(pontuacoes))
            media = sum(pontuacoes) / len(pontuacoes)
            
            self.melhor_por_geracao.append(pontuacoes[melhor_idx])
            self.pior_por_geracao.append(pontuacoes[pior_idx])
            self.media_por_geracao.append(media)
            
            # Prepara resultados (população + pontuações)
            resultados = list(zip(self.populacao, pontuacoes))
            resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)
            
            # CORREÇÃO: Registra apenas os melhores (como antes, mas estrutura correta)
            registros[geracao] = resultados_ordenados[:10]  # Top 10
            
            # Mostra progresso a cada 10 gerações
            if geracao % 10 == 0 or geracao == num_geracoes - 1:
                melhor_individuo = resultados_ordenados[0]
                print(f"Geração {geracao:3d}: Melhor = {melhor_individuo[1]:.3f} | "
                      f"Média = {media:.3f} | Pior = {pontuacoes[pior_idx]:.3f}")
                print(f"          Combinação: {melhor_individuo[0]}")
            
            # Cria nova população
            nova_populacao = []
            
            # 1. ELITISMO: Mantém os melhores indivíduos
            elite = [item[0] for item in resultados_ordenados[:tamanho_elite]]
            nova_populacao.extend(elite)
            
            # 2. CRUZAMENTO: Gera o resto da população
            while len(nova_populacao) < TAMANHO_POPULACAO:
                # Seleciona dois pais (torneio)
                pai1 = selecao_torneio(self.populacao, pontuacoes)
                pai2 = selecao_torneio(self.populacao, pontuacoes)
                
                # Crossover
                filho1, filho2 = crossover(pai1, pai2, tipo_crossover)
                
                # Mutação
                filho1 = mutacao(filho1, TAXA_MUTACAO)
                filho2 = mutacao(filho2, TAXA_MUTACAO)
                
                nova_populacao.append(filho1)
                if len(nova_populacao) < TAMANHO_POPULACAO:
                    nova_populacao.append(filho2)
            
            # Atualiza população
            self.populacao = nova_populacao
        
        print("="*70)
        print("✅ ALGORITMO GENÉTICO CONCLUÍDO!")
        
        # Mostra resultado final
        pontuacoes_finais = self.avaliar_populacao()
        melhor_final_idx = pontuacoes_finais.index(max(pontuacoes_finais))
        print(f"\n🏆 MELHOR COMBINAÇÃO ENCONTRADA:")
        print(f"   Camisa: {self.populacao[melhor_final_idx][0]}")
        print(f"   Calça:  {self.populacao[melhor_final_idx][1]}")
        print(f"   Tênis:  {self.populacao[melhor_final_idx][2]}")
        print(f"   Score:  {pontuacoes_finais[melhor_final_idx]:.3f}")
        print("="*70)
        
        return registros
    
    def mostrar_evolucao(self):
        """Mostra gráfico textual da evolução"""
        print("\n📈 EVOLUÇÃO DO ALGORITMO:")
        print("-"*70)
        print("Geração | Melhor  | Média   | Pior")
        print("-"*70)
        
        for i in range(len(self.melhor_por_geracao)):
            melhor = self.melhor_por_geracao[i]
            media = self.media_por_geracao[i]
            pior = self.pior_por_geracao[i]
            
            # Barra visual para o melhor
            barra = "█" * int(melhor * 50)
            print(f"{i:6d} | {melhor:.3f} | {media:.3f} | {pior:.3f} | {barra}")
        
        print("-"*70)


if __name__ == "__main__":
    print("🎨 OTIMIZADOR DE LOOKS - ALGORITMO GENÉTICO")
    print(f"Opções disponíveis:")
    print(f"  Camisas: {', '.join(CAMISAS)}")
    print(f"  Calças:  {', '.join(CALCAS)}")
    print(f"  Tênis:   {', '.join(TENIS)}")
    print()
    
    # Cria população inicial
    print(f"📊 Criando população inicial de {TAMANHO_POPULACAO} indivíduos...")
    populacao_inicial = criar_combinacoes(TAMANHO_POPULACAO)
    
    # Inicializa algoritmo
    algoritmo = AlgoritmoGenetico(populacao_inicial)
    
    # Executa (testa diferentes tipos de crossover)
    print("\n🔬 Testando crossover Single-point:")
    resultados_single = algoritmo.run_main(num_geracoes=50, tipo_crossover="Single")
    
    algoritmo.mostrar_evolucao()
    
    # Teste com crossover uniforme (opcional)
    print("\n" + "="*70)
    print("🔬 Testando crossover Uniforme:")
    algoritmo_uniforme = AlgoritmoGenetico(criar_combinacoes(TAMANHO_POPULACAO))
    resultados_uniforme = algoritmo_uniforme.run_main(num_geracoes=30, tipo_crossover="Uniforme")
    algoritmo_uniforme.mostrar_evolucao()