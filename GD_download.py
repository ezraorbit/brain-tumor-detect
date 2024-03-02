#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests

def download_file_from_google_drive(destination):
    URL = "https://www.dropbox.com/scl/fi/s1j4hu5mt8tshfbz24of9/brain_tumor_model.h5?rlkey=h69fq77crf7qkxygiw8ci9bny&dl=1"

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
