from fastapi import APIRouter

other_router = APIRouter()

@other_router.get('/')
async def get_root():
    return {'status': 'online'}
