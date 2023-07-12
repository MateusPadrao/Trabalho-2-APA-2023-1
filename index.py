import csv
import re

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
                # Adicionar o produto na lista de produtos do produtor descartando o parâmetro fornecedor, pois já sabemos que é o produtor atual
                # produto_sem_fornecedor = produto.copy()
                # del produto_sem_fornecedor['fornecedor']
                # produtor['produtos'].append(produto_sem_fornecedor)
                produtor['produtos'].append(produto)
    return lista_produtores

'''def calcular_melhor_compra(carrinho, produtores, nome_arquivo_saida):
    # Tabela de memoização para armazenar o custo mínimo de cada subproblema
    tabela_memoizacao = {}

    # Função auxiliar para calcular o custo mínimo
    def calcular_custo_minimo(indice_produto, quantidade_restante):
        if indice_produto >= len(carrinho) or quantidade_restante == 0:
            return 0

        # Verificar se o subproblema já foi resolvido anteriormente
        if (indice_produto, quantidade_restante) in tabela_memoizacao:
            return tabela_memoizacao[(indice_produto, quantidade_restante)]

        produto = carrinho[indice_produto]
        custo_minimo = float('inf')

        # Iterar sobre as quantidades possíveis para o produto atual
        for quantidade_atual in range(int(quantidade_restante) + 1):
            custo_atual = (
                produto['valor'] * quantidade_atual +
                produto['produtor']['frete'] +
                calcular_custo_minimo(indice_produto + 1, quantidade_restante - quantidade_atual)
            )
            custo_minimo = min(custo_minimo, custo_atual)

        # Armazenar o custo mínimo na tabela de memoização
        tabela_memoizacao[(indice_produto, quantidade_restante)] = custo_minimo
        return custo_minimo

    # Calcular o custo mínimo para a quantidade total do carrinho
    custo_minimo_total = calcular_custo_minimo(0, sum(produto['quantidade_num'] for produto in carrinho))

    # Gerar o arquivo CSV com as informações da melhor compra
    with open(nome_arquivo_saida, 'w', newline='') as arquivo_saida:
        escritor_csv = csv.writer(arquivo_saida)
        escritor_csv.writerow(['Identificação do Produto', 'Identificador do Fornecedor', 'Quantidade Requerida', 'Valor do Item'])

        # Função auxiliar para escrever as informações do produto no arquivo CSV
        def escrever_produto(produto, quantidade_restante):
            quantidade_atual = min(produto['quantidade'], quantidade_restante)
            escritor_csv.writerow([
                produto['identificacao'],
                produto['fornecedor'],
                quantidade_atual,
                produto['valor']
            ])
            return quantidade_restante - quantidade_atual

        quantidade_restante = sum(produto['quantidade_num'] for produto in carrinho)

        # Percorrer os produtos e escrever as informações no arquivo CSV
        for produto in carrinho:
            for produtor in produtores:
                produtos_do_produtor = [p for p in produtor['produtos'] if p['nome'] == produto['identificacao']]
                if produtos_do_produtor:
                    produto['produtor'] = produtor
                    produto['valor'] = produtos_do_produtor[0]['valor']
                    quantidade_restante = escrever_produto(produto, quantidade_restante)

        valor_total_produtos = custo_minimo_total - sum(produto['produtor']['frete'] for produto in carrinho)
        valor_total_fretes = sum(produto['produtor']['frete'] for produto in carrinho)
        valor_total_compra = custo_minimo_total

        escritor_csv.writerow([])
        escritor_csv.writerow(['Valor Total dos Produtos', 'Valor Total dos Fretes', 'Valor Total da Compra'])
        escritor_csv.writerow([valor_total_produtos, valor_total_fretes, valor_total_compra])

    print("A melhor compra foi calculada e as informações foram salvas no arquivo:", nome_arquivo_saida)
'''

# Exemplo de uso
lista_produtores = carregar_dados_produtores('Fretes.csv')
lista_produtos = carregar_dados_produtos('Produtos.csv')
lista_produtores = combinar_dados_produtores_produtos(lista_produtores, lista_produtos) # lista_produtores agora contém os dados dos produtores e seus produtos
carrinho = carregar_carrinho('carrinho_exemplo.csv')

# calcular_melhor_compra(carrinho, lista_produtores, 'melhor_compra.csv')
# Combinar os dados dos produtores e dos produtos



# lista_produtores agora contém os dados dos produtores e seus produtos
'''print(carrinho)
print('\n\n')
print(lista_produtores[1])'''




