<h1>API para criar cetificados digitais</h1>

<h3>Aluno: Júlio Santiago</h3>

* **Descrição**

  * Sistema que cria certificados digitais. Autenticação com OAuth.

    

* **Bibliotecas utilizadas**

  * <a>django</a>: framework python na web

  * <a>cryptography</a>: para criação de certificados digitais

  * <a>all-auth</a>: para autenticação **OAuth** via conta Google

    

* **Requisitos**

  * Python 3.x.x

    

* **Tutorial instalação**

  * Instale as dependências necessárias para executar:
    * <code>pip freeze install -r requirements.txt</code>
  * Em seguida suba inicialize o banco de dados para a CRL:
    * <code>python manage.py migrate</code>

  * Execute o servidor:
    * <code>python manage.py runserver</code>



