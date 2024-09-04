import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Função para obter o valor da moeda a partir da página de conversão do Banco Central
def get_exchange_rate(from_currency, to_currency):
    url = 'https://www.bcb.gov.br/conversao'
    
    # Acessando a página (não necessariamente funcional via requests, apenas exemplo)
    response = requests.get(url)
    
    # Aqui você vai precisar ajustar a extração real com BeautifulSoup
    # Estou simulando o retorno com valores fictícios
    rate = 5.25 if from_currency == 'BRL' and to_currency == 'USD' else 0.19  # Exemplo de taxa
    
    return rate

# Função principal do bot
def currency_converter():
    print("Bem-vindo ao Conversor de Moedas do Banco Central!")
    
    # Solicitar as moedas do usuário
    from_currency = input("Digite o código da moeda de origem (ex: BRL para Real): ").upper()
    to_currency = input("Digite o código da moeda de destino (ex: USD para Dólar): ").upper()
    amount = float(input(f"Digite o valor que deseja converter de {from_currency} para {to_currency}: "))
    
    # Obter a taxa de câmbio
    exchange_rate = get_exchange_rate(from_currency, to_currency)
    converted_amount = amount * exchange_rate
    
    # Mostrar os resultados
    print(f"Taxa de câmbio: 1 {from_currency} = {exchange_rate:.2f} {to_currency}")
    print(f"Valor convertido: {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    
    # Criar uma planilha com os dados
    data = {
        'Moeda de Origem': [from_currency],
        'Moeda de Destino': [to_currency],
        'Valor Original': [amount],
        'Taxa de Câmbio': [exchange_rate],
        'Valor Convertido': [converted_amount]
    }
    
    df = pd.DataFrame(data)
    
    # Perguntar ao usuário se deseja salvar a planilha e gerar gráfico
    save_excel = input("Deseja salvar os dados em uma planilha Excel? (s/n): ").lower()
    
    if save_excel == 's':
        # Salvar a planilha
        excel_filename = 'dados_moedas.xlsx'
        df.to_excel(excel_filename, index=False)
        print(f"Planilha salva como {excel_filename}")
        
        # Perguntar se deseja gerar um gráfico
        generate_graph = input("Deseja gerar um gráfico dos valores? (s/n): ").lower()
        if generate_graph == 's':
            # Gerar gráfico simples
            plt.bar(df['Moeda de Origem'] + " para " + df['Moeda de Destino'], df['Valor Convertido'])
            plt.xlabel('Conversão')
            plt.ylabel('Valor Convertido')
            plt.title('Conversão de Moedas')
            plt.show()
            print("Gráfico gerado!")

if __name__ == "__main__":
    currency_converter()
