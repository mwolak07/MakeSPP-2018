from bs4 import BeautifulSoup
import urllib.request
import datetime


# Gets links to current news headlines
# Pulls from nypost (no javascript to bypass w/ webdriver)
# Identifies the "primary" id, which contains the links.
# Pulls href(link + title) from all subsequent text flags ('a')
# Appends all of this to array for output, cutting initial # symbol and eliminating double links.
def get_news():
    # Requests HTML and stores it in news variable
    news = urllib.request.urlopen("https://nypost.com/news/").read()
    # Creates soup for parsing
    news_soup = BeautifulSoup(news, "lxml")
    body = news_soup.find(id="primary")
    link_list = []

    # Iterates through all 'a' flagged text in primary
    for link in body.find_all('a', href=True):
        string_link = str(link['href'])
        link_list.append(string_link)

    link_list = link_list[1: len(link_list): 2]
    return link_list


# Fetches the weather from forecast.weather.gov
# Finds seven day forecast and locates appropriate data with various soup objects
    # Locates short description from seven-day forecast
    # Adds long description below
# Trims output to fit it in nice block and packages it in an array
def get_weather():
    # Requests HTML from forecast.weather.gov for Englishtown, NJ
    weather_page = urllib.request.urlopen(
        "https://forecast.weather.gov/MapClick.php?lat=40.296&lon=-74.3584#.XFzApFxKg2w").read()
    # Assignment of soup objects for parsing
    weather_page_soup = BeautifulSoup(weather_page, "html.parser")
    seven_day = weather_page_soup.find(id="seven-day-forecast")
    forecasts = seven_day.find_all(class_="tombstone-container")

    # Fetches short description from first "tombstone-container"
    today = forecasts[0]
    short_desc = today.find(class_="short-desc").get_text()

    # High or low randomly reported with different class names, handles this and assigns temp
    if today.find(class_="temp temp-high") is not None:
        temp_type = "temp temp-high"
    else:
        temp_type = "temp temp-low"
    temp = today.find(class_=temp_type).get_text()

    # Fetches title from img
    img = today.find("img")
    description = img["title"]
    # Formatted output
    return [
        short_desc, temp, description[0:111] + "\n" + description[111:222] + "\n" + description[222:len(description)]]


# Gets school event links (calendar) from Manalapan HS website
# Uses "ui-widget app upcomingevents" class to locate the events menu
# Pulls text with links and formats it
# Returns output in array
def get_school_events():
    # Requests HTML from frhsd.com
    hs_link = urllib.request.urlopen("https://www.frhsd.com/manalapan").read()
    # Initializes soup object for parsing
    hs_soup = BeautifulSoup(hs_link, 'lxml')
    # Finds the events section by class
    events_menu = hs_soup.find(class_="ui-widget app upcomingevents")

    link_list = []

    # Finds all text with links in event menu through 'a' and href flags, appending to link_list
    for link in events_menu.find_all('a', href=True):
        string_link = str(link['href'])
        link_list.append(string_link)

    # Appropriately crops each link in the list
    for index in range(len(link_list)):
        link_list[index] = link_list[index][2: len(link_list[index])]

    # Final formatting and return of output
    link_list = link_list[0: len(link_list) - 1]
    return link_list


# Gets current school headlines from Manlapan HS website
# Uses "ui-widget app headlines" class  to find headlines menu
# Pulls text from all 'h1' header labels
# Formats and returns text in array
def get_school_headlines():
    # Requests HTML from frhsd.com
    hs_link = urllib.request.urlopen("https://www.frhsd.com/manalapan").read()
    # Initializes soup object for parsing
    hs_soup = BeautifulSoup(hs_link, 'lxml')
    # Finds headlines menu by class
    headlines = hs_soup.find(class_="ui-widget app headlines")
    things = headlines.find_all('h1')
    headline_list = []
    # Finds correct text and crops it, appending to headline_list
    for index in range(0, 10):
        a = str(things[index].find('span'))
        headline_list.append(a[6: len(a) - 7])

    # Removes blank and returns
    headline_list.remove('')
    return headline_list

# Writes file for java handoff
# file = open("Makespp_Output.txt", "r+")
# file.truncate()
# file.write(str(get_news()) + "\n")
# file.write(str(get_weather()) + "\n")
# file.write(str(get_school_events()) + "\n")
# file.write(str(get_school_headlines()) + "\n")
# file.close()

# Writes to output file with pretty formatting, dumping previous contents
# Title write
file = open("Output.txt", "w+")
file.truncate()
file.write("                                                  Current Info" + "\n")
file.write("\n")
file.write("\n")
file.write("\n")
# Date and time write
file.write("Date and Time:" + "\n")
file.write("\n")
date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
file.write(date_time + "\n")
file.write("\n")
file.write("\n")
file.write("\n")
# Weather write
file.write("Today's Weather:" + "\n")
file.write("\n")
weather_list = get_weather()
for i in range(len(weather_list)):
    file.write(str(weather_list[i]) + "\n")
file.write("\n")
file.write("\n")
file.write("\n")
# News write
file.write("Today's News (links):" + "\n")
file.write("\n")
news_list = get_news()
for i in range(len(news_list)):
    file.write(str(news_list[i]) + "\n")
file.write("\n")
file.write("\n")
file.write("\n")
# School headlines write
file.write("Today's School Headlines:" + "\n")
file.write("\n")
school_headlines_list = get_school_headlines()
for i in range(len(school_headlines_list)):
    file.write(str(school_headlines_list[i]) + "\n")
file.write("\n")
file.write("\n")
file.write("\n")
# School events write
file.write("Today's School Events (calendar links):" + "\n")
file.write("\n")
school_events_list = get_school_events()
for i in range(len(school_events_list)):
    file.write(str(school_events_list[i]) + "\n")
file.close()

# Shows changes were made and process is complete
print("Output file (Output.txt) updated, " + date_time)
