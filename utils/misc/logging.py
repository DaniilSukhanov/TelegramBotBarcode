import logging

logging.basicConfig(
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  '
           u'%(message)s',
    level=logging.INFO,
)
