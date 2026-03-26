from aiogram import Router
from .start import router as start_router
from .expenses import router as expenses_router
from .reports import router as reports_router


router = Router()

router.include_routers(
    start_router,
    expenses_router,
    reports_router
)
