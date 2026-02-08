from __future__ import annotations

import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config.settings import Settings, get_settings
from handlers import router

logging.basicConfig(level=logging.INFO)


def build_dispatcher(settings: Settings) -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    dispatcher.workflow_data["settings"] = settings
    return dispatcher


async def on_startup(bot: Bot, settings: Settings) -> None:
    if settings.webhook_url:
        await bot.set_webhook(settings.webhook_url)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


async def run_webhook() -> None:
    settings = get_settings()
    bot = Bot(settings.bot_token)
    dispatcher = build_dispatcher(settings)

    dispatcher.startup.register(lambda _: on_startup(bot, settings))
    dispatcher.shutdown.register(lambda _: on_shutdown(bot))

    app = web.Application()
    SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(app, path="/webhook")
    setup_application(app, dispatcher, bot=bot)
    web.run_app(app, host="0.0.0.0", port=settings.port)


async def run_polling() -> None:
    settings = get_settings()
    bot = Bot(settings.bot_token)
    dispatcher = build_dispatcher(settings)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(run_webhook())
    except RuntimeError:
        asyncio.run(run_polling())
