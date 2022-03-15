
# Manga Gallery Manager

A Telegram Bot to download manga from mangasee using [kamyabazad mangasee downloader](https://github.com/kamyabzad/mangasee123-downloader)

This bot is for personal use though you can change it for public use too

<br></br>
 <p align='center'>
  <a href="https://www.python.org/" alt="made-with-python"> <img src="https://img.shields.io/badge/Made%20with-Python-00ead3.svg?style=flat-square&logo=python&logoColor=00ead3&color=00ead3" /> </a>
  <a href="https://github.com/MiyukiKun/Manga_Gallery_Manager/" alt="Maintenance"> <img src="https://img.shields.io/badge/Maintained%3F-Yes-green.svg?style=flat-square&logo=serverless&logoColor=00ead3&color=00ead3" /> </a>
</p>
<br></br>

# Table of Content
- [Manga Gallery Manager](#manga-gallery-manager)
- [Table of Content](#table-of-content)
- [Features](#features)
- [Database Help](#database-help)
  - [How To Set Up Database?](#how-to-set-up-database)
- [Command Details](#command-details)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
  - [Heroku](#heroku)
- [Known Issues](#known-issues)
- [Creator](#creator)

# Features

- Manga Pdfs:- This bot downloads manga in pdf format to make it convenient to read
- Batch Downloads:- download multiple chapters at once
- Manga Tracking:- check updates for added ongoing manga
- Download updates:- Downloads updates for added manga


# Databse help:-
- This bot stores a json file in give telegram channel which stores mangaid and latest chapter (or latest chapter u have read), to use this feature you need to provide [channel id](###extract-channel-id), an [empty json file](###setup) and [message id](###setup)

## How To Setup Database
### Extract Channel ID
- Reccomended to use private channel
- To extract channel id you can copy link of a message in channel, the element after /c/ in link is channel id, for private channel you need to add "-100" before channel id for example if channel id is "27384949" channel id for `CHANNEL_ID` env varible will be "-10027384949"

### Setup
- Upload sample.json given in repository in the channel, copy the link of the file and extract message id (last number of the link) and use it for `DATABASE` env variable

# Command Details
## Get Mangaid
This bot uses mangasee to download chapters so you need to use mangaids mangasee uses which you can extract from thier url

- Note:- Mangaids are case sensitive for example one-piece mangaid is wrong and will throw error One-Piece however is correct

## Command Help

- `/download`:- Downloads given chapter of given mangaid <br />
   use:- /download mangaid:chapter

- `/batch`:- Downloads multiple chapters at once <br />
   use:- /batch mangaid:ch_start:ch_end

- `/add`:- Adds manga in database<br />
   use:- /add mangaid:latest_chapter  

- `/remove`:- Removes manga in database<br />
   use:- /remove mangaid

- `/checkupdates`:- checks updates for added ongoing manga and list them<br />
   use:- /checkupdates

- `/updateall`:- Download updates for all of the manga in database<br />
   use:- /updateall

- `/backup`:- Makes a backup for manga in database<br />
   use:- /backup

- `/restore`:- Restores manga database from give backup file<br />
   use:- /restore replied to the backup file

- `/show`:- Shows Database in telegram messages<br />
   use:- /show


# Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- `API_ID` You Can Get it from [here](https://my.telegram.org/) .

- `API_HASH` You Can Get it form [here](https://my.telegram.org/) .

- `BOT_TOKEN` Search [@BotFather](https://t.me/botfather) in telegram.

- `CHANNEL_ID` public/private channel id to store database (mangaid and updated chapters) within channel

- `DATABSE` a dummy message id of a message for database

# Deployment 

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/gautam8404/Anime_news_bot)

# Known Issues

- Crashes for few manga 
  
# Creator

- [Gautam8404](https://github.com/Gautam8404)
