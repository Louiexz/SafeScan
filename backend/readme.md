# SafeScan

RestFul API/Backend/Server para o website SafeScan, voltado para verificação de malware por meio da utilização de IA.<br>
Projeto criado para a 2º unidade da cadeira de Desenvolvimento Backend na UNIT - PE, 4º período, curso Análise e Desenvolvimento de Sistemas.

# Pré-requisitos
## Certifique-se de ter o seguinte instalado antes de começar:
    Python3

## Funcionalidades

        Autenticação: Permite que o usuário crie uma nova conta e faça login em nosso website.
        Profile: Página dedicada ao usuário, onde pode visualizar com mais precisão seus softwares e alterar informações pessoais, quando estiver logado.
        Software: Permite a visualização de todos os softwares cadastrados, além do cadastramento ou checagem por url e arquivo. Disponibiliza a atualização e exclusão do seu software, quando estiver logado.

# Instalação e Uso

1. Acesse:

    https://safescan.vercel.app/

2. Ou clone o repositorio:

        git clone https://github.com/Louiexz/SafeScan.git

        cd SafeScan

3. Instale as dependências:

        python -m venv .venv

        python install -r requirements.txt

        cd backend


4. Crie um arquivo .env e declare as seguintes secrets:

        SECRET_KEY
        DEBUG
        ALLOWED_HOSTS
        EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD
        DEFAULT_FROM_EMAIL
        API_KEY

4. Realize a migração:

        python manage.py migrate
        
5. Efetue os testes:

        pytest

6. Execute a aplicação e Acesse:

        python manage.py runserver

        http://127.0.0.1:8000/


## Estrutura do projeto

        backend/
        │
        ├── backend/          # Diretório do projeto
        │   ├── settings.py     # Configurações do projeto
        │   ├── urls.py         # Mapeamento de URLs
        │   ├── asgi.py         # Configuração para ASGI
        │   └── wsgi.py         # Configuração para WSGI
        │
        ├── safescan/         # Aplicativo Django
        │   ├── migrations/     # Arquivos de migração de banco de dados
        │   ├── model/          # Diretório dos modelos de db
        │   ├── serializer/     # Diretório dos modelos de serializers dos modelos de db
        │   ├── test/           # Diretório de testes das views
        │   ├── view/           # Diretório das lógicas de visualizações
        │   ├── admin.py        # Configurações do admin
        │   ├── apps.py         # Configurações do aplicativo
        │   └── urls.py         # URLs específicas do aplicativo
        │
        ├── pytest.ini        # Script de testes
        |
        ├── manage.py         # Script de gerenciamento do projeto
        │
        ├── requirements.txt  # Dependências do projeto
        │
        └── db.sqlite3        # Banco de dados SQLite (Criado com o migrate)

## Autores e contribuições:
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

Luiz Augusto - [@Louiexz](https://github.com/Louiexz)<br>
Vinicius José - [@ViniciusRKX](https://github.com/ViniciusRKX)
