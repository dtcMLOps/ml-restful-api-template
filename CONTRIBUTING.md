# __How to contribute__

## __Dependencies__

We are using conda to manage dependencies. You can create a new conda env using `conda create --name fastapi_boilerplate python=3.8 -y`. Use `conda activate fastapi_boilerplate` to activate the newly create env. Run `pip install -r requirements-dev.txt --use-deprecated=legacy-resolver` in local. To install less number of dependencies run, `pip install -r requirements.txt --use-deprecated=legacy-resolver`. Once this is done, next step is to install `pre-commit hooks`. Run `pre-commit install` to install pre-commit hook. Add a new file and validate the `pre-commit` hook is working. In case, someone wants to bypass `pre-commit checks` they can use `--no-verify` flag from CLI.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

To deactivate conda env run, `conda deactivate`.

To use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).

## __Codestyle__

After installation you may execute code formatting.

```bash
make auto-format
```

### __Checks__

Comand `make lint` & `make lint-check` applies all checks.

### __Before submitting at a high level__

Before submitting your code please do the following steps:

* Add any changes you want
* Add tests for the new changes
* Edit documentation if you have changed something significant
* Run `make auto-format` to format your changes.
* Run `make lint` to ensure that types, security and docstrings are okay.

## __Detailed contribution guide__

* Lets assume we have a user story like this, `User story - As a user, I want to be able to see the sum of more than two numbers - 145`
* Create a feature branch with proper naming convention: `feat/addition-api-AB#145`, here `145` is the Azure Board ticket number.
* Create a function which takes a list as input and returns sum of its element as output.
* Add static typing to the function. we will use `mypy` to check static typing.
* Add docstring string to the function. We will use google formatting for docstring. Use `autodocstring` extension in VS code for this.

```python
# app/core/addition.py

from typing import List

def addition(input_list: List[float]) -> float:
    """A function to calculate sum of a list of floating point numbers.
    Args:
        input_list (List[float]): List of numbers supplied by the user.
    Returns:
        float: Result of the addition of all the numbers in the list.
    """
    return sum(input_list)
```


* Write test case of the service using pytest. If the test is passing we will proceed forward. We will use pytest to execute test cases.

```python
# tests/test_addition_scv.py

from app.core.addition import addition

def test_addition_scv():
    assert addition([2.5, 3.5]) == 6.0
```


* Write input and output schema for the endpoint as request and response model. Provide example, description in the schema. We are using pydentic for this.

```python
# app/schemas/addition_schema.py

from typing import List

from pydantic import BaseModel, Field

class AdditionInput(BaseModel):
    input_list: List[float] = Field(
        default=None, description="List of float numbers to be added.", example=[1.4, 2.3, 3.2]
    )

class AdditionResults(BaseModel):
    results: float = Field(description="result after addition.", example=6.9)
```

* Define endpoint, add tags, add model description, add endpoint description. This should reflect in Fast API Swagger UI documentation.

```python
# app/settings.py

description = """
Addition API helps you do awesome stuff. 🚀

## Addition

You can **add** all the elements from a list.


* **ping pong** (_implemented_).
* **addition** (_implemented_).
"""

tags_metadata = [
    {
        "name": "health check",
        "description": "Check API service is up and running or not.",
    },
    {
        "name": "addition",
        "description": "Take all the elements present in a list and return the sum of all the elements.",
    },
]


```

* Validate over all API description is present or not.


```python
# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.addition import addition
from app.core.config import settings
from app.schemas.addition_schema import AdditionInput, AdditionResults
from app.settings import description, tags_metadata

def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Addition API developer",
            "url": "https://ab-inbev.com/contact/",
            "email": "xyz@ab-inbev.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        openapi_tags=tags_metadata,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

@app.get("/ping", tags=["health check"])
def pong():
    return {"ping": "pong!"}

@app.post(
    "/addition/",
    description="Addition of all the numbers in a list.",
    response_model=AdditionResults,
    tags=["addition"],
)
async def update_item(input_list: AdditionInput):
    results = addition(input_list.input_list)
    return {"results": results}

```
* Write unit test for the endpoint.

```python
# tests/test_addition.py
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_addition():
    response = client.post(
        "/addition/",
        json={"input_list": [1.4, 2.3, 3.2]},
    )
    assert response.status_code == 200
    assert response.json() == {"results": 6.9}
```

