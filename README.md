
# Code Challenge Juntos Somos+

## Instruções

Este repositório contém os arquivos necessários para executar o projeto utilizando o Docker. Antes de mais nada, será necessário instalar alguns pré-requisitos, se ainda não estiverem instalados:

- Instale o [Docker](https://docs.docker.com/get-docker/)

Faça a cópia deste repositório em um diretório qualquer

```
$ git clone git@github.com:wamauri/code-challenge-jsm.git 
$ cd code-challenge-jsm
```

Utilize o Docker para carregar e depois disponibilizar todos os serviços necessários ao funcionamento do projeto:
```
$ docker-compose up
```
Para que as migrations sejam aplicadas é necessário parar o servidor com um `Ctrl+c` e executar o comando `$ docker-compose up` novamente.

## Tests
Todos os tests foram realizado utilizando a lib Coverage.py 
- Biblioteca [Coverage.py](https://coverage.readthedocs.io/en/6.4.1/)

### Screenshots dos tests 
Foram desenvolvidos 36 tests unitários para garantir o funcionamento correto do sistema.

![tests](https://user-images.githubusercontent.com/67606510/177577981-9b10974c-5c49-4eef-8c1e-18b900dcdd04.png)

![tests_web](https://user-images.githubusercontent.com/67606510/177577982-754acfd8-cd8c-48a2-b8b3-6de4c769f09a.png)

## Telas
### Home
Foi desenvolvido uma tela para carregamento tantos de links como arquivos json ou csv. Essa tela também possui validação para que apenas links e arquivos json ou csv sejam carregados.

![home](https://user-images.githubusercontent.com/67606510/177577979-14908239-729a-4d77-980b-0933b641029c.png)

### Painel de controle
Foi utilizado o painel de administração do Django para acessar os objetos criados, não é necessário para o funcionamento do sistema. Foi apenas para acompanhar a criação dos objetos. 

![django_admin](https://user-images.githubusercontent.com/67606510/177577960-82435896-a2e4-47d6-b4a7-2d38d963addf.png)

Para acessar esse painel é preciso criar um *superuser* com o seguinte comando em um novo terminal com o sistema rodando:

```
$ docker exec -it container_id python manage.py createsuperuser
```

Para saber o *container_id* basta executar o seguinte comando:
```
$ docker container ps
```
![container_id](https://user-images.githubusercontent.com/67606510/177587015-8fb2ccf7-6907-42c0-9aa8-ca37127dc0f2.png)

### Django Rest Framework
A tela do DRF também pode ser utilizada para fazer as consultas se o usuário não possuir um API Client.

![drf](https://user-images.githubusercontent.com/67606510/177577965-2f2974bf-0bd2-4d57-be38-5c02f20df041.png)

## Endpoints
Busca todos os cliente no banco de dados.
```
http://localhost:8000/api/v1/customers/
```
![endpoint_customers](https://user-images.githubusercontent.com/67606510/177577970-95ce2767-2fa6-4730-bdae-b788022354f7.png)

Busca todos os registros no banco de dados, filtrando todos os clientes por região do Brasil e por tipo de cliente (no screenshot está sendo feita uma busca por todos os clientes da região norte e que sejam do tipo special).

Regiões para consulta:
- norte
- nordeste
- centro-oeste
- sudeste
- sul

```
http://localhost:8000/api/v1/customers/norte/special/
```
![endpoint_customer_region_and_type](https://user-images.githubusercontent.com/67606510/177577967-6c426e21-01e8-4c9e-852a-74bd48e6c305.png)

Busca todos os clientes da região norte do Brasil
```
http://localhost:8000/api/v1/customers/norte/
```
![endpoint_region](https://user-images.githubusercontent.com/67606510/177577975-227a762e-0aeb-4d40-9e53-400e0af5f8b0.png)

Busca todos os clientes do tipo special
```
http://localhost:8000/api/v1/customers/special/
```
![endpoint_customer_type](https://user-images.githubusercontent.com/67606510/177577973-a2484def-6a3e-4ad2-ae6b-16b72e5beb87.png)
