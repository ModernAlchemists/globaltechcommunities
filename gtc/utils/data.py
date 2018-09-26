from google.appengine.api import search


def deleteAllInIndex(index):
    """Delete all the docs in the given index."""
    docindex = search.Index(index)

    try:
        while True:
            # until no more documents, get a list of documents,
            # constraining the returned objects to contain only the doc ids,
            # extract the doc ids, and delete the docs.
            document_ids = [document.doc_id for document in docindex.get_range(ids_only=True)]
            if not document_ids:
                break
            docindex.delete(document_ids)
    except search.DeleteError:
        logging.exception("Error removing documents:")

