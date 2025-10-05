# Projeto de Gestão para Cidades Inteligentes

Este é um sistema web desenvolvido em Flask para gerenciar ocorrências, sensores e câmeras em uma cidade inteligente.

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
* [Git](https://git-scm.com/)
* [Python 3.10+](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/) (um banco de dados relacional)

## 🚀 Guia de Instalação e Execução

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### 1. Clone o Repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

### 2. Crie e Ative o Ambiente Virtual (Virtual Environment)

É uma boa prática isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Linux/macOS
source venv/bin/activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados PostgreSQL

Você precisa criar um banco de dados e os tipos `ENUM` customizados que a aplicação utiliza.

a. Abra o terminal do `psql` ou sua ferramenta de banco de dados preferida.

b. Crie um banco de dados para o projeto (ex: `smartcity_db`).
```sql
CREATE DATABASE smartcity_db;
```

c. Conecte-se ao banco recém-criado e execute os comandos abaixo para criar os tipos `ENUM`:
```sql
-- Conecte-se com: \c smartcity_db

CREATE TYPE public.criticidade_ocorrencia AS ENUM
    ('baixo', 'médio', 'alto');

CREATE TYPE public.status_ocorrencia AS ENUM
    ('aberta', 'em_atendimento', 'resolvida', 'cancelada');
```

### 5. Configure a Conexão com o Banco de Dados

A aplicação precisa saber como se conectar ao banco de dados através de um arquivo de configuração.

a. Faça uma cópia do arquivo `config.py.example` e renomeie-a para `config.py`:
```bash
# No Windows (usando copy)
copy config.py.example config.py

# No Linux/macOS (usando cp)
cp config.py.example config.py
```

b. Abra o arquivo `config.py` e edite a variável `SQLALCHEMY_DATABASE_URI` com suas credenciais do PostgreSQL. Por exemplo:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:minha_senha_123@localhost:5432/smartcity_db"
```

### 6. Crie as Tabelas no Banco

Para criar todas as tabelas no banco de dados a partir dos modelos SQLAlchemy, execute o seguinte comando:

```bash
python create_tables.py
```
*(Este passo assume que existe um script `create_tables.py` no projeto para inicializar o banco).*


### 7. Execute a Aplicação!

Finalmente, inicie o servidor de desenvolvimento do Flask:
```bash
python app.py
```
Acesse a aplicação no seu navegador em: **http://12.0.0.1:5000**
