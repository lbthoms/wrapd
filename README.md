## WRAP'd

### INF601 Advanced Programming with Python
### Lisa Thoms

![Picture of the Spotify logo, but purple to match my app. ](https://icones.pro/wp-content/uploads/2021/04/icone-spotify-violet.png)

## Description
This is a Flask-based web application that will allow users to login in to their Spotify profiles
and view their Top Tracks, Top Artists, and Top Genres from the last 4 weeks, 6 months, and All-Time.
They will also have the option to generate a playlist with recommended songs based on their last 6 months
of listening and add that playlist to their Spotify application. 

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
Here are some examples of how the different pages will display once the application is ran.

### Top Tracks
(https://i.ibb.co/pRLsk9J/tracks.png)

### Top Artists
(https://i.ibb.co/xfcjD6M/artists.png)