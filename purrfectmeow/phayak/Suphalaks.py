import json
import typer
from typing import Optional, List

from purrfectmeow.taeng import Suphalaks

calico = typer.Typer(
    name="suphalaks",
    help=(
        "Suphalaks CLI - Utility commands for handling files, extracting metadata, "
        "and interacting with Hugging Face models and tokenizers.\n\n"
        "This tool provides a streamlined interface for:\n"
        "- Saving and removing temporary files\n"
        "- Loading pretrained models and tokenizers from Hugging Face\n"
        "- Extracting file metadata\n"
        "- Generating LangChain-compatible Document templates"
    )
)

@calico.command("save-file")
def save_file(
    file_path: str = typer.Argument(..., help="Path to the binary file to save."),
    file_name: str = typer.Argument(..., help="Name to assign to the saved file.")
):
    """Save a binary file to a temporary directory."""
    with open(file_path, "rb") as f:
        result = Suphalaks.save_file(f, file_name)
    typer.echo(f"Saved file to: {result}")

@calico.command("remove-file")
def remove_file(
    file_path: str = typer.Argument(..., help="Path to the file to remove.")
):
    """Remove a file from the filesystem."""
    Suphalaks.remove_file(file_path)
    typer.echo(f"Removed file: {file_path}")

@calico.command("get-model")
def get_model(
    model_name: Optional[str] = typer.Argument(
        None, help="Name or path of the Hugging Face model."
    )
):
    """Load and return a Hugging Face pretrained model."""
    model = Suphalaks.get_model(model_name or "")
    typer.echo(f"Loaded model: {model.__class__.__name__}")

@calico.command("get-tokenizer")
def get_tokenizer(
    model_name: Optional[str] = typer.Argument(
        None, help="Name or path of the tokenizer."
    )
):
    """Load and return a Hugging Face tokenizer."""
    tokenizer = Suphalaks.get_tokenizer(model_name or "")
    typer.echo(f"Loaded tokenizer: {tokenizer.__class__.__name__}")

@calico.command("get-metadata")
def get_metadata(
    file_path: str = typer.Argument(..., help="Path to the file to extract metadata from.")
):
    """Extract metadata from a given file."""
    metadata = Suphalaks.get_file_metadata(file_path)
    typer.echo(json.dumps(metadata, indent=2))

@calico.command("create-document")
def create_document(
    chunks: List[str] = typer.Option(..., "--chunk", help="Text chunks to include in the document."),
    metadata: str = typer.Option(..., help="JSON string representing the metadata.")
):
    """Create a LangChain Document from text chunks and metadata."""
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        typer.echo("Invalid metadata JSON.", err=True)
        raise typer.Exit(code=1)

    document = Suphalaks.document_template(chunks, metadata_dict)
    typer.echo(f"Document created with metadata: {document.metadata}")