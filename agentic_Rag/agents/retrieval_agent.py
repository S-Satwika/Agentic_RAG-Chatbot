from core.embeddings import get_embeddings
from core.vector_store import VectorStore
from agents.ingestion_agent import create_mcp_message

vector_db = VectorStore(dim=384)

def store_chunks_mcp(mcp_message):
    chunks = mcp_message["payload"]["chunks"]
    embeddings = get_embeddings(chunks)
    vector_db.add(embeddings, chunks)

def search_chunks_mcp(mcp_message, top_k=3):
    query = mcp_message["payload"]["query"]
    query_vec = get_embeddings([query])[0]
    top_chunks = vector_db.search(query_vec, top_k=top_k)

    return create_mcp_message(
        sender="RetrievalAgent",
        receiver="LLMResponseAgent",
        trace_id=mcp_message["trace_id"],
        msg_type="CONTEXT_RESPONSE",
        payload={
            "top_chunks": top_chunks,
            "query": query
        }
    )
