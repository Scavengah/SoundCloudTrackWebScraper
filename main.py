import json
from urllib import request

from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, time

url = "https://soundcloud.com/bissiboi/homemove-prod-mxstxfxr"
page = requests.get(url)
# print(page)
soup = BeautifulSoup(page.content, "html.parser")

# Print the whole HTML document really pretty
# print(soup.prettify())

# Find and print title of sound
titleElement = soup.find("h1", {"itemprop": "name"})
# print(titleElement)
title = titleElement.find("a")
# print(title.string)
titleForFileName = re.sub('[^A-Za-z0-9]+', '', title.string)
# print(titleForFileName)


# Find and print the artist of the sound
by = title.nextSibling
# print(by)
artist = by.nextSibling
print(artist.string)

# Find and print the release date of the audio
releaseDateAndTime = soup.find("time", {"pubdate": ""})
# print(releaseDateAndTime)

# Find and print the description
description = soup.find("img", {"itemprop": "image"}).nextSibling
if description:
    print(description)
else:
    pass

# Find and print genre
genre = soup.find("meta", {"itemprop": "genre"})

if genre:
    genreExtract = genre.get('content')
else:
    genreExtract = "no genre given"

# print(genreExtract)

# Find and print tags
# prints all scripts
script = soup.find_all('script')[9].text.strip()[24:-1]

# load json after formatted
data = json.loads(script)

# find the right object
dataTwo = data[7]

# find tag list item and save it to a variable
tagList = dataTwo['data']['tag_list']

# Find and print the comment section
comments = soup.find("section", {"class": "comments"})
# print(comments.prettify())

# An example of some fine HTML navigation, that i can't use, but just WON't delete
# profile = comments.h2.a.string
# theComment = comments.p.string
# dateOfComment = comments.time.string

# Prints all comments in a nice chronological text format
if comments:
    def extract_comments():
        my_comment_list: list[str] = []
        for commentString in comments.stripped_strings:
            my_comment_list.append(commentString)
        return my_comment_list
else:
    pass


# Convert a list to string using join() function
# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = " " + "\n"
    # return string
    return str1.join(s)


# Saving the list of comments in a variable
if comments:
    s = extract_comments()
    allCommentsInOneString = listToString(s)
else:
    pass
# print(allCommentsInOneString)

# Prints all profiles that has commented
# for profilesAll in comments.find_all(re.compile("^a")):
# print(profilesAll.string)

# Prints all comments that has commented
# for theCommentsAll in comments.find_all(re.compile("^p")):
# print(theCommentsAll.string)

# Prints all dates that has been commented on
# for dateOfCommentsAll in comments.find_all(re.compile("^time")):
# print(dateOfCommentsAll.string)

# Getting current date and time
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S__")
print("Current date & time : ", current_datetime)
# Convert datetime obj to string
str_current_datetime = str(current_datetime)

# Create a file object with name along with extension
file_name = str_current_datetime + artist.string + "_" + titleForFileName + "_" + "soundcloud_info" + ".txt"

# Writing artist and song title to the doc
file = open(file_name, 'w', encoding='utf8')
print("File created : ", file_name)
file.writelines(
    "ARTIST______: " + artist.string + "\n" + "SONG TITLE__: " + title.string + "\n" + "RELEASE DATE: " + releaseDateAndTime.string + "\n" + "URL_________: " + url + "\n" + "GENRE_______: " + genreExtract + "\n" + "TAGS________: " + tagList + "\n" * 3)

# Writing the description to the doc
file = open(file_name, 'a', encoding='utf8')
file.writelines("DESCRIPTION: " + "\n" + description.string + "\n" * 2 + "---" + "\n")

# Writing the most recent comments to the doc
file = open(file_name, 'a+', encoding='utf8')
file.writelines("MOST RECENT COMMENTS FROM EXTRACTION DATE:" + "\n" + allCommentsInOneString)

# This whole thing created to separate the comments
# Creating a variable and storing the text that we want to search for
search_text = "Comment by"
# Creating a variable and storing the text that we want to add
replace_text = "\nComment by:"
# Opening our text file in read only mode using the open() function
with open(file_name, 'r', encoding='utf8') as file:
    # Reading the content of the file using the read() function and storing it in a new variable
    data = file.read()
    # Searching the content and replacing the text using the replace() function
    data = data.replace(search_text, replace_text)
# Opening our text file in write only mode to write the replaced content
with open(file_name, 'w', encoding='utf8') as file:
    # Writing the replaced data in our text file
    file.write(data)
# Printing Text replaced
# print("Text replaced")

file.close()
