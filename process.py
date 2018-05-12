import re
import string

def replaceEmojis(line):
    line = line.replace('🙂', ':)')
    line = line.replace('😞', ':(')
    line = line.replace('😢', ":'(")
    line = line.replace('😄', ':D')
    return line


def processTXT(raw_txt):
    """Process a raw string (read from a .txt file) of all journal entries from
    one year into a 3d list of tuples, described as (day of month, entries from
    a day).

    Args:
        raw_txt (string): raw string of entries from a year read from a .txt
            file

    Returns
        (3d list of tuples):
            1d - (day of month, entries from a day)
            2d - days
            3d - months
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
    # Regex to find the first entry of a day
    new_day_pattern = re.compile('^[0-9]?[0-9]:')
    # Split all raw entries by \n
    split_entries = raw_txt.splitlines()

    prev_day_of_month = 0

    entries_of_year = []
    entries_of_month = []
    entries_of_day = []
    for line in split_entries:
        if line in months:
            if entries_of_month != []:
                # Nothing in entries_of_month before first entry of new year
                # New month; add entries for the previous day and month
                entries_of_month.append((prev_day_of_month, entries_of_day))
                entries_of_year.append(entries_of_month)

                prev_day_of_month = 0
                entries_of_day = []
                entries_of_month = []
        else:
            # Every entry starts with or without '-'
            entry = line[line.find('-')+1:]

            if new_day_pattern.search(line) != None:
                # First entry of the day

                if entries_of_day != []:
                    # Nothing in entries_of_day on first entry of new month
                    # Add entries for the previous day
                    entries_of_month.append((prev_day_of_month, entries_of_day))

                # Day of month ends with a ':'
                cur_day_of_month = int(line[:line.find(':')])

                # Handle days without any entries
                for missing_day in range(prev_day_of_month+1, cur_day_of_month):
                    entries_of_month.append((missing_day, []))

                entries_of_day = [entry]
                prev_day_of_month = cur_day_of_month
            else:
                entries_of_day.append(entry)

    # Add entries for last day and month of the year
    entries_of_month.append((prev_day_of_month, entries_of_day))
    entries_of_year.append(entries_of_month)

    return entries_of_year

def processTEX(raw_tex):
    """Process a raw string (read from a .tex file) of all journal entries from
    2017 into a 3d list of tuples, described as (day of month, entries from a
    day).

    Args:
        raw_tex (string): raw string of entries from a year read from a .tex
            file

    Returns
        (3d list of tuples):
            1d - (day of month, entries from a day)
            2d - days
            3d - months
    """
    # Ignore all the LaTeX set-up
    start_idx = raw_tex.find('\section{January}')
    end_idx = raw_tex.find('\end{document}')
    usable_str = raw_tex[start_idx:end_idx]
    # Split all entries by \n
    split_entries = usable_str.splitlines()

    day_of_month = 1
    title = ''

    titles_of_year = []
    titles_of_month = []

    entries_of_year = []
    entries_of_month = []
    entries_of_day = []
    for line in split_entries:
        if '\section' in line:
            if entries_of_month != []:
                # Nothing in entries_of_month before the entry of new year
                # New month; add entries for the previous day and month
                entries_of_month.append((day_of_month, entries_of_day))
                entries_of_year.append(entries_of_month)

                # add titles for previous month
                titles_of_year.append(titles_of_month)

                day_of_month = 1
                title = ''
                entries_of_day = []
                entries_of_month = []
                titles_of_month = []
        elif '\subsection' in line:
            if entries_of_day != []:
                # Nothing in entries_of_day on first entry of new month
                # Add entries for the previous day
                entries_of_month.append((day_of_month, entries_of_day))
                entries_of_day = []

            # Add title of day
            start_idx = len('\subsection{')
            end_idx = len(line) - 1
            title = line[start_idx:end_idx]
            titles_of_month.append(title)

            day_of_month += 1
        elif not ('%' in line and '\%' not in line):
            if line != '' or (line == '' and title == 'N/A'):
                # Fill in missing entries with ''
                # Ignore comment-only lines
                entries_of_day.append(line)

    # Add entries for last day and month of the year
    entries_of_month.append((day_of_month, entries_of_day))
    entries_of_year.append(entries_of_month)
    # Add titles for the last month of the year
    titles_of_year.append(titles_of_month)

    return entries_of_year, titles_of_year

def processMD(raw_md):
    """Process a raw string (read from a .md file) of all journal entries from
    2018 into a 3d list of tuples, described as (day of month, entries from a
    day).

    Args:
        raw_md (string): raw string of entries from a year
            read from a .md file

    Returns
        (3d list of tuples):
            1d - (day of month, entries from a day)
            2d - days
            3d - months
    """
    months = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31,
            'June':30, 'July':31, 'August':31, 'September':30, 'October':31,
            'November':30, 'December':31}
    new_month = '# '
    new_day = '## **'
    # Split all raw entries by \n
    split_entries = raw_md.splitlines()

    last_day_recorded = 1

    titles_of_year = []
    titles_of_month = []

    entries_of_year = []
    entries_of_month = []
    entries_of_day = []
    for line in split_entries:
        # NOTE: Change remove line below if you use another classifier that
        # handles emojis
        # NTLK Vader doesn't consider emojis, but it does consider emoticons
        line = replaceEmojis(line)
        if line[:len(new_month)] == new_month and entries_of_month != []:
            month = line[len(new_month):]
            # Nothing in entries_of_month when we start processing the year
            # New month; add entries for the last day recorded and prev month
            entries_of_month.append((cur_day_of_month, entries_of_day))
            # Recorded entries in a month in reverse chronological order
            entries_of_year.append(entries_of_month[::-1])

            # Add titles for the previous month
            titles_of_year.append(titles_of_month)

            last_day_recorded = months[month]
            entries_of_day = []
            entries_of_month = []
            titles_of_month = []
        elif line[:len(new_day)] == new_day:
            # New day; on the title for entry
            if entries_of_day != []:
                # Add entries for the previous day
                entries_of_month.append((cur_day_of_month, entries_of_day))

            day_idx = line.find(':')
            cur_day_of_month = int(line[len(new_day):day_idx])

            # Handle days without any entries
            for missing_day in range(last_day_recorded-1, cur_day_of_month, -1):
                entries_of_month.append((missing_day, []))
                titles_of_month.append('N/A')

            title_idx = day_idx + len('**')
            title = line[title_idx:-len('**')]
            titles_of_month.append(title)

            entries_of_day = []
            last_day_recorded = cur_day_of_month
        elif line != '' and line[0] in string.ascii_letters+string.digits:
            # Entries only start with an alphanumeric character
            entries_of_day.append(line)

    # Add entries for last day and month of the year
    entries_of_month.append((cur_day_of_month, entries_of_day))
    # Recorded entries in a month in reverse chronological order
    entries_of_year.append(entries_of_month[::-1])

    return entries_of_year[::-1], titles_of_year[::-1]

def processJournals():
    """Retrieve individual entries from 2014, 2015, and 2016 .txt files; 2017
    LaTeX file; and 2018 .md file. Populate a 4d list of entries and titles in
    chronological order.

    Args:
        None

    Returns
        (4d list of tuples):
            1d - (day of month, entries from a day)
            2d - days
            3d - months
            4d - years
        (4d list of strings):
            1d - title for the day
            2d - days
            3d - months
            4d - years
    """
    journal_2014 = 'data/2014.txt'
    journal_2015 = 'data/2015.txt'
    # journal_2016 = 'data/2016.txt'
    # journal_2017 = 'data/2017.tex'
    # journal_2018 = 'data/2018.md'

    all_entries = []
    all_titles = []



    # TODO: Remove this block of code when using real data set
    title_2014 = [['nothing'], ['in', 'here', 'because', 'of', 'pruned', 'data']]
    title_2015 = [['rip', ':(']]
    all_titles.append(title_2014)
    all_titles.append(title_2015)
    # Default mode == 'r'
    with open(journal_2014) as f14, open(journal_2015) as f15:
        # Process .txt files from 2014, 2015
        raw_txt_entries_of_years = f14.read(), f15.read()
        for raw_txt_entries_of_year in raw_txt_entries_of_years:
            # Gets 3d list of entries
            entries_year = processTXT(raw_txt_entries_of_year)
            all_entries.append(entries_year)




    # with open(journal_2014) as f14, open(journal_2015) as f15, \
            # open(journal_2016) as f16, open(journal_2017) as f17, \
            # open(journal_2018) as f18:
        # # Process .txt files from 2014, 2015, and 2016
        # raw_txt_entries_of_years = f14.read(), f15.read(), f16.read()

        # for raw_txt_entries_of_year in raw_txt_entries_of_years:
            # # Gets 3d list of entries
            # entries_year = processTXT(raw_txt_entries_of_year)
            # all_entries.append(entries_year)

        # # Process .tex file from 2017
        # entries_2017, titles_2017 = processTEX(f17.read())
        # all_entries.append(entries_2017)
        # all_titles.append(titles_2017)

        # # Process .md file from 2018
        # entries_2018, titles_2018 = processMD(f18.read())
        # all_entries.append(entries_2018)
        # all_titles.append(titles_2018)

    return all_entries, all_titles
