from author import Author


def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params


def run(connection, **params):
    q = """ SELECT ?label ?article ?pubmed_id
    WHERE {{
    <{url}{Author_n}> <http://vivoweb.org/ontology/core#relatedBy> ?relation .
    ?relation <http://vivoweb.org/ontology/core#relates> ?article .
    ?article <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> .
    ?article <http://www.w3.org/2000/01/rdf-schema#label> ?label .
    ?article <http://purl.org/ontology/bibo/pmid> ?pubmed_id .
    }} """\
        .format(url = connection.vivo_url, Author_n = params['Author'].n_number)

    response = connection.run_query(q)
    print(response)

    article_dump = response.json()
    all_articles = []
    for listing in article_dump['results']['bindings']:
        a_url = listing['article']['value']
        a_n = a_url.rsplit('/', 1)[-1]
        a_pmid = listing['pubmed_id']['value']
        all_articles.append((a_n, a_pmid))

    return all_articles
