import typer
from app.common.cli.commands.characters.characters_cli import app as characters_app
from app.common.cli.commands.remote.remote_cli import app as remote_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(characters_app, name="chars")
app.add_typer(remote_app, name="remote")
