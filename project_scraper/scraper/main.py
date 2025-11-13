# scraper/main.py
import logging
from scraper.fetcher import fetch_all, combine_paths

logger = logging.getLogger(__name__)

def main():
    base = "http://localhost:8000"
    # Si en el futuro hay más secciones, se pueden combinar rutas
    common_paths = ["", "about", "robots.txt"]
    extra_paths = ["login", "register", "no_existo"]  # por ejemplo, para ampliar ejercicio
    paths = combine_paths(common_paths, extra_paths)
    logger.info(f"Running scraper with paths: {paths}")
    results = fetch_all(base, paths)
    for path, content in results.items():
        logger.info(f"Path: {path!r}, Content length: {len(content) if content else 'FAILED'}")
        print(f"=== {path or '/'} ===")
        if content:
            print(content[:200] + "...\n")
        else:
            print("FAILED to fetch content.\n")

if __name__ == "__main__":
    main()
