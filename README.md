# TESOURO NACIONAL RMD - ENGENHERIA DE DADOS
- O Relatório Mensal da Dívida Pública Federal (RMD) apresenta informações sobre emissões, resgates, estoque, composição, programa Tesouro Direto, perfil de vencimentos e custo médio, dentre outras, da Dívida Pública Federal - DPF, nela incluídas as dívidas interna e externa de responsabilidade do Tesouro Nacional em mercado. O documento reúne ainda informações sobre a reserva de liquidez e as garantias honradas pela União.
Fonte: Tesouro Nacional Transparente

- OBS.: ESSE PROJETO NÃO É UMA RECOMENDAÇÃO DE INVESTIMENTO, MAS UMA INICIATIVA DE FORNECER ALGUMAS INFORMAÇÕES E DADOS ÚTEIS - E PÚBLICOS - AOS INVESTIDORES.

---------------------------------------------------------------------------------------------
# PROJETO
- Levando em conta a riqueza de informações que o Tesouro Nacional nos concede (como: monitoramento das finanças públicas, possibilidade de tomadas de decisões de investimento em títulos governamentais, avaliação da saúde financeira do país etc - informações públicas), fiz a extração - usando web scraping - dos títulos públicos mais comuns e populares emitidos pelo Tesouro Nacional no Brasil. A partir desses dados - coletados e organizados, os investidores, de diferentes perfis e objetivos financeiros, poderão usá-los como auxiliadores em tomadas de decisões, escolhendo o título lhe atender melhor. Para conclusão desse projeto - abordando obtenção dos dados, tratamento e armazenamento deles -, foram necessárias algumas etapas, sendo elas:

---------------------------------------------------------------------------------------------
# ETAPAS

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils -, nesse arquivo há informações pertinentes a fonte extraída, o tipo do arquivo a ser gerado, parâmetros, configurações quanto ao acesso à tabela de banco de dados PostgreSQL usado, credenciais da conta cloud AWS - usuário IAM, e informações pertinentes as planilhas desejadas, pré-selecionadas pelo usuário;

# 2) Criei um processo ETL:
- E: Extração dos dados respectivos oriundos da fonte https://www.tesourotransparente.gov.br/publicacoes/relatorio-mensal-da-divida-rmd/;

- T: Posterior à coleta dos dados, e visando a geração de um relatório formal relacionado aos títulos, tratei os dados e gerei um dataframe;

- L: Logo após os tratamentos, e tendo um dataframe preparado, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'R_Mensal_Divida_[%Y%m%d].['formatodesejado']', um arquivo já tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) Criei um processo EL:
- E: Para garantir a integridade dos dados, extraí o arquivo zip original, com a estrutura de nome: '[Anexo_RMD_%B_%y].zip'. (%B: o mês por extenso e primeira letra maiúscula, %y: ano com 2 dígitos);

- L: Como a intenção é justamente usar como garantia de integridade, salvei ele na pasta do mês desejado, dentro do Bucket S3 configurado - informado logo após.

# 4) Criei Bucket S3:
- Usei o Bucket S3 (que serve de 'armazém' para arquivos, conhecidos como objetos) para guardar os objetos gerados com segurança, organização e escalabilidade. Para inserção no S3, fiz uso do Boto3, que é um SDK (Software Development Kit) da AWS para Python, que permite que os desenvolvedores criem aplicativos que interajam com serviços da AWS com facilidade.

# 5) Criei Lambda Function:
- Para inserção dos objetos coletados/gerados - arquivo zip (contendo o arquivo que usamos como fonte, da fonte, o original), o arquivo gerado (no formato desejado pelo usuário) e o arquivo log (para sinalizar possíveis erros) - no 'armazém', que é o S3, fiz uso da Função Lambda.

# 6) 

# 7) 

---------------------------------------------------------------------------------------------
# OBSERVAÇÕES:
- Conforme mencionado, há arquivos ausentes nesse repositório - exemplo do data.json, justamente para manter integridade dos dados pessoais. Dessa forma, para obtenção do resultado esperado, criei um arquivo base (de nome data_exemplo.json, dentro da pasta utils), para vocês terem uma noção da estrutura que foi necessária para obtenção do resultado esperado.

- Passos 2 e 3 foram realizadas usando, prioritariamente, Linguagem de Programação Python e suas principais bibliotecas, sendo algumas delas: pandas, requests, bs4.

- Passo 4 foi realizado manualmente, via console AWS, entretanto, é possível utilizar o boto3 para criação do Bucket via código, informando dados pertinentes ao Usuário e permissões para criação devida.

- Para facilitação e compreensão, diluí o projeto em etapas, entretanto, não, necessariamente, estão organizadas de maneira sequencial, mas que contribuíram para obtenção do resultado esperado.

------------------------------------------------------------------------------------------------
# REFERÊNCIAS:
- Sites que podem contribuir à realização das etapas relacionadas à nuvem, e que me ajudaram:

- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/creating-bucket.html
- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/uploading-an-object-bucket.html
- https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/deleting-object-bucket.html
- https://docs.aws.amazon.com/pt_br/cost-management/latest/userguide/create-budget-report.html
- https://docs.aws.amazon.com/pt_br/sdk-for-javascript/v2/developer-guide/using-lambda-functions.html

------------------------------------------------------------------------------------------------
Obrigado pela interação, fico à disposição e disponível para dicas, bons estudos e fica na paz!