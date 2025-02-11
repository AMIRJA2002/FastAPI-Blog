from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from math import ceil



async def paginate_query(query, db: AsyncSession, page: int = 1, page_size: int = 10):
    total_results = await db.scalar(func.count().select().select_from(query.subquery()))

    results = await db.execute(query.offset((page - 1) * page_size).limit(page_size))
    results = results.unique().scalars().all()

    total_pages = ceil(total_results / page_size)

    return {
        "results": results,
        "page": page,
        "page_size": page_size,
        "total_results": total_results,
        "total_pages": total_pages,
    }
