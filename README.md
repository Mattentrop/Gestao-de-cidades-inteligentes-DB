# Projeto de Gestão para Cidades Inteligentes

Este é um sistema web desenvolvido em Flask para gerenciar ocorrências, sensores e câmeras em uma cidade inteligente.

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
* [Git](https://git-scm.com/)
* [Python 3.10+](https://www.python.org/)

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

### 4. Configure a Conexão com o Banco de Dados

Este projeto utiliza um banco de dados PostgreSQL centralizado que está hospedado em um VPS. **Você não precisa criar o banco de dados, os tipos ou as tabelas**, apenas configurar a conexão.

**a. Solicite as Credenciais de Acesso**

Peça ao administrador do projeto (Matheus) as informações de conexão com o banco de dados:
* Host (Endereço IP do VPS)
* Porta (normalmente 5432)
* Nome do Banco de Dados
* Usuário
* Senha

**b. Crie o Arquivo de Configuração Local**

Faça uma cópia do arquivo `config.py.example` e renomeie-a para `config.py`:
```bash
# No Windows (usando copy)
copy config.py.example config.py

# No Linux/macOS (usando cp)
cp config.py.example config.py
```

**c. Preencha o Arquivo de Configuração**

Abra o arquivo `config.py` e edite a variável `SQLALCHEMY_DATABASE_URI` com as credenciais que você recebeu.

O formato é: `"postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO"`

**Exemplo:**
```python
SQLALCHEMY_DATABASE_URI = "postgresql://dev_user:senha_secreta_123@192.168.1.100:5432/smartcity_db_dev"
```

### 5. Execute a Aplicação!

Com a configuração pronta, inicie o servidor de desenvolvimento do Flask:
```bash
python app.py
```
A aplicação irá se conectar ao banco de dados no VPS. Acesse-a no seu navegador em: **http://127.0.0.1:5000**
