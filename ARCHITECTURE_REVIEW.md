# Revisão Inicial da Estrutura do Projeto

## 1) Estrutura atual

O projeto está organizado por responsabilidade principal:

- `main.py`: orquestra o fluxo de backtest fim-a-fim (carga de dados, cálculo de indicadores, execução da estratégia, métricas e análise adicional por dia).
- `config.py`: parâmetros padrão da estratégia e risco.
- `data/data_loader.py`: leitura e padronização do CSV de mercado.
- `strategy/indicators.py`: cálculo de indicadores técnicos (MMA/MME, ADX, volatilidade, Bollinger width).
- `strategy/trend_module.py`: lógica de detecção de tendência.
- `strategy/filters_module.py`: filtros opcionais de entrada.
- `strategy/execution_engine.py`: máquina de execução de trades e evolução de capital.
- `analytics/performance.py`: métricas agregadas de performance.

## 2) Pontos fortes

- Separação inicial entre `data`, `strategy` e `analytics` está boa para um projeto de backtest.
- `ExecutionEngine` já encapsula estado operacional (posição, capital, PnL diário).
- Parâmetros em `config.py` evitam números mágicos espalhados pelo código.

## 3) Melhorias recomendadas (prioridade)

### Alta prioridade

1. **Separar responsabilidades em `main.py`**
   - Hoje `main.py` mistura: execução do backtest + geração de arquivo + análise exploratória das primeiras entradas.
   - Sugestão:
     - `app/backtest_runner.py` para o fluxo principal.
     - `analytics/first_trade_analysis.py` para a análise de primeiras entradas.

2. **Introduzir modelos de domínio (dataclasses)**
   - `trade_data` é um dicionário literal dentro de `ExecutionEngine`.
   - Criar `models/trade.py` com `@dataclass Trade` melhora validação, legibilidade e IDE support.

3. **Evitar I/O acoplado ao fluxo principal**
   - `main.py` escreve e relê `trade_analysis.csv` para continuar análise.
   - Melhor: analisar diretamente o `DataFrame` em memória; persistir CSV apenas como saída opcional.

4. **Config tipada e validada**
   - Trocar dict solto por `StrategyConfig` (`dataclass` ou `pydantic`) para evitar erro de chave e tipos inválidos.

### Média prioridade

5. **Extrair regras de sessão/horário**
   - Regra “não operar antes das 10h” está hardcoded no engine.
   - Mover para `config` (ex: `min_entry_hour`) e/ou módulo `strategy/session_rules.py`.

6. **Desacoplar cálculo de indicadores do dataframe bruto**
   - Alguns indicadores auxiliares (`rolling_range`, `range_mean`) ficam no DF final sem necessidade para todos os módulos.
   - Opção: retornar apenas colunas necessárias ou separar “features auxiliares” em pipeline próprio.

7. **Padronizar idioma e nomenclatura**
   - Há mistura de português/inglês em chaves e comentários (`daily_stop`, `meta diária`, etc.).
   - Definir convenção única para reduzir custo cognitivo.

### Baixa prioridade

8. **Melhorar observabilidade**
   - Trocar `print` por `logging` com níveis (`INFO`, `DEBUG`) para execução reprodutível.

9. **Testes automatizados**
   - Adicionar testes unitários para:
     - `detect_trend` (cenários de cruzamento)
     - `check_filters` (matriz de flags)
     - cálculo de métricas em `performance.py`

## 4) Proposta de reorganização de arquivos

Sugestão incremental (sem quebrar tudo de uma vez):

```text
trend_project/
  app/
    backtest_runner.py
  models/
    trade.py
    config.py
  data/
    data_loader.py
    market_data/
  strategy/
    indicators.py
    trend_module.py
    filters_module.py
    session_rules.py
    execution_engine.py
  analytics/
    performance.py
    first_trade_analysis.py
  main.py
```

## 5) Próximo passo recomendado

Começar com a extração da análise de primeiras entradas para `analytics/first_trade_analysis.py`, mantendo `main.py` apenas como ponto de entrada. Esse passo é de baixo risco e já reduz acoplamento.
