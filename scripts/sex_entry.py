import csv
import webbrowser
import urllib.parse
import os


TEMPFILE = 'temp.csv'
WRITEFILE = 'top_artists.csv'
entry_complete = True
artist_to_sex = {}

os.chdir('../data')

# Data entry helper script
def search_url(query):
    url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
    webbrowser.open(url)

with open(WRITEFILE) as csvfile:
    reader = csv.reader(csvfile)

    with open(TEMPFILE, 'w') as tempfile:
        writer = csv.writer(tempfile)
        entering = True

        for row, data in enumerate(reader):
            artist, sex = data
 
            if not sex and entering:
                print(artist, sex)
                search_url(f"{artist} music artist")
                while True:
                    command = input()
                    if command in 'mfug':
                        sex = command.upper()
                        break
                    elif command == "s":
                        search_url(f"{artist} spotify")
                    elif command == "q":
                        entering = False
                        entry_complete = False
                        break
                    else:
                        print(f"not a valid command: {command}")

            artist_to_sex[artist] = sex
            writer.writerow([artist, sex])

os.replace(TEMPFILE, WRITEFILE)


# Write data to csv after entry is complete
WRITEFILE = 'country_artists.csv'

if entry_complete:
    with open(WRITEFILE) as csvfile:
        reader = csv.reader(csvfile)

        with open(TEMPFILE, 'w') as tempfile:
            writer = csv.writer(tempfile)

            for row, data in enumerate(reader):
                if row == 0:
                    writer.writerow(data)
                    continue

                country, _, gdp, artists = data
                ratios = []
                male, female, unknown, group = 0, 0, 0, 0
                for artist in eval(artists):
                    match artist_to_sex[artist]:
                        case 'M':
                            male += 1
                        case 'F':
                            female += 1
                        case 'U':
                            unknown += 1
                        case 'G':
                            group += 1
                total = male + female + unknown + group
                ratios = list(map(lambda x:x/total, [male, female, unknown, group]))

                writer.writerow([country, ratios, gdp, artists])

os.replace(TEMPFILE, WRITEFILE)
