from typing import Annotated
import typer

Page = Annotated[int, "--page", typer.Option(help="Номер страницы для отображения")] 
AccountId = Annotated[int, "--id", typer.Argument(help="ID аккуанта пользователя")]
CharacterName = Annotated[str, "--name", typer.Argument(help="Имя персонажа")]
CharacterId = Annotated[int, "--id", typer.Argument(help="guid character")]
Value = Annotated[int, "--value", typer.Argument(help="how many talents")]
StrValue = Annotated[str, "--value", typer.Argument(help="string value")]
ItemInstanceId = Annotated[int, "--instance-id", typer.Argument(help="Instance item guid")]
EnchantmentId = Annotated[
    int,
    typer.Argument(help="SpellItemEnchantment ID"),
]
EnchantmentSlotOption = Annotated[
    int | None,
    typer.Option("--slot", help="Custom slot number from 7 to 11"),
]
Overwrite = Annotated[
    bool,
    typer.Option("--overwrite", help="Allow replacing an occupied custom slot"),
]
DryRun = Annotated[
    bool,
    typer.Option("--dry-run", help="Calculate the change without writing to the database"),
]
