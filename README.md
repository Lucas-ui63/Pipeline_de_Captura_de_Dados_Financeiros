# Pipeline de Captura de Dados Financeiros (YFinance + Supabase)

Este é um módulo independente de Engenharia de Dados desenvolvido em Python. Ele faz a extração automatizada de dados históricos de ações da API do Yahoo Finance e realiza a carga diretamente em um banco de dados PostgreSQL hospedado no Supabase.

O projeto foi construído do zero focando em boas práticas de arquitetura de software, visando compor o back-end de um ecossistema futuro de saúde financeira.

## Tecnologias Utilizadas
* **Python 3** - Linguagem base
* **Pandas** - Conversão de dados
* **YFinance** - API de dados do mercado financeiro
* **Psycopg2** - Driver de conexão com o banco de dados
* **Supabase / PostgreSQL** - Banco de dados na nuvem

## Diferenciais de Arquitetura Aplicados

Para garantir que o código seja fácil de manter, escalável e seguro, apliquei conceitos de boas práticas de programação:

* **Separação de Responsabilidades:** A classe `Banco` cuida da infraestrutura de conexão, enquanto a classe `Data` foca exclusivamente nas regras de negócio e captura da API.
* **Injeção de Dependência:** A classe `Data` recebe o objeto de conexão do banco já configurado. Caso eu precisar trocar o banco de dados no futuro, não preciso reescrever a lógica da API.
* **Gerenciamento de Contexto (with):** Utilização do bloco `with` para garantir abertura e fechamento automáticos de conexões e cursores, evitando vazamentos de memória e travamentos no banco.
* **Estratégia ELT:** Os dados são extraídos e salvos no formato bruto (`JSONB`) no banco de dados. Isso preserva o histórico fiel da API para que as limpezas e filtros (camadas Silver/Gold) sejam feitos posteriormente sem novas requisições web.
* **Prevenção de Falhas (Operador Walrus):** Implementação de checagem em tempo de execução para garantir que o banco só tente salvar dados se a API responder com sucesso.

## Como Rodar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/Lucas-ui63/Pipeline_de_Captura_de_Dados_Financeiros
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure seu arquivo `.env` na raiz com as credenciais do Supabase (ou do seu banco):
```env
SUPABASE_URL=seu_link
SUPABASE_KEY=sua_chave
SUPABASE_HOST=seu_host
SUPABASE_PORT=sua_porta
```

4. Execute o script principal:
```bash
python main.py
```
