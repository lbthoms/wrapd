from flask import Flask, render_template, redirect, url_for, session, request
from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = config('SECRET_KEY')

# Load Spotify client ID and client secret from environment variables
spotify_client_id = config('SPOTIFY_CLIENT_ID')
spotify_client_secret = config('SPOTIFY_CLIENT_SECRET')

# Spotify OAuth configuration
sp_oauth = SpotifyOAuth(spotify_client_id, spotify_client_secret, redirect_uri='http://127.0.0.1:8080/callback/q',
                        scope='user-top-read playlist-modify-private')


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Spotify login route
@app.route('/spotify-login')
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


# Callback after Spotify login
@app.route('/callback/q')
def spotify_authorized():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['spotify_token'] = token_info['access_token']

    # Fetch user information from Spotify API
    sp = spotipy.Spotify(auth=session['spotify_token'])
    user_info = sp.current_user()
    session['spotify_user'] = {
        'display_name': user_info.get('display_name', 'Spotify User'),
        'profile_image': user_info.get('images', [{}])[0].get('url', None),
        'id': user_info.get('id', None),  # Add the user ID to the session
    }

    # Store user ID in a separate session key
    session['spotify_user_id'] = session['spotify_user']['id']

    return redirect(url_for('welcome'))


# Spotify logout route
@app.route('/spotify-logout')
def spotify_logout():
    session.pop('spotify_token', None)
    session.pop('spotify_user', None)
    return redirect(url_for('home'))


# Welcome route
@app.route('/welcome')
def welcome():
    if 'spotify_token' in session and 'spotify_user' in session:
        user_info = session['spotify_user']
        return render_template('success.html', username=user_info['display_name'],
                               profile_image=user_info['profile_image'])
    else:
        return redirect(url_for('home'))


# Function to get top tracks based on time range
def get_top_tracks(time_range):
    if 'spotify_token' not in session:
        return redirect(url_for('spotify_login'))

    sp = spotipy.Spotify(auth=session['spotify_token'])
    top_tracks = sp.current_user_top_tracks(limit=25, offset=0, time_range=time_range)

    # Extract relevant information for each track
    tracks_info = []
    for track in top_tracks['items']:
        track_info = {
            'id': track['id'],  # Add the 'id' field to track information
            'name': track['name'],
            'artists': track['artists'],  # Adjust as needed based on the actual structure
            'album': track['album'],
        }
        tracks_info.append(track_info)

    return tracks_info


@app.route('/top-tracks')
def top_tracks():
    time_range = request.args.get('time_range', 'medium_term')  # Default to medium_term if not provided
    tracks_info = get_top_tracks(time_range)
    return render_template('top_tracks.html', top_tracks=tracks_info)


# Function to get top artists based on time range
def get_top_artists(time_range):
    if 'spotify_token' not in session:
        return redirect(url_for('spotify_login'))

    sp = spotipy.Spotify(auth=session['spotify_token'])
    top_artists = sp.current_user_top_artists(limit=25, offset=0, time_range=time_range)

    # Extract relevant information for each artist
    artists_info = []
    for artist in top_artists['items']:
        artist_info = {
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else None,  # Check if images exist
            'genres': artist['genres'],
        }
        artists_info.append(artist_info)

    return artists_info


# Route for generating top artists for user
@app.route('/top-artists')
def top_artists():
    time_range = request.args.get('time_range', 'medium_term')  # Default to medium_term if not provided
    artists_info = get_top_artists(time_range)
    return render_template('top_artists.html', top_artists=artists_info, time_range=time_range)


# Route for generating recommended playlist
@app.route('/recommended-playlist')
def recommended_playlist():
    if 'spotify_token' not in session:
        return redirect(url_for('spotify_login'))

    # Print debug statement to check the value of time_range
    time_range = request.args.get('time_range', 'medium_term')  # Last 6 months

    # Get the user's top tracks for the specified time range
    top_tracks = get_top_tracks(time_range=time_range)

    # Initialize a new Spotify object
    sp = spotipy.Spotify(auth=session['spotify_token'])

    # Create and add tracks to the playlist
    playlist = create_and_add_to_playlist(sp, top_tracks, time_range)

    # Get the playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist['id'])

    return render_template('recommended_playlist.html', playlist_tracks=playlist_tracks)


# Make sure the route with the time_range parameter is correct
@app.route('/recommended-playlist/<time_range>')
def recommended_playlist_with_range(time_range):
    if 'spotify_token' not in session:
        return redirect(url_for('spotify_login'))

    # Get the user's top tracks for the specified time range
    top_tracks = get_top_tracks(time_range=time_range)

    # Create and add tracks to the playlist
    playlist = create_and_add_to_playlist(top_tracks, time_range)

    # Initialize a new Spotify object
    sp = spotipy.Spotify(auth=session['spotify_token'])

    # Get the playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist['id'])

    return render_template('recommended_playlist.html', playlist_tracks=playlist_tracks)


def create_and_add_to_playlist(sp, top_tracks, time_range):
    if 'spotify_token' not in session:
        return redirect(url_for('spotify_login'))

    # Extract track URIs from the top tracks
    track_uris = [f"spotify:track:{track['id']}" for track in top_tracks]

    # Set the number of seeds (tracks used for recommendations)
    num_seeds = 5  # Change this to the desired number of seeds

    # Get recommendations based on the specified seeds
    recommendations = sp.recommendations(seed_tracks=track_uris[:num_seeds], limit=25)

    # Extract track URIs from the recommendations
    recommended_track_uris = [track['uri'] for track in recommendations['tracks']]

    # Map time range to term length
    term_length_map = {
        'short_term': '4 weeks',
        'medium_term': '6 months',
        'long_term': 'All Time',
    }

    term_length = term_length_map.get(time_range, 'All Time')

    # Create a new playlist with a customized name
    playlist_name = f"WRAP'd Playlist Based on {term_length}"
    playlist_description = f"Playlist generated by WRAP'd based on your top tracks from the last {term_length}."
    playlist = sp.user_playlist_create(
        user=session['spotify_user_id'],
        name=playlist_name,
        public=False,
        description=playlist_description
    )

    # Add recommended tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=recommended_track_uris)
    return playlist


if __name__ == '__main__':
    app.run(debug=True, port=8080)
