# House Rocket

<img src="images/house_rocket_logo.png" width=50% height=50%/>

Disclaimer: Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais e não têm objetivo comercial. O Dataser público está disponivel no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction).

Este projeto é um desafio da [Comunidade DS](https://www.comunidadedatascience.com/).

<!-- O dashboard com os produtos de dados em produção pode ser acessado via navegador pelo [Heroku](https://dso-analytics-house-rocket.herokuapp.com/). -->


## 1. Problema de negócios
### 1.1 Problema
A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia. O CEO da House Rocket gostaria de maximizar a receita da empresa encontrando boas oportunidades de negócio.

Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita.

### 1.2 Objetivo
O objetivo do projeto é encontrar, através de Insights gerados por Análise Exploratória de Dados (EDA), oportunidades de negócios na região de atuação da House Rocket.


### 1.3 Demandas
Produto de dados solicitado: 
* Dashboard interativo do portfólio disponível, com todas informações mais relevantes disponíveis atualmente, para que o CEO e o time de negócios  possa realizar análises (self-service BI).
   
* Respostas para duas questões:
  - 1 - Quais são os imóveis que deveríamos comprar?
  - 2 - Uma vez o imóvel comprado, qual o melhor momento para vendê-lo, e por qual preço?
  - 3 - A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?

## 2. Premissas
- Todos os produtos de dados entregues devem ser acessíveis via internet.
- O planejamento da solução será validado com os times de negócio, visando garantir que as soluções desenvolvidas são úteis na sua tomada de decisão.

As variáveis do dataset original são:

Variável | Definição
------------ | -------------
|id | Identificador de cada imóvel.|
|date | Data em que a imóvel ficou disponível.|
|price | O preço de cada imóvel, considerado como preço de compra.|
|bedrooms | Número de quartos.|
|bathrooms | O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.|
|sqft_living | Pés quadrados do interior das casas.|
|sqft_lot | Pés quadrados do terreno das casas.|
|floors | Número de andares.|
|waterfront | Uma variável fictícia para saber se a casa tinha vista para a orla ou não, '1' se o imóvel tem uma orla, '0' se não.|
|view | Vista, Um índice de 0 a 4 de quão boa era a visualização da imóvel.|
|condition | Um índice de 1 a 5 sobre o estado das moradias, 1 indica imóvel degradado e 5 excelente.|
|grade | Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 fica aquém da construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade.|
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo.|
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo.|
|yr_built | Ano de construção da imóvel.|
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as imóvel nunca renovadas.|
|zipcode | Um código de cinco dígitos para indicar a área onde se encontra a imóvel.|
|lat | Latitude.|
|long | Longitude.|
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.|
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.|

## 3. Planejamento da solução
### 3.1. Produto final 

- Um grande dashboard interativo acessível via navegador, contendo os produtos de dados solicitados pelos times de negócio.
  
### 3.2. Ferramentas 
Quais ferramentas serão usadas no processo?
- Visual Studio code;
- Jupyter Notebook;
- Git, Github;
- Python;
- Streamlit;
- Heroku.
  
## 4. Os 3 principais insights dos dados

#### 1 Imóveis com vista para o mar são, em média, 212.64% mais caros que os sem vista.
* Insight de negócio: Prospectar para compra imóveis com vista para o mar, quando estiverem com valor até 150% maior que imóveis sem vista na mesma região. Aliar outros critérios relevantes como o seu estado de conservação, para a tomada de decisão.

#### 2 Imóveis com data de construção menor que 1955, são em média apenas 0.79 % mais baratos que os após 1955.
* Insight de negócio: Prospectar imóveis com data de construção menor de 1955, que tenham passado por reformas, e que estejam com preço no mínimo 10% abaixo da média dos imóveis com ano de construção maior que 1955 na mesma região.

#### 3 Imóveis reformados na mesma região, tem preços em média 17.49 % maiores que imóveis não reformados.
* Insight de negócio: Prospectar imóvies reformados, onde o preço do imóvel seja até 5% maior que a média dos imóveis não reformados da região, nas mesmas condições.

## 5. Resultados financeiros para o negócio
De acordo com os critérios definidos, foram sugeridos os imóvies com as seguintes condições para a compra: 

* Preço da propriedade abaixo da mediana da região;
* Condição da propriedade acima de media da região;
* Área contruída da propriedade é maior do que a mediana da região;
* O terreno da propriedade é maior do que a mediana da região.

De acordo com a região, foi observada a sazonalidade em que a média de preços é maior, e recomendada a venda nessas épocas com valor 30% acima da mediana das respectivas.

Considerando apenas o lucro por imóvel, o lucro total estimado caso as sugestões de compra e venda sejam seguidas é de aproximadamente o $61 milhões de dólares, com uma margem média de lucro esperada de 31.52%.

## 5. Conclusão
O objetivo do projeto foi alcançado, dado que os produtos de dados propostos foram gerados com sucesso. Os times já podem utilizar a solução para a tomada de decisão e o atingimento de metas na House Rocket.

<!-- O dashboard com os produtos de dados em produção pode ser acessado via navegador pelo [Heroku](https://dso-analytics-house-rocket.herokuapp.com/). -->

## 7. Próximoss passos

Algumas melhorias nos dashboard podem ser incrementadas no futuro:

* Desenvolver uma solução de Machine Learning para prever com maior acuracia os preços de venda dos imóveis, objetivando aumentar a margem média de lucro.
* Implementar um código de Geopandas para buscar os bairros dos imóveis e melhorar o filtro do CEO.
* Recomendar a compra de imóveis na baixa temporada e vendê-los na alta. Levando em consideração que as estações do 
ano inverno e outono os preços dos imóveis estão mais desvalorizados e as estações do ano primavera e verão são as 
estações que os imóveis estão mais valorizados.   

## 6 Referências
* Este Projeto de Insights é parte do curso "Python do Zero ao DS", da [Comunidade DS](https://www.comunidadedatascience.com/).
* O Dataset foi obtido no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction).

* Os significados das variáveis foi obtido no [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/).