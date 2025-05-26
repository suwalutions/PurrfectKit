import typer
import numpy
from typing import Optional
from langchain_core.documents import Document

from purrfectmeow.meeze import WichienMaat

app = typer.Typer(
    name="wichienmaat",
    help=(
        "WichienMaat CLI - Perform similarity search over embedded documents.\n\n"
        "Example:\n"
        "  wichienmaat search \\\n"
        "    --query-embedding '0.1,0.2,0.3' \\\n"
        "    --embeddings '0.1,0.2,0.3;0.4,0.5,0.6' \\\n"
        "    --documents 'Hello world;Bonjour monde' \\\n"
        "    --top-k 1\n"
    )
)

@app.command("search")
def search(
    query_embedding: str = typer.Option(..., help="Comma-separated query embedding vector, e.g. '0.1,0.2,0.3'"),
    embeddings: str = typer.Option(..., help="Semicolon-separated list of comma-separated document embeddings, e.g. '0.1,0.2,0.3;0.4,0.5,0.6'"),
    documents: str = typer.Option(..., help="Semicolon-separated list of document texts, e.g. 'Hello world;Bonjour monde'"),
    top_k: Optional[int] = typer.Option(5, help="Number of top documents to retrieve"),
):
    """
    Search for the top_k documents most similar to the query embedding.
    """
    try:
        query_emb = numpy.array([float(x) for x in query_embedding.split(",")])
        embeddings_list = [
            numpy.array([float(i) for i in emb.split(",")]) for emb in embeddings.split(";")
        ]
        documents_list = [Document(page_content=doc.strip()) for doc in documents.split(";")]

        top_docs = WichienMaat.get_search(
            query_embedding=query_emb,
            embeddings=embeddings_list,
            documents=documents_list,
            top_k=top_k
        )
        for i, doc in enumerate(top_docs, start=1):
            typer.echo(f"\n--- Result {i} ---\n{doc.page_content}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)