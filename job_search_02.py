# import os
# this file simply compiles data concerning where the most jobs per city are
import csv, requests
from lxml import html
filename1, filename2, filename3 = 'search-strings-06.csv', 'largest-cities-01.csv', 'results-largest-cities-01.csv'
city_col, state_col = 1, 2
# https://www.indeed.com/jobs?q=cybersecurity+or+penetration+or+vulnerability&l=
search_q, search_l = 'https://www.indeed.com/jobs?q="', '"&l='
split_word="+"
states = []
with open(filename1) as f1:
    reader = csv.reader(f1)
    # this is creating a header row for a later csv write and has
    # nothing to do with reading csv file
    header_row = []
    header_row.append("State")
    header_row.append("City")
    my_searches = []
    for row in reader:
        # write value to header row for later csv write (will be a column heading)
        header_row.append(row[0])
        # build search string
        temp = search_q + split_word.join( x for x in row[0].split(" ")) + search_l
        # print(temp) # debug line
        my_searches.append(temp)
        my_searches.sort()
    header_row.append("City Total")
    header_row.append("State Total")
    
with open(filename3, "w+") as f3:
    writer = csv.writer(f3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header_row)

    with open(filename2) as f2:
        reader = csv.reader(f2)
        my_locs = []
        for row in reader:
            temp = row[state_col] + ", " + row[city_col]
            my_locs.append(temp)
            my_locs.sort()

    cur_loc = 0
    loc_count = len(my_locs)
    old_state = my_locs[0].split(", ")[0] # initialize the first state
    state_count = 0
    for loc in my_locs:
        cur_loc += 1
        print("Scraping",str(cur_loc),"of",str(loc_count) + ": " + loc + "...")
        current_row = loc.split(", ")
        current_state = loc.split(", ")[0]
        city_count = 0
        for search in my_searches:
            jobs = 0
            try:
                url = str(search + loc)
                page = requests.get(url)
                tree = html.fromstring(page.content)
                # lazy way to see if there are no jobs
                try:
                    #jobs = tree.xpath("//description")
                    jobs = int(tree.xpath("//div[@id='searchCount']/text()")[0].split()[3])
                    # jobs = tree.xpath("//meta[@name='Description']")
                    #jobs = int(tree.xpath(//div[@id="searchCount"]/text()).split(" ")[3])
                except:
                    # do nothing
                    i = 0
        
                # print(url+ ": " + str(jobs)) # debug

            except:
                print("Something went wrong.  Perhaps the page is no longer accepting requests.")
                # add a little pause
                for i in range(0, 100000):
                    i = i
            city_count += jobs
            current_row.append(jobs)

        # if we are still counting results from the same state
        if current_state == old_state:
            state_count += city_count
        # otherwise initialize a new state and write state count to current row
        else:
            state_count = city_count
            old_state = current_state
        current_row.append(city_count)
        current_row.append(state_count)
        writer.writerow(current_row)
