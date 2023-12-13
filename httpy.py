import requests
from requests import Session, Response
from requests.adapters import HTTPAdapter, Retry

from concurrent.futures import ThreadPoolExecutor, as_completed

from urllib.parse import urlparse

from typing import List

import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)8s]: %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

logger = logging.getLogger(__name__)


def get_one(url: str, http: Session = None) -> Response:
    '''
    Realiza o download do conteúdo de uma única URL e retorna o objeto da resposta.

    :param url: A URL para download.
    :type url: str

    :param http: (Opcional) Uma sessão HTTP pré-configurada. O valor padrão é None.
    :type http: requests.Session
    
    :returns: O objeto da resposta para a URL baixada.
    :rtype: requests.Response
    '''
    
    logger.info(f'GET \'{url}\'.')

    if http:
        response = http.get(url)
    else:
        response = requests.get(url)

    response.raise_for_status()

    logger.info(f'GOT \'{url}\'.')

    return response


def get_multiple(urls: List[str], max_workers: int = 10) -> List[Response]:
    '''
    Realiza o download do conteúdo de múltiplas URLs concorrentemente usando um pool de threads.

    :param urls: Uma lista de URLs para download.
    :type urls: list[str]

    :param max_workers: (Opcional) O número máximo de threads a serem usadas para o download. O valor padrão é 10.
    :type max_workers: int

    :returns: Uma lista de objetos de resposta para cada URL baixada.
    :rtype: list[requests.Response]
    '''

    with Session() as session:
        retry = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )

        if urls:
            parsed_url = urlparse(urls[0])
            protocol = parsed_url.scheme
        else:
            protocol = 'https'

        session.mount(f'{protocol}://', HTTPAdapter(max_retries=retry))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = list()

            for url in urls:
                futures.append(executor.submit(get_one, url=url, http=session))

            responses = list()

            for future in as_completed(futures):
                responses.append(future.result())

            return responses
