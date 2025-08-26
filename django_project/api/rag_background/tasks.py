from celery import shared_task
import logging
import google_drive_manager


@shared_task
def connector(x, y):
    logging.info('Starting connector')
    google_drive_manager.index_with_google_drive()
    logging.info('Connector execution complete')


@shared_task
def chunking_and_embedding():
    # todo: madan: pull items one by one from chunking_and_embedding queue
    # queue name is defined in settings.RAG.QUEUE_CHUNKING_AND_EMBEDDING
    # then perform chunking and embedding
    pass
