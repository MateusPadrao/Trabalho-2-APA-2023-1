import csv
import re
import itertools
import random
import tkinter as tk
from tkinter import filedialog

def separar_numeros(texto):
    """
    Separa os números de um texto.
    :param texto: texto a ser analisado
    :return: valor em float e unidade de medida em string ou None, None
    """
    padrao = r"(\d+(?:\.\d+)?)\s*(\D+)"
    correspondencias = re.match(padrao, texto)
    if correspondencias:
        valor = float(correspondencias.group(1))
        unidade = correspondencias.group(2)
        return valor, unidade
    else:
        return None, None
    
def carregar_dados_produtores(nome_arquivo):
    """
    Carrega os dados dos produtores de um arquivo CSV.
    :param nome_arquivo: nome do arquivo CSV
    :return: lista de dicionários com os dados dos produtores
    """
    
    dados_produtores = []
    with open(nome_arquivo, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        # Ignorar o cabeçalho, se houver
        next(leitor_csv)
        for linha in leitor_csv:
            nome = linha[0].strip()  # nome do produtor
            frete = float(linha[1])  # valor do frete
            dados_produtores.append({
                'nome': nome,
                'frete': frete,
                'produtos': []
            })
    return dados_produtores

def carregar_dados_produtos(nome_arquivo):
    """
    Carrega os dados dos produtos de um arquivo CSV.
    :param nome_arquivo: nome do arquivo CSV
    :return: lista de dicionários com os dados dos produtos
    """
    
    dados_produtos = []
    with open(nome_arquivo, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        # Ignorar o cabeçalho, se houver
        next(leitor_csv)
        for linha in leitor_csv:
            tipo = linha[0].strip()  # tipo do produto
            nome = linha[1].strip()  # nome do produto
            valor = float(linha[2])  # valor do produto
            quantidade = linha[3].strip()  # quantidade do produto
            qtde_numerica, und_medida = separar_numeros(quantidade)
            if und_medida == 'g':
                qtde_numerica /= 1000
                und_medida = 'kg'
            fornecedor = linha[4].strip()  # fornecedor do produto
            dados_produtos.append({
                'tipo': tipo,
                'nome': nome,
                'valor': valor,
                'quantidade_num': qtde_numerica,
                'quantidade_unidade': und_medida,
                'fornecedor': fornecedor
            }) # adiciona o dicionário produto na lista de produtos
    return dados_produtos

def carregar_carrinho(nome_arquivo):
    """
    Carrega os dados do carrinho de um arquivo CSV.
    :param nome_arquivo: nome do arquivo CSV
    :return: lista de dicionários com os dados do carrinho
    """
    
    dados_carrinho = []
    with open(nome_arquivo, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        # Ignorar o cabeçalho, se houver
        next(leitor_csv)
        for linha in leitor_csv:
            nome_prod = linha[0].strip()  # nome do produto
            quantidade = linha[1].strip()  # quantidade do produto
            qtde_numerica, und_medida = separar_numeros(quantidade)
            dados_carrinho.append({
                'nome_prod': nome_prod,
                'quantidade_num': qtde_numerica,
                'quantidade_unidade': und_medida
            }) # adiciona o dicionário produto na lista de produtos
    return dados_carrinho

def combinar_dados_produtores_produtos(lista_produtores, lista_produtos):
    """
    Coloca os produtos de cada produtor na lista de produtos do produtor.
    :param lista_produtores: lista de dicionários, onde cada dicionário representa um produtor
    :param lista_produtos: lista de dicionários, onde cada dicionário representa um produto
    :return: lista de dicionários, onde cada dicionário representa um produtor, com a lista de produtos do produtor
    """
    
    # Para cada produtor
    for produtor in lista_produtores:
        # Para cada produto
        for produto in lista_produtos:
            # Se o fornecedor do produto for o produtor atual
            if produto['fornecedor'] == produtor['nome']:
                # Adicionar o produto à lista de produtos do produtor
                produtor['produtos'].append(produto)
    return lista_produtores

def calcular_melhor_compraAG(carrinho, produtores, populacao_inicial=50, geracoes=100):
    """
    Abordagem de algoritmo genético para calcular a melhor compra. Testado e funcional para o caso de teste.
    :param carrinho: lista de dicionários, onde cada dicionário representa um produto do carrinho
    :param produtores: lista de dicionários, onde cada dicionário representa um produtor
    :param nome_arquivo_saida: nome do arquivo CSV de saída
    :param populacao_inicial: número de soluções na população inicial com valor padrão de 50. É a primeira geração de soluções candidatas.
    :param geracoes: número de gerações com valor padrão de 100. Representa o número de vezes que o algoritmo genético será executado.
    :return: None
    """
    
    # Função para avaliar a aptidão de uma solução
    def avaliar_aptidao(sol):
        custo_total = 0
        for produto in sol:
            custo_total += produto['valor'] + produto['produtor']['frete']
        return custo_total

    # Gerar população inicial aleatória
    populacao = []
    for _ in range(populacao_inicial):
        solucao = []
        for produto in carrinho:
            # Selecionar um fornecedor aleatório para cada produto no carrinho
            fornecedores = [produtor for produtor in produtores if produto['nome_prod'] in [p['nome'] for p in produtor['produtos']]]
            fornecedor = random.choice(fornecedores) if fornecedores else None
            if fornecedor:
                # Adicionar o produto selecionado à solução
                produto['produtor'] = fornecedor
                produto['valor'] = next((p['valor'] for p in fornecedor['produtos'] if p['nome'] == produto['nome_prod']), 0)
                solucao.append(produto)
        populacao.append(solucao)

    # Avaliar aptidão da população inicial
    populacao_avaliada = [(sol, avaliar_aptidao(sol)) for sol in populacao]

    # Algoritmo genético
    for _ in range(geracoes):
        # Seleção dos pais (torneio binário)
        pais = []
        for _ in range(populacao_inicial):
            pai1 = random.choice(populacao_avaliada)
            pai2 = random.choice(populacao_avaliada)
            pais.append(pai1 if pai1[1] < pai2[1] else pai2)

        # Crossover
        filhos = []
        for i in range(0, populacao_inicial, 2):
            pai1, pai2 = pais[i], pais[i + 1]
            ponto_corte = random.randint(1, len(carrinho) - 1)
            filho1 = pai1[0][:ponto_corte] + pai2[0][ponto_corte:]
            filho2 = pai2[0][:ponto_corte] + pai1[0][ponto_corte:]
            filhos.append(filho1)
            filhos.append(filho2)

        # Mutação
        for solucao in filhos:
            if random.random() < 0.1:  # taxa de mutação de 10%
                posicao = random.randint(0, len(solucao) - 1)
                produto = solucao[posicao]
                fornecedores = [produtor for produtor in produtores if produto['nome_prod'] in [p['nome'] for p in produtor['produtos']]]
                fornecedor = random.choice(fornecedores) if fornecedores else None
                if fornecedor:
                    # Mutação: selecionar um novo fornecedor para o produto
                    produto['produtor'] = fornecedor
                    produto['valor'] = next((p['valor'] for p in fornecedor['produtos'] if p['nome'] == produto['nome_prod']), 0)

        # Avaliar aptidão dos filhos
        filhos_avaliados = [(sol, avaliar_aptidao(sol)) for sol in filhos]

        # Seleção dos sobreviventes (elitismo)
        nova_populacao = sorted(populacao_avaliada + filhos_avaliados, key=lambda x: x[1])[:populacao_inicial]

        # Atualizar população
        populacao_avaliada = nova_populacao

    # Melhor solução encontrada
    melhor_solucao = populacao_avaliada[0][0]        

    return melhor_solucao

def calcula_valor_total(solucao):
    valor_total_produtos = sum(produto['valor'] for produto in solucao)
    valor_total_fretes = sum(produto['produtor']['frete'] for produto in solucao)
    valor_total_compra = valor_total_produtos + valor_total_fretes

    valores = {"valor_total_produtos": valor_total_produtos, "valor_total_fretes": valor_total_fretes, "valor_total_compra": valor_total_compra}
    
    return valores

def gerar_csv(nome_arquivo_saida, melhor_solucao):
    # Gerar o arquivo CSV com as informações da melhor compra
    with open(nome_arquivo_saida, 'w', newline='') as arquivo_saida:
        escritor_csv = csv.writer(arquivo_saida)
        escritor_csv.writerow(['Identificacao do Produto', 'Identificador do Fornecedor', 'Quantidade Requerida', 'Valor do Item'])

        for produto in melhor_solucao:
            escritor_csv.writerow([
                produto['nome_prod'],
                produto['produtor']['nome'],
                produto['quantidade_num'],
                produto['valor']
            ])

        valores = calcula_valor_total(melhor_solucao)

        escritor_csv.writerow([])
        escritor_csv.writerow(['Valor Total dos Produtos', 'Valor Total dos Fretes', 'Valor Total da Compra'])
        escritor_csv.writerow([valores["valor_total_produtos"], valores["valor_total_fretes"], valores["valor_total_compra"]])

    print("A melhor compra foi calculada e as informações foram salvas no arquivo:", nome_arquivo_saida)

def melhor_melhor_compra(carrinho, lista_produtores):
    melhor_compra = calcular_melhor_compraAG(carrinho, lista_produtores)
    valores_melhor = calcula_valor_total(melhor_compra)

    for i in range(10):
        possivel_melhor_compra = calcular_melhor_compraAG(carrinho, lista_produtores)
        valores_possivel_melhor = calcula_valor_total(possivel_melhor_compra)

        if valores_melhor['valor_total_compra'] > valores_possivel_melhor['valor_total_compra']:
            valores_melhor = valores_possivel_melhor
            melhor_compra = possivel_melhor_compra
    
    print(f"melhor valor na teoria: {valores_melhor['valor_total_compra']}")
    print(f"melhor valor na pratica: {calcula_valor_total(melhor_compra)['valor_total_compra']}")

    return melhor_compra

def main():
    nome_arquivo_saida = 'melhor_compra.csv'
    arquivo_produtores = filedialog.askopenfilename(title='Selecione o arquivo de produtores', filetypes=[('CSV', '*.csv')])
    arquivo_produtos = filedialog.askopenfilename(title='Selecione o arquivo de produtos', filetypes=[('CSV', '*.csv')])
    arquivo_carrinho = filedialog.askopenfilename(title='Selecione o arquivo do carrinho', filetypes=[('CSV', '*.csv')])

    lista_produtores = carregar_dados_produtores(arquivo_produtores) # lista_produtores contém os dados dos produtores
    lista_produtos = carregar_dados_produtos(arquivo_produtos) # lista_produtos contém os dados dos produtos
    lista_produtores = combinar_dados_produtores_produtos(lista_produtores, lista_produtos) # lista_produtores agora contém os dados dos produtores e seus produtos
    carrinho = carregar_carrinho(arquivo_carrinho) # carrinho contém os dados do carrinho
    melhor_solucao = melhor_melhor_compra(carrinho, lista_produtores)
    gerar_csv(nome_arquivo_saida, melhor_solucao)

main()
