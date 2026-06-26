# Sistema de Contabilidade: Custo de Produção do App Delivery

## Descrição da Atividade
Esta atividade tem como objetivo calcular o custo total de manutenção e operação de um aplicativo, utilizando o método de Custeio Baseado em Atividades (Custeio ABC). O desafio consiste em distribuir os custos indiretos da equipe de tecnologia (R$ 40.000,00 mensais) entre quatro etapas principais do ciclo de vida do software, baseando-se no esforço real medido pelo consumo de direcionadores de custos.

## Dados do Projeto
Os dados utilizados para o cálculo são divididos em:
1. **Capacidade e Custos da Empresa:** Volume total da capacidade da empresa e custo do pool de recursos para cada uma das quatro etapas (Desenvolvimento, Testes, Deploy e Suporte).
2. **Consumo Real do Mês:** Dados específicos do comportamento do App Delivery no mês em questão (horas de programação, bugs encontrados, deploys realizados e chamados atendidos).

Os dados de entrada são carregados a partir do arquivo `dados_app_delivery.csv`.

## Funcionamento do Algoritmo
O algoritmo realiza o cálculo do custo unitário para cada etapa, dividindo o custo do pool pela capacidade total de cada driver. Em seguida, multiplica a taxa do direcionador pelo consumo real do mês, obtendo o custo alocado por atividade. Por fim, soma-se o custo de todas as atividades para encontrar o custo total de produção do aplicativo no mês.

## Funções do Código
* `calcular_custo_unitario(custo_pool, capacidade_total)`: Executa a fórmula do Custeio ABC para determinar a taxa por unidade.
* `calcular_custo_etapa(custo_unitario, consumo_real)`: Calcula o custo total alocado para uma atividade específica com base no consumo real.
* `carregar_dados(caminho_csv)`: Responsável pela leitura e estruturação dos dados contidos no arquivo CSV.
* `processar_contabilidade(dados)`: Aplica as funções de cálculo para todas as etapas e calcula o custo total do app.
* `exibir_terminal(resultados, custo_total_app)`: Formata e apresenta os resultados tabulados no console.
* `gerar_pdf(resultados, custo_total_app)`: Gera um relatório completo em formato PDF, contendo tabelas e análise gráfica.

## Menu do Sistema
O sistema oferece as seguintes opções:
1. **Exibir respostas em terminal:** Apresenta os cálculos de custo unitário, consumo e custo total por etapa, além de uma análise de impacto financeiro. 
   [Visualizar exemplo de saída no terminal](prints/resultadoTerminal.png)
2. **Gerar pdf com resultados:** Cria um relatório profissional com os dados consolidados e um gráfico de distribuição. 
   [Acessar resultados.pdf](Resultados.pdf)
3. **Sair:** Encerra a execução do sistema.

## Informações de Uso
### Pré-requisitos
Certifique-se de ter o Python instalado e as seguintes dependências:
pip install fpdf matplotlib pandas

## Como Executar
1. Clone o repositório.
2. Certifique-se de que o arquivo dados_app_delivery.csv está na raiz do projeto.
3. Execute o programa através do terminal: 
**python main.py**

## Informações Adicionais
 - Autor e Desenvolvedor: Gustavo Anibele.
Em caso de dúvidas ou sugestões, entre em contato pelo e-mail: 
[email](mailto:gustavoanibele@gmail.com)
