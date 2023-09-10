# Engenharia_de_Dados_Tesouro_Nacional_RMD
O Relatório Mensal da Dívida Pública Federal (RMD) apresenta informações sobre emissões, resgates, estoque, composição, programa Tesouro Direto, perfil de vencimentos e custo médio, dentre outras, da Dívida Pública Federal - DPF, nela incluídas as dívidas interna e externa de responsabilidade do Tesouro Nacional em mercado. O documento reúne ainda informações sobre a reserva de liquidez e as garantias honradas pela União.
Fonte: Tesouro Nacional Transparente

# Projeto
Conforme explicado, explanado, e visando a coleta e organização dos dados (que serão coletados via web scraping, oriundos de um arquivo xlsx - compactados em um zip), para concluir essa tarefa, e viabilizar o relatório à equipe de Dados, separei o projeto em algumas etapas, sendo elas:

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils, nesse arquivo há informações pertinentes a fonte extraída, configurações quanto ao acesso à tabela de banco de dados PostgreSQL usado, credenciais da conta cloud AWS e informações pertinentes as planilhas desejadas, pré-selecionadas pelo usuário;

# 2) Criei um processo ETL:
- E: Extração dos dados respectivos oriundos da fonte https://www.tesourotransparente.gov.br/publicacoes/relatorio-mensal-da-divida-rmd/.

- T: Posterior à coleta dos dados, e visando a geração de um relatório formal relacionado às cotações, tratei os dados e gerei um dataframe.

- L: Logo após os tratamentos, e tendo um dataframe preparado, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'R_Mensal_Divida_[%Y%m%d].csv', um arquivo já tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) Criei um processo EL:
- E: Para validar a garantia dos dados, para a base que estou montando, extraí o arquivo zip base, com a estrutura de nome: '[Anexo_RMD_%B_%y].zip'.

- L: Como a intenção é justamente usar como garantia de integridade, salvei ele na pasta do mês e, posteriormente, no Bucket S3 desejado.

--- FAZER
# 4) Orquestrei com Airflow
- Como a intenção é montar um histórico, usei o Apache Airflow para orquestar os códigos. As coletas serão realizadas a cada 5 minutos, diariamente, 7 dias por semana, durante todos os dias do ano.