# Copyright (c) 2023 Frankie Pang
# SpotiSync a Spotify Visualizer
# Written by Frankie Pang
# Website at https://mrfrank.art

import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import io
import pygame
from pygame.locals import *
import fast_colorthief
import os

# Function to calculate brightness of a color
def brightness(color):
    # Calculate brightness based on the formula Y = 0.299*R + 0.587*G + 0.114*B
    r, g, b = color
    return (0.299 * r + 0.587 * g + 0.114 * b)

# Determine if text should be white or black based on background brightness
def determine_text_color(background_color):
    if brightness(background_color) > 128:
        return (0, 0, 0)  # Black text for bright backgrounds
    else:
        return (255, 255, 255)  # White text for dark backgrounds

# Spotify API credentials
SPOTIPY_CLIENT_ID = '08a90f6e29b8459e804801848ed2ef0a'
SPOTIPY_CLIENT_SECRET = '03bc3b6f706d49bf8f7f4600450a2c56'
SPOTIPY_REDIRECT_URI = 'http://localhost:1234'

# Create the Spotipy object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-read-playback-state'))

# Initialize Pygame
pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
font = pygame.font.Font(None, 36)

# Define the file path for the album image
album_image_path = "album_image.jpg"
previous_album_image_path = "previous_album_image.jpg"
signature_path = "FrankSignature.png"

# Watermark inclusion
watermark_image = pygame.image.load(signature_path)
watermark_image = pygame.transform.scale(watermark_image, (100, 100))

# Position of the watermark (bottom left)
watermark_x = screen_width - watermark_image.get_width()  # Position it at the right
watermark_y = screen_height - watermark_image.get_height()  # Position it at the bottom

def center_text_horizontally(surface, text, y):
    text_rect = text.get_rect()
    text_rect.centerx = surface.get_rect().centerx
    text_rect.y = y
    return text_rect

def save_current_album_image(album_image):
    # Save the current album image to a file
    pygame.image.save(album_image, album_image_path)

def save_previous_album_image(album_image):
    # Save the previous album image to a file
    pygame.image.save(album_image, previous_album_image_path)

# Load the previous album image if it exists
if os.path.exists(previous_album_image_path):
    previous_album_image = pygame.image.load(previous_album_image_path)
else:
    previous_album_image = None

# Initialize the previous track ID
previous_track_name = None
track_list = []
advert = False

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:  # Detect spacebar press
                running = False

        # Get the current playback info
        current_track = sp.current_playback()

        if current_track is not None:
            if current_track.get("item") and current_track["item"]["type"] == "track":
                track_name = current_track['item']['name']
                artist_name = current_track['item']['artists'][0]['name']
                album_name = current_track['item']['album']['name']
                album_image_url = current_track['item']['album']['images'][0]['url']
                advert = False
            else:
                # Handle Spotify ad here
                advert = True
                track_name = "Advertisement"
                artist_name = ""
                album_name = ""
                album_image = pygame.image.load(signature_path)
                album_image = pygame.transform.scale(album_image, (400, 400))

            # New Song Detection
            if track_name not in track_list:
                track_list.append(track_name)
                if len(track_list) > 1:
                    save_previous_album_image(album_image)
                    if previous_track_name in track_list:
                        track_list.remove(previous_track_name)
                previous_track_name = track_name

            if advert == False:
                # Get the album art image
                response = requests.get(album_image_url)
                album_image = Image.open(io.BytesIO(response.content))
                album_image = album_image.resize((400, 400))
                album_image = album_image.convert()
                album_image = pygame.image.fromstring(album_image.tobytes(), album_image.size, album_image.mode)

            # Save the current album image to a file
            save_current_album_image(album_image)

            # Calculate the dominant color from the saved image
            dominant_color = fast_colorthief.get_dominant_color(album_image_path, quality=5)
            if advert == False:
                screen.fill(dominant_color)
            else:
                screen.fill((0,0,0))

            # Determine text color based on background color
            text_color = determine_text_color(dominant_color)

            # Update on screen the previous album image
            previous_album_image = pygame.image.load(previous_album_image_path)
            previous_album_image = pygame.transform.scale(previous_album_image, (300, 300))
            if advert == False:
                screen.blit(previous_album_image, (screen_width // 2 - previous_album_image.get_width() // 2 - 200, screen_height // 2 - previous_album_image.get_height() // 2))
            else:
                screen.blit(previous_album_image, (-400,-400))

            # Center the album art on the screen
            screen.blit(album_image, (screen_width // 2 - album_image.get_width() // 2, screen_height // 2 - album_image.get_height() // 2))

            # Render text with the appropriate text color
            track_text = font.render(f"{track_name}", True, text_color)
            artist_text = font.render(f"{artist_name}", True, text_color)
            album_text = font.render(f"{album_name}", True, text_color)
            nowplaying_text = font.render("Now Playing...", True, text_color)

            # Determine the maximum text width among all texts
            max_text_width = max(track_text.get_width(), artist_text.get_width(), album_text.get_width())

            # Center the text horizontally based on the maximum text width
            text_x = screen_width // 2 - max_text_width // 2

            # Determine the vertical position of the text
            text_y = screen_height // 2 + album_image.get_height() // 2 + 20

            screen.blit(track_text, center_text_horizontally(screen, track_text, text_y))
            screen.blit(artist_text, center_text_horizontally(screen, artist_text, text_y + 40))
            screen.blit(album_text, center_text_horizontally(screen, album_text, text_y + 80))
            screen.blit(nowplaying_text,center_text_horizontally(screen, nowplaying_text, text_y - 480))
            screen.blit(watermark_image, (watermark_x, watermark_y))

            pygame.display.update()
        else:
            screen.fill((0,0,0)) #Clear Screen

            no_song_text = font.render("No song playing", True, (255, 255, 255))  # White text
            screen.blit(no_song_text, center_text_horizontally(screen, no_song_text, screen_height // 2))
            screen.blit(watermark_image, (watermark_x, watermark_y))
            pygame.display.flip()

        time.sleep(1)

except KeyboardInterrupt:
    pygame.quit()

# Clean up: Remove the saved album image file
if os.path.exists(album_image_path):
    os.remove(album_image_path)
