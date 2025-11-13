# scraper/fetcher.py
import logging
from functools import lru_cache, partial
from itertools import chain
import httpx

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class FetchError(Exception):
    """Excepción personalizada para errores de fetch."""
    pass

@lru_cache(maxsize=128)
def fetch_url(url: str, timeout: float = 10.0) -> str:
    """
    Descarga el contenido de una URL con httpx.
    Usa lru_cache para evitar volver a descargar la misma URL repetidamente.
    """
    logger.info(f"Fetching URL: {url}")
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
    except httpx.RequestError as e:
        logger.error(f"Network error while requesting {url}: {e}")
        raise FetchError(f"Network error: {e}") from e
    except httpx.HTTPStatusError as e:
        logger.error(f"Bad status code for {url}: {e.response.status_code}")
        raise FetchError(f"Bad status: {e.response.status_code}") from e
    else:
        logger.info(f"Successfully fetched {url} (length {len(response.text)})")
        return response.text

def fetch_all(base_url: str, paths: list[str]) -> dict[str, str]:
    """
    Descarga varias rutas a partir de un base_url.
    Retorna dict path -> contenido.
    Usa partial para fijar el base_url prefijado y chain para procesar iterables.
    """
    logger.info(f"Fetching all paths from base URL {base_url}")
    # Creamos una función que ya tiene fijado el base_url
    fetch_with_base = partial(fetch_url, timeout=10.0)
    results = {}
    for p in paths:
        full = base_url.rstrip("/") + "/" + p.lstrip("/")
        try:
            results[p] = fetch_with_base(full)
        except FetchError as e:
            # No abortamos todo: registramos y seguimos con la siguiente ruta
            logger.warning(f"Failed to fetch path '{p}': {e}")
            results[p] = None
    return results

# Ejemplo de uso de itertools.chain: combinar múltiples listas de paths
def combine_paths(*lists_of_paths: list[str]) -> list[str]:
    """
    Combina varias listas de paths en una sola (usa itertools.chain).
    Útil si queremos extender las rutas en el futuro.
    """
    return list(chain(*lists_of_paths))
