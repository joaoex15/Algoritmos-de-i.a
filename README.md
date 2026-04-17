---
title: Suite de Algoritmos de IA
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
---

# 🤖 Suite de Algoritmos de IA

Três algoritmos clássicos de Inteligência Artificial implementados em Python puro, com interface interativa via Gradio.

---

## 📦 Estrutura dos Arquivos

```
├── app.py                  # Interface Gradio (Hugging Face entry point)
├── main.py                 # Entry point CLI — importa os 3 algoritmos
├── A_estrela.py            # Algoritmo A*
├── Algoritmos_genetico.py  # Algoritmo Genético
├── aprendizado_ref.py      # Q-Learning / Aprendizado por Reforço
├── requirements.txt
└── README.md
```

> **`main.py` e `app.py` apenas importam os algoritmos — nenhum código foi duplicado.**

---

## 🗺️ Algoritmo A* (`A_estrela.py`)

**O que é:** Algoritmo de busca informada que encontra o **caminho ótimo** entre dois pontos num grid com obstáculos.

**Como funciona:**
1. Gera um grid N×M com obstáculos aleatórios
2. Usa a fórmula `f(n) = g(n) + h(n)`:
   - `g` = custo real do caminho percorrido
   - `h` = heurística de Chebyshev (estimativa até o destino)
3. Explora 8 direções (horizontal, vertical e diagonal)
4. Reconstrói e exibe o caminho encontrado

**Parâmetros configuráveis:**
| Parâmetro | Descrição |
|-----------|-----------|
| Linhas / Colunas | Dimensão do grid |
| Obstáculos | Quantidade de bloqueios aleatórios |
| Início / Fim | Coordenadas de origem e destino |

---

## 🧬 Algoritmo Genético (`Algoritmos_genetico.py`)

**O que é:** Metaheurística inspirada na evolução biológica para **otimizar combinações de roupas**.

**Cromossomo:** `(Camisa, Calça, Tênis)` — 3 genes com múltiplos alelos.

**Ciclo evolutivo:**
1. **Avaliação (Fitness):** Pontua cada combinação com critérios de harmonia de cores
2. **Seleção:** Torneio — os mais aptos competem para gerar filhos
3. **Crossover:** Single-point, Double-point ou Uniforme
4. **Mutação:** Substituição aleatória de gene com taxa configurável
5. **Elitismo:** Os 10% melhores são preservados a cada geração

**Parâmetros configuráveis:**
| Parâmetro | Descrição |
|-----------|-----------|
| Gerações | Quantas iterações evolutivas |
| Tipo de Crossover | Single / Double / Uniforme |

---

## 🤖 Q-Learning (`aprendizado_ref.py`)

**O que é:** Algoritmo de **Aprendizado por Reforço** — o agente aprende a navegar num grid coletando recompensas e evitando punições.

**Como funciona:**
1. Gera um grid com células neutras, de recompensa (+) e punição (−)
2. O agente inicia numa posição aleatória
3. A cada passo, escolhe uma ação com a política **ε-greedy**:
   - Com prob. ε → explora (ação aleatória)
   - Com prob. 1−ε → explota (melhor ação conhecida)
4. Atualiza a Q-table com a fórmula de Bellman:

```
Q(s,a) ← Q(s,a) + α × [r + γ × max Q(s',a') − Q(s,a)]
```

**Parâmetros configuráveis:**
| Parâmetro | Símbolo | Descrição |
|-----------|---------|-----------|
| Exploração | ε (greedy) | Taxa de escolhas aleatórias |
| Desconto | γ | Peso dado às recompensas futuras |
| Aprendizado | α (alpha) | Velocidade de atualização dos valores |
| Episódios | — | Número de treinos |

---

## 🚀 Como Rodar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Interface web (Gradio)
python app.py

# Terminal interativo
python main.py
```

---

## 🧠 Conceitos de IA Cobertos

| Algoritmo | Área | Paradigma |
|-----------|------|-----------|
| A* | Busca em Espaço de Estados | IA Clássica / Busca Informada |
| Genético | Otimização Combinatória | Computação Evolutiva |
| Q-Learning | Tomada de Decisão | Aprendizado por Reforço |
