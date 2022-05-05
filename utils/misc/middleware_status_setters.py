from data import const


def rate_limit(limit: int, key=None):
    """Установить лимит по отправке."""

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def clearance_level(level: int = const.REGISTERED_USER):
    """Устанавливает уровень допуска."""
    def decorator(func):
        setattr(func, 'clearance_level', level)

    return decorator
