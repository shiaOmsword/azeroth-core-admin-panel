import typer
from app.common.cli.commands.characters.characters_cli import app as characters_app
from app.common.cli.commands.remote.remote_cli import app as remote_app
from app.common.cli.commands.remote.characters_cli import app as remote_characters_app
from app.common.cli.commands.auth.realmlists.realmlist_cli import app as realmlists_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(characters_app, name="chars")
app.add_typer(remote_app, name="remote")
app.add_typer(remote_characters_app, name="characters")
app.add_typer(realmlists_app, name="realmlist")