* Add any new dependency required in `requirements*.txt` files
* Validate all the tests are passing including standalone functions and the developed endpoints. `make test`
* Run formatting on the code base. `make auto-format`
* Run linting on the code base.  `make lint`
* Run lint checks. Make sure all the checks are being passed. `make lint-check`
* Check docker compose is working or not: build, run, test, kill. `make build && make run && make kill`
* Update docs in wiki. validate docstring are getting parsed correctly. Addition function description and context. `mkdocs build && mkdocs serve`
* Push code to the feature branch with conventional commit. `git add . && cz -n cz_commitizen_emoji c && git push origin feat/addition-api-AB#145`
* Create a draft pull request unless the feature is over. give an appropriate title to the PR such as `feat: developing addition POST endpoint in addition service.`
* Keep pushing changes following the above step until the feature is compleat.
* Once the feature is compleat add a label, add reviewers and submit pull request for merge.
* Make sure when you are submitting the pull request there is not merge conflict. If there is a merge conflict resolve before raising a pull request.
* Once the CI pipeline gets executed, check all the checks are being passed or not.
* If there is any KPI generated from Sonar Cloud or any other tool is failing fix that.
* Once all the checks in CI pipelines are being passed, __squash and merge__ the code to the `develop` or working branch.
* Once this is merge to develop, move ticket in azure devops board to `dev compleat`.


### __Tools & technologies__

