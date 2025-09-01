# Aplicação de Assinatura Digital

## Visão Geral

Esta é uma aplicação web de prova de conceito para demonstrar o processo de assinatura e verificação digital usando criptografia de chave pública (RSA) e hashing (SHA-256). O sistema permite que um usuário se cadastre, gere seu par de chaves, assine um documento e tenha sua assinatura verificada por terceiros, garantindo a autenticidade e a integridade da mensagem.

A aplicação é modularizada e construída com:

- Backend: Django (framework web em Python).

- Frontend: HTML, JavaScript e Tailwind CSS.

- Banco de Dados: SQLite (embutido).

- Criptografia: Biblioteca cryptography para gestão de chaves e algoritmos criptográficos.

## Funcionalidades Principais

- Cadastro de Usuário: Ao se cadastrar, o sistema gera automaticamente um par de chaves (pública e privada) exclusivo para o usuário, que é persistido no banco de dados.

- Área de Assinatura: Permite que o usuário autenticado digite um texto, que será assinado com sua chave privada. O sistema retorna o ID da assinatura para posterior verificação.

- Verificação Pública: Uma rota pública onde qualquer pessoa pode verificar a autenticidade de uma assinatura, fornecendo a assinatura e o texto original. O sistema retorna VÁLIDA ou INVÁLIDA.

- Logs de Verificação: Todas as tentativas de verificação são registradas no banco de dados, incluindo a data e o status.

## Estrutura do Projeto
O projeto segue a arquitetura padrão do Django, com o código dividido em diretórios lógicos para maior organização e escalabilidade.

```bash
assinatura_digital/
├── .gitignore          # Arquivos e diretórios a serem ignorados pelo Git
├── manage.py           # Ferramenta de linha de comando do Django
├── requirements.txt    # Lista de dependências Python
├── mysite/             # Configurações principais do projeto Django
│   ├── settings.py     # Configurações do banco de dados, middlewares, etc.
│   ├── urls.py         # Rotas principais da API
│   └── ...             # Outros arquivos de configuração
└── signatures/         # A aplicação principal de assinatura
    ├── templates/      # Interface do usuário para a aplicação
        ├── private.html # Interface privada de assinatura de mensagem e cadastro
        └── public_verification.html  # Interface pública para verificação de assinatura
    ├── models.py       # Definição das tabelas do banco de dados (Usuários, Chaves, Assinaturas)
    ├── urls.py         # Rotas da API específicas da aplicação
    └── views.py        # Lógica de negócios da API
```

## Configuração e Instalação

Siga os passos abaixo para configurar e rodar a aplicação em sua máquina.

### 1. Clone o Repositório:

```python
git clone [https://github.com/Nathan-Santana/assinatura-digital.git](https://github.com/Nathan-Santana/assinatura-digital.git)
cd assinatura_digital
```
### 2. Crie e Ative um Ambiente Virtual:
```python
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```
### 3. Instale as Dependências:
```python
pip install -r requirements.txt
```

### 4. Execute as Migrações do Banco de Dados:
```python
python manage.py makemigrations signatures
python manage.py migrate
```
## Como Rodar a Aplicação
### 1. Inicie o Servidor Backend:
```python
python manage.py runserver
```
### 2. Acesse a Aplicação:
No navegador, acesse a aplicação através de `127.0.0.1:8000`

## Endpoints da API
* `POST /api/register/`: Cadastra um novo usuário, gera chaves RSA e retorna o `id` do usuário.

* **Corpo da requisição:** `{ "username": "seu_usuario" }`

* `POST /api/sign/`: Assina uma mensagem com a chave privada do usuário.

* **Corpo da requisição:** `{ "username": "seu_usuario", "message": "sua mensagem aqui" }`

* **Resposta:** Retorna o ID da assinatura.

* `POST /api/verify/`: Verifica a autenticidade de uma assinatura.

* **Corpo da requisição:** `{ "username": "seu_usuario", "message": "a mensagem original", "signature": "a_assinatura_em_base64" }`

* **Resposta:** Retorna `VÁLIDA` ou `INVÁLIDA`.

[Se gostou do meu trabalho, entre em contato](https://www.linkedin.com/in/nathan-santana-dev-fs)
