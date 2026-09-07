"""Public metadata is independent of document contents."""

def metadata(document):
    return {"document_id": document["document_id"], "title": document["title"]}
