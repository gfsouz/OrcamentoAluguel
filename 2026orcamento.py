"""
Sistema de Orçamento de Aluguel - Imobiliária R.M
Versão simples: interface direta, código curto
"""

import csv
from datetime import datetime


# função para pedir números válidos ao usuário
# evita erros se digitar texto ou número fora do limite
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


# função para perguntas de sim ou não
# aceita variações como s, sim, y, yes, n, nao, não, no
def perguntar_sim_nao(mensagem):
    while True:
        r = input(mensagem).strip().lower()
        if r in ('s', 'sim', 'y', 'yes'):
            return True
        elif r in ('n', 'nao', 'não', 'no'):
            return False
        else:
            print("Responda 'sim' ou 'não'.")


# classe que representa o imóvel
# guarda tipo, quartos e vagas de garagem
class Imovel:
    def __init__(self, tipo, quartos, garagem):
        self.tipo = tipo  # "apartamento", "casa", "estudio"
        self.quartos = quartos
        self.garagem = garagem

    # calcula o valor do aluguel baseado nas regras da imobiliária
    def calcular_aluguel(self, tem_criancas):
        # define valor base conforme tipo de imóvel
        if self.tipo == "apartamento":
            base = 700.0
        elif self.tipo == "casa":
            base = 900.0
        else:  # estudio
            base = 1200.0

        # adiciona taxa extra se tiver 2 quartos ou mais
        if self.tipo == "apartamento" and self.quartos >= 2:
            base += 200.0  # apartamento com 2+ quartos
        elif self.tipo == "casa" and self.quartos >= 2:
            base += 250.0  # casa com 2+ quartos

        # calcula custo da garagem conforme tipo
        if self.tipo == "estudio":
            # estúdio tem preço fixo para 2 vagas
            # vagas extras custam 60 reais cada
            if self.garagem <= 2:
                base += 250.0
            else:
                base += 250.0 + (self.garagem - 2) * 60.0
        elif self.tipo in ("apartamento", "casa"):
            # apartamento e casa pagam 300 por vaga
            base += self.garagem * 300.0

        # aplica desconto de 5% em apartamento sem crianças
        if self.tipo == "apartamento" and not tem_criancas:
            base -= base * 0.05

        # garante que o valor não fique negativo
        return max(base, 0.0)


# classe que gerencia o orçamento completo
# inclui cálculo final e geração do arquivo csv
class Orcamento:
    VALOR_CONTRATO = 2000.0  # valor fixo do contrato imobiliário
    MAX_PARCELAS = 5  # máximo de parcelas permitidas

    def __init__(self, imovel, tem_criancas):
        self.imovel = imovel
        self.tem_criancas = tem_criancas
        self.data = datetime.now()  # data atual para nome do arquivo

    # calcula aluguel mensal e valor da parcela do contrato
    def calcular(self, parcelas_contrato):
        aluguel = self.imovel.calcular_aluguel(self.tem_criancas)
        parcela_contrato = self.VALOR_CONTRATO / parcelas_contrato
        return aluguel, parcela_contrato

    # gera arquivo csv com 12 meses de orçamento
    def gerar_csv(self, parcelas_contrato):
        aluguel, parcela_contrato = self.calcular(parcelas_contrato)
        
        # cria nome único para o arquivo usando data e hora
        nome_arquivo = f"orcamento_{self.data.strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # escreve cabeçalho do csv
            writer.writerow(['Mês', 'Aluguel (BRL)', 'Parcela Contrato (BRL)', 'Total (BRL)'])
            
            # escreve 12 linhas, uma para cada mês
            for mes in range(1, 13):
                # só cobra parcela do contrato nos primeiros meses
                parcela = parcela_contrato if mes <= parcelas_contrato else 0.0
                total = aluguel + parcela
                writer.writerow([mes, f"R$ {aluguel:.2f}", f"R$ {parcela:.2f}", f"R$ {total:.2f}"])
        
        return nome_arquivo


# função principal que controla o fluxo do programa
def main():
    print("=" * 40)
    print("ORÇAMENTO DE ALUGUEL - R.M")
    print("=" * 40)

    # pede tipo de imóvel ao usuário
    print("\nTipo de imóvel:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    opcao = perguntar_numero("Digite o número (1-3): ", 1, 3)
    tipo = ["apartamento", "casa", "estudio"][opcao - 1]

    # pede quantidade de quartos e vagas de garagem
    quartos = perguntar_numero("Quantos quartos? ", 1)
    garagem = perguntar_numero("Quantas vagas de garagem? ", 0)

    # pergunta sobre crianças apenas se for apartamento
    # outros tipos não têm desconto por isso
    if tipo == "apartamento":
        tem_criancas = perguntar_sim_nao("Tem crianças? (s/n): ")
    else:
        tem_criancas = False

    # pede número de parcelas para o contrato
    parcelas_contrato = perguntar_numero("Parcelar contrato em quantas vezes? (1-5): ", 1, 5)

    # cria objetos de imóvel e orçamento
    imovel = Imovel(tipo, quartos, garagem)
    orcamento = Orcamento(imovel, tem_criancas)

    # calcula valores finais
    aluguel, parcela_contrato = orcamento.calcular(parcelas_contrato)
    
    # exibe resumo na tela
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

    # gera arquivo csv com orçamento anual
    nome_arquivo = orcamento.gerar_csv(parcelas_contrato)
    print(f"\nArquivo salvo: {nome_arquivo}")
    print("Orçamento concluído!")


# executa o programa somente se este arquivo for executado diretamente
if __name__ == "__main__":
    main()
