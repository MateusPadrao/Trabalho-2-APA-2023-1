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

# Exemplo de uso
lista_produtores = carregar_dados_produtores('Fretes.csv')
lista_produtos = carregar_dados_produtos('Produtos.csv')

# Combinar os dados dos produtores e dos produtos

# Para cada produtor
for produtor in lista_produtores:
    # Para cada produto
    for produto in lista_produtos:
        # Se o fornecedor do produto for o produtor atual
        if produto['fornecedor'] == produtor['nome']:
            # Adicionar o produto na lista de produtos do produtor descartando o parâmetro fornecedor, pois já sabemos que é o produtor atual
            produto_sem_fornecedor = produto.copy()
            del produto_sem_fornecedor['fornecedor']
            produtor['produtos'].append(produto_sem_fornecedor)

# lista_produtores agora contém os dados dos produtores e seus produtos
print(lista_produtores[0])


'''{
    'nome': 'Matheus Nogueira',
    'frete': 12.0,
    'produtos': 
    [
        {
            'tipo': 'Hortifruti',
            'nome': 'Laranja de Umbigo', 
            'valor': 11.0, 
            'quantidade_num': 1.0, 
            'quantidade_unidade': 'kg'
        }, 
        {
            'tipo': 'Laticínio', 
            'nome': 'Nata Piá', 
            'valor': 12.0, 
            'quantidade_num': 200.0, 
            'quantidade_unidade': 'g'
        }, 
        {
            'tipo': 'Laticínio', 
            'nome': 'Nata Tirol', 
            'valor': 12.0, 
            'quantidade_num': 200.0, 
            'quantidade_unidade': 'g'
        }, 
        {
            'tipo': 'Hortifruti', 
            'nome': 'Abacaxi', 
            'valor': 11.0, 
            'quantidade_num': 1.0, 
            'quantidade_unidade': 'un'
        }, 
        {
            'tipo': 'Hortifruti', 
            'nome': 'Cebola', 
            'valor': 12.0, 
            'quantidade_num': 1.0, 
            'quantidade_unidade': 'kg'
        }, 
        {
            'tipo': 'Laticínio', 
            'nome': 'Manteiga', 
            'valor': 19.0, 
            'quantidade_num': 200.0, 
            'quantidade_unidade': 'g'
        }, 
        {
            'tipo': 'Laticínio', 
            'nome': 'Manteiga', 
            'valor': 61.0, 
            'quantidade_num': 1.0, 
            'quantidade_unidade': 'kg'
        }
    ]
}'''

