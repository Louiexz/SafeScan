# Soft.ai

Website Soft.ai, voltado para verificação de malware por meio da utilização de IA.<br>
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

    https://soft.ai.vercel.app/

2. Ou clone o repositorio:

        git clone https://github.com/Louiexz/Soft.ai.git

        cd Soft.ai

3. Instale as dependências:

        cd frontend
        npm install

5. No Frontend:

        - Execute a aplicação:

                npm run dev
        
        - Crie um arquivo .env e declare as seguintes secrets :

                NODE_ENV = production ou outro
        
        - Acesse:

                http://localhost:5173/


## Estrutura do projeto

        frontend/
        |
        └── project-safescan/
            ├──
            └── src/
                ├── assets/        # Diretório de imagens e arquivos css
                ├── components/    # Diretório de componentes comuns das páginas
                ├── pages/         # Diretório de componentes das páginas
                ├── services/      # Diretório de serviços usadas nas páginas
                ├── App.css        # Estilos da rota
                ├── App.jsx        # Componente de rotas do projeto
                ├── index.css      # Estilos da aplicação
                └── main.jsx       # Chamada da aplicação


          
## Autores e contribuições:
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

Luiz Augusto - [@Louiexz](https://github.com/Louiexz)<br>
Vinicius José - [@ViniciusRKX](https://github.com/ViniciusRKX)
