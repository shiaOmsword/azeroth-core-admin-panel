from typing import Annotated
import typer

Page = Annotated[int, "--page", typer.Option(help="Номер страницы для отображения")] 
AccountId = Annotated[int, "--id", typer.Argument(help="ID аккуанта пользователя")]
CharacterName = Annotated[str, "--name", typer.Argument(help="Имя персонажа")]
CharacterId = Annotated[int, "--id", typer.Argument(help="guid character")]
Value = Annotated[int, "--value", typer.Argument(help="how many talents")]
StrValue = Annotated[str, "--value", typer.Argument(help="string value")]
ItemInstanceId = Annotated[int, "--instance-id", typer.Argument(help="Instance item guid")]