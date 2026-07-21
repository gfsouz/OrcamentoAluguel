"""
Sistema de Orçamento de Aluguel - Imobiliária R.M
Versão simples: interface direta, código curto
"""

import csv
from datetime import datetime


def perguntar_numero(mensagem, minimo=0, maximo=None):
    while True:
        try:
            n = int(input(mensagem))
            if n < minimo:
                print(f"Digite pelo menos {minimo}.")
                continue
            if maximo is not None and n > maximo:
                print(f"Digite no máximo {maximo}.")
                continue
            return n
        except ValueError:
            print("Digite um número válido.")


def perguntar_sim_nao(mensagem):
    while True:
        r = input(mensagem).strip().lower()
        if r in ('s', 'sim', 'y', 'yes'):
            return True
        elif r in ('n', 'nao', 'não', 'no'):
            return False
        else:
            print("Responda 'sim' ou 'não'.")


class Imovel:
    def __init__(self, tipo, quartos, garagem):
        self.tipo = tipo  # "apartamento", "casa", "estudio"
        self.quartos = quartos
        self.garagem = garagem

    def calcular_aluguel(self, tem_criancas):
        # Valor base
        if self.tipo == "apartamento":
            base = 700.0
        elif self.tipo == "casa":
            base = 900.0
        else:  # estudio
            base = 1200.0

        # Acréscimo para 2 quartos ou mais
        if self.tipo == "apartamento" and self.quartos >= 2:
            base += 200.0  # R$ 200,00 na mensalidade
        elif self.tipo == "casa" and self.quartos >= 2:
            base += 250.0  # R$ 250,00 na mensalidade

        # Garagem
        if self.tipo == "estudio":
            if self.garagem <= 2:
                base += 250.0
            else:
                base += 250.0 + (self.garagem - 2) * 60.0
        elif self.tipo in ("apartamento", "casa"):
            base += self.garagem * 300.0

        # Desconto de 5% para apartamento sem crianças
        if self.tipo == "apartamento" and not tem_criancas:
            base -= base * 0.05

        return max(base, 0.0)


class Orcamento:
    VALOR_CONTRATO = 2000.0
    MAX_PARCELAS = 5

    def __init__(self, imovel, tem_criancas):
        self.imovel = imovel
        self.tem_criancas = tem_criancas
        self.data = datetime.now()

    def calcular(self, parcelas_contrato):
        aluguel = self.imovel.calcular_aluguel(self.tem_criancas)
        parcela_contrato = self.VALOR_CONTRATO / parcelas_contrato
        return aluguel, parcela_contrato

    def gerar_csv(self, parcelas_contrato):
        aluguel, parcela_contrato = self.calcular(parcelas_contrato)
        nome_arquivo = f"orcamento_{self.data.strftime('%Y%m%d_%H%M%S')}.csv"
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mês', 'Aluguel (BRL)', 'Parcela Contrato (BRL)', 'Total (BRL)'])
            for mes in range(1, 13):
                parcela = parcela_contrato if mes <= parcelas_contrato else 0.0
                total = aluguel + parcela
                writer.writerow([mes, f"R$ {aluguel:.2f}", f"R$ {parcela:.2f}", f"R$ {total:.2f}"])
        return nome_arquivo


def main():
    print("=" * 40)
    print("ORÇAMENTO DE ALUGUEL - R.M")
    print("=" * 40)

    # Tipo de imóvel
    print("\nTipo de imóvel:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    opcao = perguntar_numero("Digite o número (1-3): ", 1, 3)
    tipo = ["apartamento", "casa", "estudio"][opcao - 1]

    # Quartos e garagem
    quartos = perguntar_numero("Quantos quartos? ", 1)
    garagem = perguntar_numero("Quantas vagas de garagem? ", 0)

    # Crianças (só pergunta se for apartamento)
    if tipo == "apartamento":
        tem_criancas = perguntar_sim_nao("Tem crianças? (s/n): ")
    else:
        tem_criancas = False

    # Contrato
    parcelas_contrato = perguntar_numero("Parcelar contrato em quantas vezes? (1-5): ", 1, 5)

    # Cria imóvel e orçamento
    imovel = Imovel(tipo, quartos, garagem)
    orcamento = Orcamento(imovel, tem_criancas)

    # Calcula e exibe
    aluguel, parcela_contrato = orcamento.calcular(parcelas_contrato)
    print("\n" + "=" * 30)
    print("RESUMO")
    print("=" * 30)
    print(f"Tipo: {tipo.title()}")
    print(f"Quartos: {quartos}")
    print(f"Garagem: {garagem} vagas")
    if tipo == "apartamento":
        print(f"Crianças: {'Sim' if tem_criancas else 'Não'}")
    print(f"Aluguel: R$ {aluguel:.2f}")
    print(f"Contrato: R$ {Orcamento.VALOR_CONTRATO:.2f}")
    print(f"Parcelado em: {parcelas_contrato} x R$ {parcela_contrato:.2f}")
    print("=" * 30)

    # Gera CSV
    nome_arquivo = orcamento.gerar_csv(parcelas_contrato)
    print(f"\nArquivo salvo: {nome_arquivo}")
    print("Orçamento concluído!")


if __name__ == "__main__":
    main()
