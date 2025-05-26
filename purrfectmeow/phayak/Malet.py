import os
import typer

from purrfectmeow.sawat import Malet

calico = typer.Typer(
    name="malet",
    help=(
        "Malet CLI - Extract text from documents, images, and URLs using specialized backends.\n\n"
        "Supported loaders:\n"
        " - MARKITDOWN\n"
        " - DOCLING\n"
        " - PYTESSERACT\n"
        " - EASYOCR\n"
        " - SURYAOCR\n"
        " - PYMUPDF\n"
        " - PYMUPDF_AS_TXT\n"
        " - PANDAS_EXCEL\n"
        " - PANDAS_CSV"
    )
)

@calico.command("extract")
def extract_text(
    file_path: str = typer.Argument(..., help="Path to the file for text extraction."),
    loader: str = typer.Option("PYMUPDF", help="Loader backend to use for extraction."),
):
    """
    Extract text content from the provided file using the specified loader.
    """
    if not os.path.exists(file_path):
        typer.echo(f"Error: File '{file_path}' does not exist.", err=True)
        raise typer.Exit(code=1)

    try:
        with open(file_path, "rb") as f:
            text = Malet.loader(f, os.path.basename(file_path), loader=loader)
        typer.echo(text)
    except ValueError as e:
        typer.echo(f"Loader error: {e}", err=True)
        raise typer.Exit(code=2)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=3)

@calico.command("loaders")
def list_loaders():
    """
    List all supported loader backends.
    """
    typer.echo("Supported loaders:")
    for loader_name in Malet._LOADER_METHODS.keys():
        typer.echo(f" - {loader_name}")