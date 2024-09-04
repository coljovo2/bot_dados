import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para realizar o scraping da tabela de imposto de renda
def get_income_tax_table():
    url = 'https://www.moneytimes.com.br/imposto-de-renda-brasil-nao-tem-maior-imposto-do-mudo-veja-onde-a-mordida-do-leao-e-maior/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Erro ao acessar o site.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Localiza a tabela com base em tags específicas (assumindo que a tabela está em 'table')
    table = soup.find('table')
    
    # Se não encontrar a tabela, retorna uma mensagem de erro
    if table is None:
        print("Tabela não encontrada.")
        return None
    
    # Extraindo as linhas da tabela
    rows = table.find_all('tr')
    
    # Criando uma lista de dicionários para armazenar os dados da tabela
    country_tax_data = []
    for row in rows[1:]:  # Ignorando o cabeçalho
        cols = row.find_all('td')
        if len(cols) >= 3:
            rank = cols[0].text.strip()  # Posição na tabela
            country = cols[1].text.strip()  # País
            tax_rate = cols[2].text.strip()  # Alíquota
            
            # Adiciona os dados do país à lista
            country_tax_data.append({
                'rank': rank,
                'country': country,
                'tax_rate': tax_rate
            })
    
    return country_tax_data

# Função para interagir com o usuário e registrar as respostas
def ask_user_for_country(country_tax_data):
    selected_countries = []  # Lista para armazenar os países selecionados pelo usuário
    
    while True:
        # Pergunta ao usuário o país que ele quer saber
        country_name = input("Digite o nome do país que você quer saber o imposto de renda (ou 'sair' para encerrar): ").strip().title()
        
        if country_name.lower() == 'sair':
            print("Encerrando o programa.")
            break
        
        # Procura o país na lista
        country_info = next((item for item in country_tax_data if country_name in item['country']), None)
        
        if country_info:
            print(f"O país {country_info['country']} está na posição {country_info['rank']} com uma alíquota de imposto de renda de {country_info['tax_rate']}.")
            selected_countries.append(country_info)  # Adiciona o país selecionado à lista
        else:
            print(f"O país {country_name} não foi encontrado na tabela.")
        
        # Pergunta se o usuário quer fazer outra busca
        repeat = input("Gostaria de procurar outro país? (sim/não): ").strip().lower()
        if repeat != 'sim':
            print("Encerrando o programa.")
            break
    
    return selected_countries

# Função para salvar os dados em uma planilha Excel
def save_to_excel(selected_countries):
    if selected_countries:
        df = pd.DataFrame(selected_countries)
        df.to_excel("imposto_de_renda.xlsx", index=False)
        print("Os dados foram salvos na planilha 'imposto_de_renda.xlsx'.")
    else:
        print("Nenhum dado foi selecionado para salvar.")

# Função principal para rodar o bot
def main():
    print("Buscando dados da tabela de imposto de renda...")
    country_tax_data = get_income_tax_table()
    
    if country_tax_data:
        print("Dados obtidos com sucesso!")
        selected_countries = ask_user_for_country(country_tax_data)
        save_to_excel(selected_countries)  # Salva os dados selecionados em Excel
    else:
        print("Não foi possível obter os dados.")

# Executa o programa
if __name__ == "__main__":
    main()
