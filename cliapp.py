import typer
import requests

app = typer.Typer()
DOMAIN = 'http://127.0.0.1:8000'


@app.command()
def ping():
    """
        python cliapp.py ping
    """
    x = requests.get(str(DOMAIN) + '/ping')
    typer.echo(x.status_code)
    typer.echo(x._content)

@app.command()
def heartbeat():
    """
        python cliapp.py heartbeat
    """
    x = requests.get(str(DOMAIN) + '/heartbeat')
    typer.echo(x.status_code)
    typer.echo(x._content)

@app.command()
def getteams():
    """
        python cliapp.py getteams
    """
    x = requests.get(str(DOMAIN) + '/teams')
    typer.echo(x.status_code)
    typer.echo(x._content)

@app.command()
def getteam(name:str):
    """
        python cliapp.py getteams Backendteam
    """
    params={name:name}
    x = requests.get(str(DOMAIN) + '/teams/name='+str(name))
    typer.echo(x.status_code)
    typer.echo(x._content)



if __name__ == "__main__":
    app()
