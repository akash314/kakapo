from Bio import Entrez
from Bio import Medline
from owlery import Connection
import queries.make_academic_article as create_query
import yaml
import utils.db_util as db_util


def main():
    print "In main"
    Entrez.email = "agarwalakash@ufl.edu"

    conn = db_util.create_connection("db/kakapo.db")
    authors = db_util.get_all_people(conn)
    for author in authors:
        process_author(author)
    '''
    with open('vivo_author_nnumber.csv', 'rb') as author_csv:
        reader = csv.reader(author_csv)
        for row in reader:
            process_author(row)
    '''


def process_author(author):
    author_name = author[2]
    connection = get_vivo_connection()
    doc_list = get_pubmed_docs_for_author(author_name)
    for doc in doc_list:
        add_academic_article(connection, doc, author[0])


def add_academic_article(connection, doc, author_nnum):
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
    print(response)


def get_pubmed_docs_for_author(author_name):
    search_term = author_name + "[Full Author Name]"

    handle = Entrez.esearch(db="pubmed", term=search_term)
    record = Entrez.read(handle)

    print "Journal IDs for %s: " % author_name + ",".join(record['IdList'])

    handle = Entrez.efetch(db="pubmed", id=record['IdList'], rettype="MEDLINE", retmode="text")
    records = Medline.parse(handle)
    doc_list = list(records)
    return doc_list


def get_vivo_connection():
    config_path = "config/config.yaml"
    config = get_config(config_path)

    email = config.get('email')
    password = config.get ('password')
    update_endpoint = config.get('update_endpoint')
    query_endpoint = config.get('query_endpoint')
    vivo_url = config.get('upload_url')
    check_url = config.get('checking_url')

    connection = Connection(vivo_url, check_url, email, password, update_endpoint, query_endpoint)
    return connection


def get_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Error: Check config file")
        exit()
    return config

if __name__ == '__main__':
    main()


