# SafeScan

Website SafeScan, voltado para verificação de malware por meio da utilização de IA.<br>
Projeto criado para a 2º unidade da cadeira de Desenvolvimento Backend na UNIT - PE, 4º período, curso Análise e Desenvolvimento de Sistemas.

# Pré-requisitos
## Certifique-se de ter o seguinte instalado antes de começar:

    Python3
    npm

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

        cd backend

        python -m venv .venv

        python install -r requirements.txt

4. Para o backend:
        - Crie um arquivo .env e declare as seguintes secrets :

                SECRET_KEY (Key do django, use alguma gerada por ele)
                DEBUG (Seta respostas detalhadas de erro ou não)
                ALLOWED_HOSTS (Sites que irão poder se comunicar)
                EMAIL_HOST_USER (Email para enviar recuperação de senha ao usuário)
                EMAIL_HOST_PASSWORD (Sua senha para enviar recuperação de senha ao usuário)
                DEFAULT_FROM_EMAIL (Email para enviar recuperação de senha ao usuário)
                API_KEY (Api key da API VirusTotal)
                CORS_ALLOWED_ORIGINS (Permissão para sites externos utilizarem métodos HTTP)
        
        - Use as seguintes variaveis em caso de banco externo:
        
                DB_NAME 
                DB_USER
                DB_PASSWORD
                DB_HOST
                DB_PORT
        
        - Ou implemente o banco local:
                DATABASES = {
                        'default': {
                                'ENGINE': 'django.db.backends.sqlite3',
                                'NAME': BASE_DIR / 'db.sqlite3',
                        }
                }        

        - Realize a migração:

                python manage.py migrate
        
        - Efetue os testes:

                pytest

        - Execute a aplicação e Acesse:
        
                gunicorn backend.wsgi

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
        ├── pytest.ini        # Script de testes backend
        |
        ├── manage.py         # Script de gerenciamento do projeto
        │
        ├── requirements.txt  # Dependências do projeto
        │
        └── db.sqlite3        # Banco de dados SQLite (Mude em settings para criar com o migrate)
          
## Autores e contribuições:
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

Artur Ramos - [@Arturdev05](https://github.com/Arturdev05)<br>
Carlos Eduardo - [@carlos-1ima](https://github.com/carlos-1ima)<br>
Luiz Augusto - [@Louiexz](https://github.com/Louiexz)<br>
Paulo Arthur -<br>
Vinicius José - [@ViniciusRKX](https://github.com/ViniciusRKX)
