from math import ceil


def paginate_query(query, page: int = 1, page_size: int = 10):
    total_results = query.count()
    query = query.offset((page - 1) * page_size).limit(page_size)
    results = query.all()

    total_pages = ceil(total_results / page_size)
    return {
        "results": results,
        "page": page,
        "page_size": page_size,
        "total_results": total_results,
        "total_pages": total_pages
    }
