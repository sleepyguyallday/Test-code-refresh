# Discord bot token

token = "NTM0OTg3NjE2ODg2NTg3NDE0.DyF3DQ.v6jOuxTo9PFeEGS3nhVhT9X8nH0"

# Testing if the other options for Youtube Downloader will work as based on Svenbot discord music bot

ydl_opts = {
	"default_search": "auto",
	"format": "bestaudio/best",
	"postprocessors": [{'key': 'FFmpegExtractAudio', 
	'preferredcodec': 'mp3', 
	'preferredquality': '192'},
	{'key': 'FFmpegMetadata'}],
	"extractaudio": True,
	"nocheckcertificate": True,
	"ignoreerrors": True,
	"no_warnings": True,
	"verbose": False,
	"quiet": True,
	"forcetitle": True,
	"forceurl": True,
	"skip_download": True,
	"noplaylist": True
}


# Arguments added to the YouTube Downloader/player, giving
# some time for the player to catch up and reconnect to the 
# media

before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"