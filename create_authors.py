import vivo_queries.create_person as create_person
import utils.db_util as db_util
import utils.vivo_util as vivo_util


def main():
    print "In main"
    sqlite_conn = db_util.create_connection("db/kakapo.db")
    authors = db_util.get_all_people(sqlite_conn)
    print authors
    make_authors(authors)


def make_authors(authors):
    vivo_conn = vivo_util.get_vivo_connection()

    for author in authors:
        print "Process author: " + author[0]
        params = create_person.get_params(vivo_conn)
        new_author = params["Author"]
        new_author.name = author[0]
        new_author.n_number = author[2]
        response = create_person.run(vivo_conn, **params)
        print(response)


if __name__ == '__main__':
    main()
