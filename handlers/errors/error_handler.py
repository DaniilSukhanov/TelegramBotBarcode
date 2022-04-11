import logging
from aiogram.utils.exceptions import (TelegramAPIError,
                                      MessageNotModified,
                                      CantParseEntities, CantDemoteChatCreator,
                                      MessageCantBeDeleted,
                                      MessageToDeleteNotFound,
                                      MessageTextIsEmpty, Unauthorized,
                                      InvalidQueryID, RetryAfter)


from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        # do something here?
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        # or here
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        # or here
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        # well, you know.
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
      
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
      
    #  MUST BE THE  LAST CONDITION (ЭТО УСЛОВИЕ ВСЕГДА ДОЛЖНО БЫТЬ В КОНЦЕ)
    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    
    # At least you have tried.
    logging.exception(f'Update: {update} \n{exception}')
