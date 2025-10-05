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

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias com um único comando:
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

### 5. Configure as Variáveis de Ambiente

A aplicação precisa saber como se conectar ao banco de dados.

a. Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
```bash
# No Windows (usando copy)
copy .env.example .env

# No Linux/macOS (usando cp)
cp .env.example .env
```

b. Abra o arquivo `.env` e edite as variáveis com as suas credenciais do PostgreSQL. Por exemplo:
```
DATABASE_URL="postgresql://postgres:minha_senha_123@localhost:5432/smartcity_db"
SECRET_KEY="qualquer-string-aleatoria-e-segura"
```

### 6. Crie as Tabelas no Banco

Para criar todas as tabelas no banco de dados a partir dos modelos definidos no `app.py`, execute o script de criação.

*(Observação: Se você não tiver um script separado, pode ser necessário adicionar uma função temporária ao seu app ou criá-lo via terminal Python).*

Uma forma simples de criar um script para isso (ex: `create_tables.py`):
```python
# create_tables.py
from app import app, db

with app.app_context():
    print("Criando tabelas...")
    db.create_all()
    print("Tabelas criadas com sucesso!")

```
Execute o script:
```bash
python create_tables.py
```

### 7. Execute a Aplicação!

Finalmente, inicie o servidor de desenvolvimento do Flask:
```bash
python app.py
```
Acesse a aplicação no seu navegador em: **http://127.0.0.1:5000**

Pronto! Agora qualquer pessoa que clonar seu repositório terá um guia completo para rodar o projeto.
