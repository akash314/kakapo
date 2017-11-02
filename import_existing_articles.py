import utils.vivo_util as vivo_util
import vivo_queries.get_articles_by_author as get_articles_query
import utils.db_util as db_util


def main():
    sqlite_conn = db_util.create_connection("db/kakapo.db")
    vivo_conn = vivo_util.get_vivo_connection()
    authors = db_util.get_all_people(sqlite_conn)
    authors = [authors[0]]

    for author in authors:
        author_nnum = author[2]
        params = get_articles_query.get_params(vivo_conn)
        params["Author"].n_number = author_nnum
        articles = get_articles_query.run(vivo_conn, **params)

        db_util.add_uploaded_articles(sqlite_conn, articles)
        pubmed_ids = [article[1] for article in articles]
        pubmed_ids_string = ",".join(pubmed_ids)

        update_obj = (pubmed_ids_string, author_nnum)
        db_util.update_author(sqlite_conn, update_obj)

        # TODO Handle articles without PMID, maybe find title similarity when downloading from Pubmed

if __name__ == '__main__':
    main()
