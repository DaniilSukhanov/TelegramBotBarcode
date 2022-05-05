from aiogram import types


async def set_default_commands(dp):
    """Ставит команды для бота."""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand('register', 'Регистрация'),
            types.BotCommand('statistics', "Получить статистику")
        ]
    )
