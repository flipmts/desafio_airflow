# Configuração do Ambiente Airflow

Este projeto requer a configuração do Apache Airflow para a execução de tarefas agendadas. Certifique-se de seguir as etapas abaixo para configurar o ambiente do Airflow.

## Instalação do Apache Airflow

Antes de começar, certifique-se de ter o Apache Airflow instalado no seu ambiente. Você pode instalá-lo usando o comando:

```pip install apache-airflow```

# Instalando os Requisitos

Depois de instalar o Apache Airflow, você precisará instalar as dependências especificadas no arquivo requirements.txt. Para fazer isso, execute o seguinte comando no diretório raiz do projeto:

```pip install -r requirements.txt```

# Banco de Dados SQLite

Este projeto utiliza um banco de dados SQLite para armazenar os dados. Certifique-se de que o arquivo do banco de dados data/Northwind_small.sqlite esteja disponível.

DAG utilizada
A DAG example_desafio.py consiste em três tasks:

- export_order_csv: Lê os dados da tabela 'Order' do banco de dados e escreve um arquivo chamado "output_orders.csv".

- export_count_csv: Lê os dados da tabela "OrderDetail" do mesmo banco de dados e faz um JOIN com o arquivo "output_orders.csv" gerado pela Task 1. Essa task calcula a soma da quantidade vendida (Quantity) com destino (ShipCity) para o Rio de Janeiro. O resultado é exportado em um arquivo "count.txt" que contém apenas o valor em formato texto.

- export_final_output: Exporta a mensagem final, composta pelo endereço de e-mail (my_email) e o valor da contagem (count), codificada em Base64, para um arquivo "final_output.txt".

- Variável do E-mail no Apache Airflow: É necessário configurar a variável my_email no ambiente do Apache Airflow. Você pode fazer isso no painel de administração do Airflow.

Após seguir essas etapas e configurar o ambiente, você estará pronto para executar a DAG com as duas tarefas especificadas no desafio. Certifique-se de que o Apache Airflow esteja em execução e agendado para executar a DAG.