# Trabalho-2-APA-2023-1 - Disciplina de Análise e Projeto de Algoritmos do curso de Engenharia de Computação da Universidade Federal do Pampa - Campus Bagé

# Sistema de Compra e Venda de Produtos

Este projeto é um sistema de compra e venda de produtos voltado para pequenos produtores rurais e seus clientes. O sistema permite que os produtores cadastrem seus produtos e os clientes possam montar um carrinho de compras com os itens desejados, buscando a melhor combinação de produtos e produtores para minimizar o custo total da compra, considerando os valores dos produtos e dos fretes.

## Funcionamento

O sistema é composto por três principais etapas:

1. **Carregamento dos Dados**: Os dados dos produtores e produtos são carregados a partir de arquivos CSV, contendo informações sobre os produtores, seus produtos, valores, quantidades e fretes.

2. **Algoritmo Genético**: A otimização do carrinho de compras é realizada utilizando um algoritmo genético. O algoritmo começa gerando uma população inicial aleatória de soluções (carrinhos de compras) e, em seguida, realiza seleção, crossover e mutação para gerar novas soluções. O processo é repetido por um número de gerações especificado, e a melhor solução é escolhida como a combinação de produtos e produtores que resulta no menor custo total.

3. **Geração do Arquivo de Saída**: A melhor solução é escrita em um arquivo CSV com as informações da melhor compra. O arquivo contém detalhes sobre cada produto no carrinho, como identificação, fornecedor, quantidade requerida, valor unitário e valor total. Além disso, são fornecidos o valor total dos produtos, o valor total dos fretes e o valor total da compra.

## Como Usar

1. Clone o repositório para o seu computador:

```bash
git clone https://github.com/MateusPadrao/Trabalho-2-APA-2023-1.git
cd Trabalho-2-APA-2023-1
```

2. Certifique-se de ter o Python instalado (versão 3.x).

3. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

4. Tenha no seu computador os arquivos Produtores.csv e Produtos.csv e gere um arquivo Carrinho.csv para execução da otimização.

5. O arquivo `index.py` é o arquivo com o código fonte.

6. Execute o programa:

```bash
python index.py
```

7. O programa irá executar o algoritmo genético e gerar o arquivo de saída com a melhor compra.

## Formato dos Arquivos CSV

### Arquivo de Produtores

O arquivo CSV dos produtores deve conter as seguintes colunas:

- `Nome`: Nome do produtor.
- `Frete`: Valor do frete cobrado pelo produtor para entrega.

Exemplo:

```
Nome;Frete
Produtor1;10.0
Produtor2;15.0
```

### Arquivo de Produtos

O arquivo CSV dos produtos deve conter as seguintes colunas:

- `Tipo`: Tipo do produto.
- `Nome`: Nome do produto.
- `Valor`: Valor unitário do produto.
- `Quantidade`: Quantidade disponível do produto no fornecedor.
- `Fornecedor`: Nome do produtor que fornece o produto.

Exemplo:

```
Tipo;Nome;Valor;Quantidade;Fornecedor
Tipo1;Produto1;5.0;20;Produtor1
Tipo2;Produto2;8.0;15;Produtor1
```

### Arquivo de Carrinho

O arquivo CSV do carrinho de compras deve conter as seguintes colunas:

- `Produto`: Nome do produto desejado.
- `Quantidade`: Quantidade desejada do produto.

Exemplo:

```
Produto;Quantidade
Produto1;2
Produto2;1
Produto3;3
```

## Contribuindo

Contribuições são bem-vindas! Ainda existem alguns problemas, então se tiver alguma ideia de melhoria ou quiser adicionar novos recursos, sinta-se à vontade para abrir uma issue ou enviar um pull request.
