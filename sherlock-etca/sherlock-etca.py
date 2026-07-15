#!/usr/bin/env python3
"""
Sherlock-ETCA v1.0 - Herramienta de OSINT para redes sociales.
Creado por ETCA (Edison Tobias Calderara Ayala) - https://github.com/thacker19
Basado en el concepto de Sherlock, pero optimizado y con estilo ETCA.
"""
import requests
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# --------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------
VERSION = "1.0"
CREADOR = "ETCA (Edison Tobias Calderara Ayala)"
REPO_URL = "https://github.com/thacker19/sherlock-etca"

# Base de datos de sitios (más de 50 sitios populares)
SITES = {
    "instagram": "https://www.instagram.com/{}",
    "twitter": "https://twitter.com/{}",
    "github": "https://github.com/{}",
    "youtube": "https://www.youtube.com/@{}",
    "tiktok": "https://www.tiktok.com/@{}",
    "reddit": "https://www.reddit.com/user/{}",
    "pinterest": "https://www.pinterest.com/{}",
    "tumblr": "https://{}.tumblr.com",
    "flickr": "https://www.flickr.com/people/{}",
    "vimeo": "https://vimeo.com/{}",
    "soundcloud": "https://soundcloud.com/{}",
    "spotify": "https://open.spotify.com/user/{}",
    "twitch": "https://www.twitch.tv/{}",
    "patreon": "https://www.patreon.com/{}",
    "discord": "https://discord.com/users/{}",  # Solo si es público
    "telegram": "https://t.me/{}",
    "whatsapp": "https://wa.me/{}",  # No funciona directamente
    "linkedin": "https://www.linkedin.com/in/{}",
    "facebook": "https://www.facebook.com/{}",
    "snapchat": "https://www.snapchat.com/add/{}",
    "tinder": "https://tinder.com/@{}",
    "badoo": "https://badoo.com/en/{}",
    "ok": "https://ok.ru/{}",
    "vk": "https://vk.com/{}",
    "xing": "https://www.xing.com/profile/{}",
    "meetup": "https://www.meetup.com/members/{}",
    "pastebin": "https://pastebin.com/u/{}",
    "hackernews": "https://news.ycombinator.com/user?id={}",
    "devto": "https://dev.to/{}",
    "medium": "https://medium.com/@{}",
    "wordpress": "https://{}.wordpress.com",
    "blogger": "https://{}.blogspot.com",
    "gravatar": "https://en.gravatar.com/{}",
    "keybase": "https://keybase.io/{}",
    "gitlab": "https://gitlab.com/{}",
    "bitbucket": "https://bitbucket.org/{}/",
    "sourceforge": "https://sourceforge.net/u/{}",
    "hackaday": "https://hackaday.io/{}",
    "instructables": "https://www.instructables.com/member/{}",
    "thingiverse": "https://www.thingiverse.com/{}",
    "replit": "https://replit.com/@{}",
    "codepen": "https://codepen.io/{}",
    "jsfiddle": "https://jsfiddle.net/user/{}",
    "hackerrank": "https://www.hackerrank.com/{}",
    "codewars": "https://www.codewars.com/users/{}",
    "leetcode": "https://leetcode.com/{}",
    "topcoder": "https://www.topcoder.com/members/{}",
    "freecodecamp": "https://www.freecodecamp.org/{}",
    "kaggle": "https://www.kaggle.com/{}",
    "coursera": "https://www.coursera.org/user/{}",
    "udemy": "https://www.udemy.com/user/{}",
}

# --------------------------------------------
# FUNCIONES PRINCIPALES
# --------------------------------------------

def check_username(site, username):
    """
    Verifica si un usuario existe en un sitio específico.
    Retorna (site, url, encontrado).
    """
    url = SITES[site].format(username)
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return (site, url, True)
        else:
            return (site, url, False)
    except:
        return (site, url, False)

def search(username):
    """
    Busca un username en todos los sitios de la base de datos.
    """
    print(f"\n[+] Buscando usuario: {username}")
    print(f"[+] Sitios a revisar: {len(SITES)}")
    print("-" * 50)

    found = []
    not_found = []
    errors = []

    # Usamos ThreadPoolExecutor para hacer las peticiones en paralelo (más rápido)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_username, site, username): site for site in SITES}
        
        for future in as_completed(futures):
            site, url, exists = future.result()
            if exists:
                print(f"[+] {site}: {url}")
                found.append((site, url))
            else:
                print(f"[-] {site}: No encontrado")
                not_found.append(site)

    # Resumen final
    print("\n" + "=" * 50)
    print(f"[+] Total encontrados: {len(found)}")
    print(f"[-] No encontrados: {len(not_found)}")
    print(f"[!] Errores: {len(errors)}")
    print("=" * 50)

    return found

def guardar_resultados(username, found, archivo=None):
    """
    Guarda los resultados en un archivo de texto.
    """
    if not archivo:
        archivo = f"resultados_{username}.txt"
    
    with open(archivo, "w") as f:
        f.write(f"ETCA-OSINT v{VERSION} - Resultados para: {username}\n")
        f.write(f"Creado por: {CREADOR}\n")
        f.write(f"Repositorio: {REPO_URL}\n")
        f.write("=" * 50 + "\n\n")
        
        if found:
            for site, url in found:
                f.write(f"[+] {site}: {url}\n")
        else:
            f.write("No se encontraron perfiles.\n")
    
    print(f"\n[+] Resultados guardados en: {archivo}")

def mostrar_banner():
    """
    Muestra el banner de ETCA-OSINT.
    """
    banner = f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  ETCA-OSINT v{VERSION}                                   ║
    ║  Herramienta de OSINT para redes sociales                ║
    ║  Creado por: {CREADOR}                 ║
    ║  Repositorio: {REPO_URL}  ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

# --------------------------------------------
# MAIN
# --------------------------------------------

def main():
    # Mostrar banner
    mostrar_banner()

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python3 etca-osint.py <username> [--guardar]")
        print("Ejemplo: python3 etca-osint.py linux_1010 --guardar")
        sys.exit(1)

    username = sys.argv[1]
    guardar = "--guardar" in sys.argv

    # Iniciar búsqueda
    inicio = time.time()
    found = search(username)
    fin = time.time()

    print(f"\n[+] Tiempo total: {fin - inicio:.2f} segundos")

    # Guardar resultados si se solicita
    if guardar and found:
        guardar_resultados(username, found)

if __name__ == "__main__":
    main()
