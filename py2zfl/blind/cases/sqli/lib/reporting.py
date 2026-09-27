"""SQL snippets for the library reporting views."""


def author_totals_sql(author):
    return (
        "SELECT a.id, a.name, COUNT(b.id) AS books "
        "FROM library_author a JOIN library_book b ON b.author_id = a.id "
        "WHERE a.name = '{}' GROUP BY a.id, a.name".format(author)
    )


def author_totals_query(author):
    sql = (
        "SELECT a.id, a.name, COUNT(b.id) AS books "
        "FROM library_author a JOIN library_book b ON b.author_id = a.id "
        "WHERE a.name = %s GROUP BY a.id, a.name"
    )
    return sql, [author]
