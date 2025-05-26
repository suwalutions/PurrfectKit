import typer
from typing import Optional

from purrfectmeow.konja import Kornja

calico = typer.Typer(
    name="kornja",
    help=(
        "Kornja CLI - Chunk text using token-based or separator-based strategies.\n\n"
        "Examples:\n"
        "  Token-based:\n"
        "    kornja chunk \"some text\" --splitter token --model-name intfloat/multilingual-e5-large-instruct\n\n"
        "  Separator-based:\n"
        "    kornja chunk \"sentence one. sentence two.\" --splitter separator --separator ."
    )
)

@calico.command("chunk")
def chunk_text(
    text: str = typer.Argument(..., help="Input text to chunk."),
    splitter: str = typer.Option("token", help="Splitter type: 'token' or 'separator'."),
    model_name: Optional[str] = typer.Option(
        "text-embedding-ada-002", help="Model name (used for token-based splitter)."
    ),
    chunk_size: Optional[int] = typer.Option(
        500, help="Chunk size in tokens (for token-based splitter)."
    ),
    chunk_overlap: Optional[int] = typer.Option(
        0, help="Token overlap between chunks (for token-based splitter)."
    ),
    separator: Optional[str] = typer.Option(
        "\n\n", help="Separator string (for separator-based splitter)."
    ),
):
    """
    Chunk text into smaller segments using either token-based or separator-based splitting.
    """
    try:
        kwargs = {}

        if splitter == "token":
            kwargs["model_name"] = model_name
            kwargs["chunk_size"] = chunk_size
            kwargs["chunk_overlap"] = chunk_overlap

        elif splitter == "separator":
            kwargs["separator"] = separator

        else:
            typer.echo("Invalid splitter type. Use 'token' or 'separator'.", err=True)
            raise typer.Exit(code=1)

        chunks = Kornja.chunking(text, splitter=splitter, **kwargs)
        for i, chunk in enumerate(chunks, start=1):
            typer.echo(f"\n--- Chunk {i} ---\n{chunk}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)