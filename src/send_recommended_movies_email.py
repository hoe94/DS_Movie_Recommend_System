from email.mime.image import MIMEImage
import pandas as pd
import yaml
import requests
from PIL import Image
import urllib.request


import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from collaboration_filtering import main

rating_df = pd.read_parquet('movie_rating.parquet')
input_df = pd.read_parquet('input_user_rating.parquet')

with open('config.yaml', 'rb') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

TMDB_API_KEY = config['API_KEY']
smtp_server = "smtp.gmail.com"
port = 587
sender_email = config['sender_email']
receiver_email = config['receiver_email']
password = config['password']


def get_recommended_movies_image():
    movie_id_list = []
    movie_name_list = []
    movie_poster_url_list = []

    recommended_movies_dict = main(input_df, rating_df)
    for movie_id, movie_title in recommended_movies_dict.items():
        base_url = f'https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={TMDB_API_KEY}'
        language = '&language=en-US'
        include_image = '&include_image_language=en'
        url = base_url + language + include_image
        response = requests.get(url).json()
        #print(json.dumps(response, indent = 4))
        #print(response["posters"][0]['file_path'])
        movie_poster_url = response["posters"][0]['file_path']

        movie_id_list.append(movie_id)
        movie_name_list.append(movie_title)
        movie_poster_url_list.append(movie_poster_url)
    
    return movie_id_list, movie_name_list, movie_poster_url_list

def send_email(movie_id_list, movie_name_list, movie_poster_url_list):
    message = MIMEMultipart()
    message['Subject'] = 'testing email'
    message['From'] =  sender_email
    message['To'] = receiver_email

    base_url = "https://www.themoviedb.org/t/p/w1280"
    text = f"""\
    <html>
        <body>
            <p>This is the recommended movies </p>
            <figure>
                <img src = "{base_url+movie_poster_url_list[0]}" width="500" height="500"><br>
                <h4><figcaption>{movie_name_list[0]}</figcaption></h4>
            </figure>
            
            <figure>
                <img src = "{base_url+movie_poster_url_list[1]}" width="500" height="500"><br>
                <h4><figcaption>{movie_name_list[1]}</figcaption></h4>
            </figure>

            <figure>
                <img src = "{base_url+movie_poster_url_list[2]}" width="500" height="500"><br>
                <h4><figcaption>{movie_name_list[2]}</figcaption></h4>--
            </figure>

            <figure>
                <img src = "{base_url+movie_poster_url_list[3]}" width="500" height="500"><br>
                <h4><figcaption>{movie_name_list[3]}</figcaption></h4>
            </figure>

            <figure>
                <img src = "{base_url+movie_poster_url_list[4]}" width="500" height="500"><br>
                <h4><figcaption>{movie_name_list[4]}</figcaption></h4>
            </figure>
        </body>
    </html> 
    """

    body_text = MIMEText(text, 'html')
    message.attach(body_text)
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # check connection
        server.starttls(context = context)  # Secure the connection
        server.ehlo()  # check connection
        server.login(sender_email, password)

        # Send email here
        server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as e:
        print(e)
    finally:
        server.quit()


movie_id_list, movie_name_list, movie_poster_url_list = get_recommended_movies_image()
send_email(movie_id_list, movie_name_list, movie_poster_url_list)
