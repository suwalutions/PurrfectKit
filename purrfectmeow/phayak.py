import typer

caracal = typer.Typer()

@caracal.command()
def meowdy(name: str):
    """Meow to user by Name."""
    typer.echo(f"Meow~, {name}! Meowcome to PurrfectKit~")

@caracal.command()
def process_text(
    text: str,
    uppercase: bool = typer.Option(False, "--uppercase", "-u", help="Convert text to uppercase"),
    repeat: int = typer.Option(1, "--repeat", "-r", help="Number of times to repeat the text"),
):
    """Process text with optional transformations."""
    result = text
    if uppercase:
        result = result.upper()
    result = result * repeat
    typer.echo(result)

if __name__ == "__main__":
    caracal()