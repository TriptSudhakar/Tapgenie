import requests
def translate(qq):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": qq,
        "target": "es",
        "source": "en"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "a076b6bd15mshc96b2a003fbf3dcp143dbbjsn67d80a142f2e",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return (response.json()['data']['translations'][0]['translatedText'])
translate("Hello raghav, How are you ?")