* We are following [conventional commit](https://www.conventionalcommits.org/). Commit msg and pr title follow conventional commit structure.
* We are following [semantic versioning](https://semver.org/).
* We are following [giflow](https://danielkummer.github.io/git-flow-cheatsheet/) as branching model.
* `develop` is the working branch. `develop`, `staging` and `master` are no commit branches.
* To manage release note we are using [release drafter](https://github.com/release-drafter/release-drafter).
* To generate Change Logs we are using `saadmk11/changelog-ci@v1.0.0` github actions.
* To ensure code quality we are using [`pre-commit hooks`](https://pre-commit.com/).
* For linting we are using [`flake8`](https://pypi.org/project/flake8/) and [`pylint`](https://pylint.pycqa.org/en/latest/).
* For formatting we are using [`black`](https://github.com/psf/black), [`autopep8`](https://pypi.org/project/autopep8/), [`autoflake`](https://pypi.org/project/autoflake/) and [`isort`](https://pycqa.github.io/isort/).
* For wiki we are using [`mkdocs`](https://www.mkdocs.org/). To render docstring we are using [`mkdocstring`](https://github.com/mkdocstrings/mkdocstrings). Also we are using [`autosocstring`](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension in VS Code with [`google`](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format.
* For writing test cases we are using [`pytest`](https://docs.pytest.org/en/7.1.x/).
* To manage virtual env, we are using [`conda`](https://www.anaconda.com/products/distribution) and [`venv`](https://docs.python.org/3/tutorial/venv.html).
* For containerization we are using [`docker`](https://www.docker.com/).
* As IDE we are using [`VS Code`](https://code.visualstudio.com/). As OS, [`Ubuntu`](https://ubuntu.com/) is a preferred choice.
* For static code analysis we are using [`Sonar Cloud`](https://sonarcloud.io/).
* For code scanning we are using [`CodeQL`](https://codeql.github.com/), [`gitleaks`](https://github.com/zricethezav/gitleaks), [`Checkmarx`](https://checkmarx.com/) and [`bandit`](https://bandit.readthedocs.io/en/latest/).
* For container scanning we are using [`Snyk`](https://snyk.io/).
* As SCM we are using [`GitHub`](https://github.com/). For CI/CD pipelines we are using [`GitHub actions`](https://github.com/features/actions).
* For project management we are using [`Azure DevOps`](https://azure.microsoft.com/en-us/services/devops/) and [`Azure Boards`](https://azure.microsoft.com/en-us/services/devops/boards/).
* As public cloud we are using [`Azure`](https://azure.microsoft.com/en-in/).
* For static typing we are using [`mypy`](https://mypy.readthedocs.io/en/stable/).
* For diagrams we are using [`lucid charts`](https://www.lucidchart.com/pages/) & [`diagrams`](https://www.diagrams.net/).
* For artifact store we are using [`jfrog`](https://jfrog.com/).
* To serve code related documentation we are using [`github pages`](https://pages.github.com/). Other project related docs are present in [`Azure Wiki`](https://docs.microsoft.com/en-us/azure/devops/project/wiki/wiki-create-repo?view=azure-devops&tabs=browser).
* To build RESTful APIs we are using [`FastAPI`](https://fastapi.tiangolo.com/). We are using [`MySQL`](https://www.mysql.com/) as database. We are using [`SQLalchemy`](https://www.sqlalchemy.org/) as ORM.
* We are using [`Alembic`](https://alembic.sqlalchemy.org/en/latest/) for database migration.
* For REST API documentation we are using [`Swagger UI`](https://swagger.io/tools/swagger-ui/).


### __Application security__

At a high level, an application security review includes the following stages:

* Architecture design review
* Threat modeling (abuse case development)
* In-depth code review
* Dynamic testing

To initiate the process, we need your help to:

* Provide AppSec Team Members with access to the source code and ticket/issue/work item management system
* Share architecture diagrams and documentation of the various system components and microservices
* Share credentials to the non-prod environment for at least two different user roles
* Swagger/OpenAPI/Postman Collections*
* Provide AppSec Team Members with read-only access to the product's cloud account/resource group
* Assign your DevOps engineer to [Follow guidelines](https://anheuserbuschinbev.sharepoint.com/teams/ApplicationSecurity/SitePages/CI-CD-Integration-for-Secure-Coding-Tools.aspx?CT=1653272387751&OR=OWA-NT&CID=213e784c-ee2a-d8e2-5015-8c24114434f4) and configure the CI/CD pipelines to include AppSec scanning suite: [Checkmarx](https://anheuserbuschinbev.sharepoint.com/teams/ApplicationSecurity/SitePages/Getting-access-to-Checkmarx.aspx), [Snyk](https://anheuserbuschinbev.sharepoint.com/teams/ApplicationSecurity/SitePages/Developer-Access-to-Snyk.aspx), and GitLeaks. Onboard product developers to Checkmarx  and Snyk.
  * __Snyk Org:__ Analytics
  * __Checkmarx Team:__ CxServer\AB-InBev\GHQ\Analytics\MediaMixModelling
* Reach out to [SOC-BrandProtection](SOC-BrandProtection@ab-inbev.com) to set up Imperva WAF, Qualys WAS, and IntSights monitoring
* Work with the zone's cybersecurity team to register the application in the [App360](https://beerforce.my.salesforce.com/)  inventory and update the risk profile


To make the in-depth code review more efficient, we leverage several tools aimed at identifying software security gaps, each is focused on different parts of an application/product/system and implemented at different stages of the product’s CI/CD pipelines:

* __Checkmarx__ – Source Code Scanning (SAST) – identify vulnerabilities in code that the developers write on their own, the application business logic
* __Snyk:__
  * __Dependency Scanning (SCA)__ : Identify vulnerabilities in open source components or third-party dependencies that the developers bring to the product, which was written by someone else.
  * __Container image scanning__ : Identify vulnerabilities in container images which is the platform that is running the developer’s compiled code
  * __Kubernetes deployment scanning__ : Enforcing least privilege principle at the container level that is running the code, trying to minimize the impact of one compromised container on the entire host and product system
* __Checkov__ : Infrastructure as Code scanning – focused on Terraform security best practices that make up the product system ecosystem
* __Gitleaks__ : Secrets scanning, passwords, and API keys that developers accidentally commit to the code
* __Imperva Incapsula (Web Application Firewall)__ : Imperva’s Incapsula is a 100 cloud-based solution for protecting websites and applications from external threats including OWASP top 10 threats, hacking attempts, malicious bots, scraping, and DDoS attacks
* __IntSights (External Threat Protection)__ : Brand Protection OpsCenter (BPOC) leverages IntSights for the Digital Fraud Footprint capability. The IntSights Enterprise Threat Intelligence Mitigation Platform delivers proactive defense by transforming threat intelligence into automated security action. It monitors ABinBev’s external threat profile, aggregates and analyses tens of thousands of threats, and automates the risk mitigation lifecycle.
* __Qualys WAS (Web Vulnerability Management)__ : Qualys Web Application Scanning (WAS) is a cloud-based service that provides automated crawling and testing of custom web applications to identify vulnerabilities including cross-site scripting (XSS) and SQL injection. The automated service enables regular testing that produces consistent results, reduces false positives, and easily scales to cover thousands of websites.
* __Apiiro*__
* __Bright Security(prev. NeuraLegion)*__
