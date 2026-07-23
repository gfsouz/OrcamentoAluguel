# Orçamento de Aluguel — R.M

Sistema simples para calcular orçamento de aluguel com geração de planilha CSV.

## Como usar

1. Certifique-se de ter **Python 3** instalado.
2. Execute no terminal:

```bash
python3 2026orcamento.py
```

3. Responda as perguntas:
   - Tipo de imóvel (apartamento, casa ou estúdio)
   - Quantidade de quartos e vagas de garagem
   - Se tem crianças (apenas para apartamentos)
   - Em quantas parcelas quer pagar o contrato (1 a 5)

4. O programa exibe o resumo na tela e salva um arquivo CSV com o orçamento de 12 meses.

## Regras de cálculo

| Fator                | Regra                                                                 |
|----------------------|-----------------------------------------------------------------------|
| Apartamento          | R$ 700 + R$ 200 (se 2+ quartos) - 5% se sem crianças                  |
| Casa                 | R$ 900 + R$ 250 (se 2+ quartos)                                       |
| Estúdio              | R$ 1.200 + R$ 250 (até 2 vagas) + R$ 60 por vaga extra                |
| Garagem (apt/casa)   | R$ 300 por vaga                                                       |
| Contrato imobiliário | R$ 2.000 dividido nas parcelas escolhidas (máx. 5)                    |

## Saída

Gera um arquivo `orcamento_AAAA_MM_DD.csv` com 12 meses de aluguel, parcelas e total.
