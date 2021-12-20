# Ministério Público do Mato Grosso (MPMT)
Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Mato Grosso. O site com as informações pode ser acessado [aqui](https://mpmt.mp.br/transparencia/contracheque.php).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixadas duas planilhas no formato ODS, cada planilha é referente a uma destas categorias: 

- Tipo I - Folha de remunerações: Membros Ativos. 
- Tipo II - Verbas Indenizatórias e outras remunerações temporárias.

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

    ```sh
    $ cd coletor-mpmt
    $ sudo docker build -t mpmt .
    ```

- Execução:

    ```sh
    $ sudo docker run -e YEAR=2020 -e MONTH=1 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpmt
    ```

### Executando sem uso do docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório coletor-mpgo, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado.
 
    ```sh
        YEAR=2020 MONTH=01 GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
    ```sh
        pip install -r requirements.txt
    ```

## Dicionário de Dados

As planilhas possuem as seguintes colunas:

- **Matrícula (String)**: Matrícula do funcionário  
- **Nome (String)**: Nome completo do funcionário
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Férias - ⅓ Constitucional (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago ao servidor por ocasião das férias
- **Abono de Permanência (Number)**:  Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social)
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração básica bruta, quando esta ultrapassa o teto constitucional, nos termos da legislação correspondente

## Dificuldades para libertação dos dados

- Não há API para acesso aos dados
