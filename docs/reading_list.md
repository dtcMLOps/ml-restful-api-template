### __Reading List__

To build a ML Engine we are going to use [FastAPI](). [Here]() is an introduction about the framework. There are other frameworks out there. [Here]() is a comparison between all the other existing frameworks out there. [SQLModel]() which we are going to using as ORM. [Here]() is some details about the ORM. [Alembic]() we using for database migration. [Here]() is some documentation regarding Alembic. FastAPI comes with [Swagger UI](). We are going to user Swagger UI for API documentation.

For project level documentation we are using [MKDocs](). [Here]() is a overview of the framework. Also, we are using [MKdocstrings]() to render docstring along with the API documentations.

We are using docker for containerization. Here is an overview about docker. Also along with docker we will use docker-compose to run things in local. We are using Kubernetes in production to serve the application. To store the docker images we are going to use azure container register.

Regarding SCM, we are using [gitflow] as branching model. We have multiple [git sub-modules]() for different micro-services and micro-frontend components. We will combine all components in a [monorepo](). Whenever there is a push to any of the sub modules, CI pipeline will trigger, run all the checks and if everything goes fine, it will push a docker image to a container registry and will update the code in the monorepo. To host our code we will use [GitHub]().

Regarding virtual env, the preferred env is [conda](). But other than that we can use [venv]() and [poetry]().
