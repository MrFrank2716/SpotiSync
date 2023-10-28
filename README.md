# SpotiSync
 A lightweight Spotify player/visualizer built in Python - recommended for low power computers such as Raspberry Pi  to show your Now Playing song and the last listened song!


# Spotify Visualizer

## Introduction

Spotify Visualizer is a Python program that creates a dynamic visual display of the currently playing song on Spotify. It utilizes the Spotify API and various libraries to fetch album art, extract dominant colors, and display song information in a visually appealing manner.

![Screenshot](screenshot.png)

## Features

- Real-time visualization of currently playing songs on Spotify.
- Automatic detection of new songs and advertisement content.
- Display of song title, artist name, album name, and album art.
- Background color adaptation based on the dominant color of the album art.
- Watermark inclusion in the bottom right corner for branding.

## Requirements

- Python 3.x
- Python libraries: `requests`, `spotipy`, `PIL`, `io`, `pygame`, `fast_colorthief`
- Spotify developer account with client ID and client secret.
- A machine with a screen to display the visualization.

## Installation

1. Clone this repository to your local machine:
	git clone https://github.com/your-username/spotify-visualizer.git
2. Install the required Python libraries:
	pip install requests spotipy Pillow pygame colorthief
Set up your Spotify Developer Account and obtain the client ID and client secret.
3. Update the following variables in the script with your Spotify API credentials:
	SPOTIPY_CLIENT_ID = 'your-client-id'
	SPOTIPY_CLIENT_SECRET = 'your-client-secret'

## Usage
1.Run the program using Python:
python main.py
2.The program will display the current song playing on your Spotify account in real-time.
3.You can press the Spacebar key to exit the program.

## Credits
Developed by Frankie Pang.

##License
This project is open-source and available under the MIT License. You are free to use, modify, and distribute it.

##Happy listening and visualizing!