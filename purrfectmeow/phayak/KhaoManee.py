import typer
import json
from typing import List
from langchain_core.documents import Document

from purrfectmeow.plort import KhaoManee

app = typer.Typer(
    name="plort",
    help=(
        "Plort CLI (KhaoManee) - Commands for embedding, tokenization, and similarity search.\n\n"
        "Use this tool to embed documents, tokenize text, or search for the most relevant documents."
    )
)

@app.command("embed-docs")
def embed_documents(
    texts: List[str] = typer.Option(..., "--text", help="Document content(s) to embed."),
    model_name: str = typer.Option(
        "intfloat/multilingual-e5-large-instruct", help="Hugging Face model name for embedding."
    ),
):
    """Generate embeddings for one or more documents."""
    documents = [Document(page_content=txt) for txt in texts]
    embeddings = KhaoManee.get_embeddings(documents, model_name)
    typer.echo(f"Embeddings shape: {embeddings.shape}")
    typer.echo(embeddings.tolist())

@app.command("embed-query")
def embed_query(
    query: str = typer.Argument(..., help="Query string to embed."),
    model_name: str = typer.Option(
        "intfloat/multilingual-e5-large-instruct", help="Model to use for query embedding."
    ),
):
    """Generate an embedding vector for a query."""
    embedding = KhaoManee.get_query_embeddings(query, model_name)
    typer.echo(f"Query embedding shape: {embedding.shape}")
    typer.echo(embedding.tolist())

@app.command("tokenize")
def tokenize(
    text: str = typer.Argument(..., help="Text to tokenize."),
    engine: str = typer.Option("pythainlp", help="Engine: 'spacy', 'pythainlp', or 'huggingface'."),
):
    """Tokenize input text using a specified NLP engine."""
    tokens = KhaoManee.get_tokens(text, engine)
    typer.echo(json.dumps(tokens, ensure_ascii=False))

@app.command("search")
def similarity_search(
    query: str = typer.Argument(..., help="Query text to match."),
    documents: List[str] = typer.Option(..., "--doc", help="List of document texts to compare."),
    model_name: str = typer.Option(
        "intfloat/multilingual-e5-large-instruct", help="Model name to use for embeddings."
    ),
    top_k: int = typer.Option(3, help="Number of top documents to return."),
):
    """Perform a top-k similarity search using vector embeddings."""
    docs = [Document(page_content=txt) for txt in documents]
    doc_embeddings = KhaoManee.get_embeddings(docs, model_name)
    query_embedding = KhaoManee.get_query_embeddings(query, model_name)
    top_docs = KhaoManee.get_search(query_embedding, list(doc_embeddings), docs, top_k)

    typer.echo("\nTop matching documents:")
    for i, doc in enumerate(top_docs, start=1):
        typer.echo(f"\n--- Document {i} ---\n{doc.page_content}")