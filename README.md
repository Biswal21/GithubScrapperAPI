
# Githhub Scrapper API

This is an assignment to implement a user dat scrapping server from Github API.




## Tasks Completed

* Buillt a REST API using Django REST Framework.
* Swagger implemented for API documentation
* Containerized application and database using Docker.
* API Endpoints for fetching Github users from Github API,fetching Github user profiles saved in DB.
* Rest of working in WORKING.md


## Built With

[Django Rest framwork](https://www.django-rest-framework.org/)


[Postgres](https://www.postgresql.org/docs/)


## Prerequisites


[Docker](https://docs.docker.com/get-docker/)

[docker-compose](https://docs.docker.com/compose/install/)
## Installation

1. Clone the repository and change the directory

```bash
  git clone https://github.com/Biswal21/GithubScarpperAPI.git
  cd GithubScarpperAPI
```
2. Build the server

```bash
  docker-compose -f docker-compose.dev.yml Build
```
3. Up the server
```bash
  docker-compose -f docker-compose.dev.yml up
```
4. Visit Django admin panel
  Visit django-admin at `localhost:8000/admin/` for admin panel

5. Visit Swagger API documentation and endpoint testing 
  Visit swagger at `localhost:8000/swagger/` 