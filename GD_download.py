#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests

def download_file_from_google_drive(destination):
    URL = "https://www.dropbox.com/scl/fi/ost4oplhu4jeecdv27w87/brain_tumor_model.h5?rlkey=my1e0ivp7ch48l4z8hft84qy4&dl=1"

    session = requests.Session()

    response = session.get(URL, stream = True)
    token = get_confirm_token(response)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
