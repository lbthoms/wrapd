## WRAP'd

### INF601 Advanced Programming with Python
### Lisa Thoms

![Picture of the Spotify logo, but purple to match my app. ](https://icones.pro/wp-content/uploads/2021/04/icone-spotify-violet.png)

## Description
This is a Flask-based web application using the spotipy package that will allow users to login in to 
their Spotify profiles and view their Top Tracks and Top Artists from the last 4 weeks, 6 months, and All-Time.

They will also have the option to generate a playlist with 25 recommended songs based on those three time ranges and 
add the playlist to their personal Spotify library.

 ## Pip Install Instructions
Please run the following:
```
pip install -r requirements.txt
```

## IMPORTANT! Create .env file with your Spotify API credentials
```
# wrapd/.env

SPOTIFY_CLIENT_ID=your client id goes here
SPOTIFY_CLIENT_SECRET=your secret key goes here

```

## How To Run

```
python wrapd/main.py
```

## Examples
Here are some examples of how the different pages will display once the application has successfully run:

### Top Tracks
![Picture of the website display of top tracks.html ](https://i.ibb.co/j6xPNXP/tracks.png)

### Top Artists
![Picture of the website display of top artists.html ](https://i.ibb.co/0FdKJQ3/artists.png)