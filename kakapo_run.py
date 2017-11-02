from Bio import Entrez
from Bio import Medline
import queries.make_academic_article as create_query
import utils.db_util as db_util
import utils.vivo_util as vivo_util


def main():
    print "In main"
    Entrez.email = "agarwalakash@ufl.edu"

    sqlite_conn = db_util.create_connection("db/kakapo.db")
    authors = db_util.get_all_people(sqlite_conn)
    print("Authors: ")
    print authors
    process_all_authors(authors, sqlite_conn)


def process_all_authors(authors, sqlite_conn):
    existing_authors = {}
    existing_articles = set()

    # Create an existing authors dictionary
    for author in authors:
        existing_authors.update({author[0]: {"n_num": author[2], "pubs": set()}})
        # TODO Instead of setting empty pubs read from db
        # TODO Add existing article to existing_articles set so if article exists do not create a duplicate.

    for author in authors:
        print author
        author_name = author[0]
        n_number = author[2]
        vivo_conn = vivo_util.get_vivo_connection()
        doc_ids = get_pubmed_doc_ids_for_author(author_name)
        doc_set = set(doc_ids)
        existing_author = existing_authors.get(author_name)
        existing_docs = existing_author.get("pubs")

        new_docs_set = doc_set.difference(existing_docs)
        print "New docs"
        print new_docs_set
        new_docs_list = get_pubmed_docs_for_ids(new_docs_set)

        nnum_to_pmid = []

        for doc in new_docs_list:
            params = add_academic_article(vivo_conn, doc, n_number)
            nnum_to_pmid.append((params['Article'].n_number, params['Article'].pubmed_id))

        db_util.add_uploaded_articles(sqlite_conn, nnum_to_pmid)

        # TODO 1. Save updated doc list to disk
        # TODO 2. If the document has more authors add reference to other authors.
        # TODO 3. Create other authors if needed else update existing.
        # TODO 4. Add AUID and save to disk if available.

        # Update author to include new docs
        existing_docs.update(new_docs_set)
        print "Update existing"
        print existing_docs
        existing_author["pubs"] = existing_docs
        existing_authors[author_name] = existing_author

        journal_ids_string = ",".join(existing_author["pubs"])
        update_obj = (journal_ids_string, n_number)

        # Associate new pubmed ids with person
        db_util.update_author(sqlite_conn, update_obj)

        # Update article list
        existing_articles.update(existing_docs)


def add_academic_article(connection, doc, author_nnum):
    """
    Create new article in vivo
    :param connection: vivo connection object
    :param doc: article to add
    :param author_nnum: author's n_number in vivo
    :return: params
    """

    params = create_query.get_params(connection)
    article = params["Article"]
    article.name = doc.get("TI")
    article.volume = doc.get("VI")
    article.issue = doc.get("IP")
    pub_year = doc.get("DP").partition(' ')[0]
    article.publication_year = pub_year
    article.pubmed_id = doc.get("PMID")
    author = params["Author"]
    author.n_number = author_nnum
    print (params["Article"]).__dict__
    response = create_query.run(connection, **params)
    #print(response)
    return params


def get_pubmed_doc_ids_for_author(author_name):
    """
    Get the pubmed ids for all articles authored by a person
    :param author_name: Full author name in pubmed (Of the form - lastname, firstname middle_initial)
    :return: list of pubmed ids
    """
    search_term = author_name + "[Full Author Name]"
    handle = Entrez.esearch(db="pubmed", term=search_term)
    record = Entrez.read(handle)
    print "Journal IDs for %s: " % author_name + ",".join(record['IdList'])

    return record['IdList']


def get_pubmed_docs_for_ids(id_set):
    """
    Download journal articles from pubmed for given set of ids.
    :param id_set: Python set containing pubmed ids
    :return: List of articles.
    """
    id_list = list(id_set)
    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="MEDLINE", retmode="text")
    records = Medline.parse(handle)
    doc_list = list(records)

    return doc_list


if __name__ == '__main__':
    main()


