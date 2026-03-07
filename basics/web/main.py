import requests as req

def lade_webseite(url):

    res = req.get(url)
    print("Status Code:", res.status_code)
    print("Erste 200 Zeichen")
    print(res.text[:1000])


if __name__ == "__main__":

    lade_webseite("https://azlan-ainto.de")
    
