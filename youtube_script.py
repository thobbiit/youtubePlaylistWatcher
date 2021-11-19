# import module
from googleapiclient.discovery import build
import json
import sys
import time
import logging
import requests
import os
from datetime import datetime

youtubeDLDomain = "https://" + os.environ['youtubeDLDomain'] + "/add"
youtubeAPIKey = os.environ['youtubeAPIKey']
playlistId = os.environ['playlistId']
alreadyDownloadedCount = os.environ['alreadyDownloaded']

def playlist_video_links(playlistId, VideosCount):
	
	# creating youtube resource object
	youtube = build('youtube','v3',developerKey=youtubeAPIKey)


	# retrieve youtube video results
	pl_request = youtube.playlistItems().list(
		part="contentDetails",
		playlistId=playlistId,
		)
	pl_response = pl_request.execute()
	newCount = pl_response['pageInfo']['totalResults']


	# is there a new item?
	if newCount > VideosCount:
		download_new_video(newCount, pl_response['items'][VideosCount]['contentDetails']['videoId'])
	else:
		logging.warning(str(datetime.now()) + "; allready up to date")
		time.sleep(7200)
			
def download_new_video(playlistNumber, videoId):
	link = 'https://www.youtube.com/watch?v=' + videoId
	newCount = downloadedVideosCount + 1
	

	with open("DownloadCount.txt", "a+") as file:
		file.write("\n"+str(newCount))

	post = requests.post(youtubeDLDomain, json={"url":link, "quality":"best", "format":"MP4"})

	if post.status_code == 200:
		logging.warning(str(datetime.now()) + "; SUCCESS; downloading video: " + link)
	else:
		logging.error(str(datetime.now()) + "; " + str(post.status_code) + ": Send to metube failed: " + link)


while 1:
	downloadedVideosCount = 0
	with open("DownloadCount.txt", "a+") as file:
	
		file.seek(0)
		line = file.readlines()
		if len(line) == 0:
			file.write(alreadyDownloadedCount)
		else: 
			downloadedVideosCount = int(line[-1])

	playlist_video_links(playlistId, downloadedVideosCount)




