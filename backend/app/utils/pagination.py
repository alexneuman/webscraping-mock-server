
from fastapi.exceptions import HTTPException

def enforce_max_total(offset, limit, max_total=1000):
    if offset + limit > max_total:
        raise HTTPException(404, f'Cannot request beyond limit {max_total}')
    