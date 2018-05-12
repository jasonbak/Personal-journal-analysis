import process
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import time
from collections import Counter

def plotLineGraph(title, x_label, y_label, x_vals, y_vals, x_ticks=None, marker=True):
    # Fit graph to my 13 inch MacBook Pro screen
    plt.figure(figsize=(11,7))

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True, which="both")
    # Make x_labels vertical
    if x_ticks != None:
        plt.xticks(x_vals, x_ticks, rotation='vertical')
    if marker == True:
        plt.plot(x_vals, y_vals, marker='o')
    else:
        plt.plot(x_vals, y_vals)

    # Draw and show graph for 5 seconds
    plt.draw()
    plt.pause(5)
###############################################################################

def getAllEntriesStr(all_entries):
    """Construct a string of all the entries

    """
    all_entries_str = ''
    for year in all_entries:
        for month in year:
            for day in month:
                for entry in day[1]:
                    all_entries_str += (entry + '\n')
    return all_entries_str

def getEntriesOfYearStr(year):
    """Construct a string of all entries from a year

    """
    entries_of_year_str = ''
    for month in year:
        for day in month:
            for entry in day[1]:
                entries_of_year_str += (entry + '\n')
    return entries_of_year_str

def getEntriesOfMonthStr(month):
    """Construct a string of all entries from a month

    """
    entries_of_month_str = ''
    for day in month:
        for entry in day[1]:
            entries_of_month_str += (entry + '\n')
    return entries_of_month_str

def getEntriesOfDayStr(day):
    """Construct a string of all entries from a day

    """
    entries_of_day_str = ''
    for entry in day[1]:
        entries_of_day_str += (entry + '\n')
    return entries_of_day_str

###############################################################################

###############################################################################
###############################   SENTIMENT   #################################

def reportOverallSentiment(all_entries):
    """Prints overall sentiment

    Args:
        all_entries (4d list of tuples):
                        1d - (day of month, entries from a day)
                        2d - days
                        3d - months
                        4d - years

    Returns:
        None
    """
    # Condense entries over all the years into one string
    all_entries_str = getAllEntriesStr(all_entries)

    # TODO: Commented out code runs slower, but may be more accurate
    # sid = SentimentIntensityAnalyzer()
    # ss = sid.polarity_scores(entries_of_year_str)
    # overall_sentiment = ss['pos']

    entire_journal = TextBlob(all_entries_str)
    overall_sentiment = entire_journal.sentiment
    print('Overall: ' + str(overall_sentiment))

def reportYearlySentiments(all_entries):
    """Plot Polarity vs. Year line graph

    Args:
        all_entries (4d list of tuples):
                        1d - (day of month, entries from a day)
                        2d - days
                        3d - months
                        4d - years

    Returns:
        None
    """
    # For line graph
    x_vals, y_vals = [], []

    sid = SentimentIntensityAnalyzer()
    cur_year = 2014

    for year in all_entries:
        # Condense entries over all a year into one string
        entries_of_year_str = getEntriesOfYearStr(year)

        tb = TextBlob(entries_of_year_str)
        y_vals.append(tb.polarity)
        x_vals.append(cur_year)
        cur_year += 1

        # TODO: Commented out code runs slower, but may be more accurate
        # ss = sid.polarity_scores(entries_of_year_str)
        # # Build up y variables
        # y_vals.append(ss['pos'])

    plotLineGraph('Polarity by year', 'Year', 'Polarity', x_vals ,y_vals)

def reportMonthlySentiments(all_entries):
    """Plot Polarity vs. Month line graph

    Args:
        all_entries (4d list of tuples):
                        1d - (day of month, entries from a day)
                        2d - days
                        3d - months
                        4d - years

    Returns:
        None
    """
    # For line graph
    # If we use a list of strings as x_vals, then we will incorredctly plot in
    # alphabetical order
    x_ticks = []
    y_vals = []

    sid = SentimentIntensityAnalyzer()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
    cur_year = 14

    print(len(all_entries))
    for year in all_entries:
        # Start of a new year
        # Journal starts on the 8th month in 2014
        cur_month_idx = 0 if cur_year != 14 else 8
        for month in year:
            # Build up x variables
            x_ticks.append(months[cur_month_idx] + '-' + str(cur_year))
            entries_of_month_str = getEntriesOfMonthStr(month)

            tb = TextBlob(entries_of_month_str)
            y_vals.append(tb.polarity)

            # TODO: Commented out code runs slower, but may be more accurate
            # ss = sid.polarity_scores(entries_of_month_str)
            # # Build up y variables
            # y.append(ss['pos'])

            cur_month_idx += 1
        cur_year += 1

    x_vals = [i for i in range(len(y_vals))]
    # Plot Year vs. Polarity line graph
    plotLineGraph('Polarity by month', 'Month', 'Polarity', x_vals, y_vals, x_ticks=x_ticks)

def reportTop5Sentiments(all_entries):
    """Print entries of top 5 daily sentiments.

    Args:
        all_entries (4d list of tuples):
                        1d - (day of month, entries from a day)
                        2d - days
                        3d - months
                        4d - years

    Returns:
        None
    """
    top_vals = []
    top_dates = []
    top_entries = []

    sid = SentimentIntensityAnalyzer()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
    cur_year = 2014

    for year in all_entries:
        # Start of a new year
        # Journal starts on the 8th month in 2014
        cur_month_idx = 0 if cur_year != 14 else 8
        for month in year:
            cur_day = 1
            # Append all entries from a month into one string
            for day in month:
                entries_of_day_str = getEntriesOfDayStr(day)
                ss = sid.polarity_scores(entries_of_day_str)
                sentiment_of_day = ss['pos']

                # Build up top 5
                if len(top_vals) < 5:
                    top_vals.append(sentiment_of_day)
                    cur_date = months[cur_month_idx] + ' ' \
                            + str(cur_day) + ', ' + str(cur_year)
                    top_dates.append(cur_date)
                    top_entries.append(entries_of_day_str)
                elif min(top_vals) < sentiment_of_day:
                    min_idx = top_vals.index(min(top_vals))

                    top_vals[min_idx] = sentiment_of_day
                    cur_date = months[cur_month_idx] + ' ' \
                            + str(cur_day) + ', ' + str(cur_year)
                    top_dates[min_idx] = cur_date
                    top_entries[min_idx] = entries_of_day_str

                cur_day += 1
            cur_month_idx += 1
        cur_year += 1

    for i in range(len(top_vals)):
        print(top_dates[i] + ': ' + str(top_vals[i]))
        print((top_entries[i]))

def reportPosNegSentiments(all_entries):
    """Graph line graph of positive, negative, and neural sentiments per entry

    Args:
        all_entries (4d list of tuples):
                        1d - (day of month, entries from a day)
                        2d - days
                        3d - months
                        4d - years

    Returns:
        None
    """
    x_labels = []

    pos_count = 0
    neg_count = 0
    neu_count = 0
    pos = []
    neg = []
    neu = []
    sid = SentimentIntensityAnalyzer()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
    cur_year = 14
    for year in all_entries:
        # Start of a new year
        if cur_year == 14:
            cur_month_idx = 8
        else:
            cur_month_idx = 0
        for month in year:
            # Build up x variables
            x_labels.append(months[cur_month_idx] + '-' + str(cur_year))
            entries_of_month_str = ''
            for day in month:
                for entry in day[1]:
                    entries_of_month_str += (entry + '\n')
            for word in entries_of_month_str.split():
                ss = sid.polarity_scores(word)
                if ss['pos'] == 1.0:
                    pos_count += 1
                elif ss['neg'] == 1.0:
                    neg_count += 1
                elif ss['neu'] == 1.0:
                    neu_count += 1
            pos.append(pos_count)
            neg.append(neg_count)
            neu.append(neu_count)
            cur_month_idx += 1
        cur_year += 1

    # Plot All sentiment types per month line graph
    x = [i for i in range(len(pos))]
    plt.figure(figsize=(11,7))
    plt.title('All sentiment types per month')
    plt.plot(x, pos, 'g')
    plt.plot(x, neg, 'r')
    plt.plot(x, neu, 'b')
    plt.xticks(x, x_labels, rotation='vertical')
    plt.ylabel('Count')
    plt.xlabel('Month')
    plt.draw() # draw the plot
    plt.pause(5) # show it for 5 seconds

def reportSentiments(all_entries):
    """Reports sentiment values for different time periods

    Args:
        all_entries (4d list of strings): 4d list of entries

    Returns:
        None
    """
    # reportOverallSentiment(all_entries)
    # reportYearlySentiments(all_entries)
    reportMonthlySentiments(all_entries)
    # reportTop5Sentiments(all_entries)
    # reportPosNegSentiments(all_entries)

###############################   SENTIMENT   #################################
###############################################################################

###############################################################################
###############################   FREQUENCY   #################################
def getSortedFreqs(journal_entries, all_words):
    # Map word to their frequencies
    freq = {}
    for word in all_words:
        freq[word] = freq[word]+1 if word in freq else 1

    length = len(all_words)

    sorted_freqs = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return sorted_freqs

def reportOverallNounFrequencies(all_entries):
    all_entries_str = getAllEntriesStr(all_entries)
    entire_journal = TextBlob(all_entries_str)

    # This line takes 20 minutes to run :(
    all_words = entire_journal.noun_phrases

    sorted_freqs = getSortedFreqs(entire_journal, all_words)
    words, scores = zip(*sorted_freqs)
    # # Report overall noun frequencies
    # for i in range(0,50):
        # print(words[i], scores[i])

def reportIncreasedFrequencies(all_entries):
    # TODO: Wrok on this function
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
    all_monthly_freqs = []

    for year in all_entries:
        for month in year:
            # Append all entries from a month into one string
            entries_of_month_str = ''
            for day in month:
                for entry in day[1]:
                    entries_of_month_str += (entry + '\n')
            journal_of_month = TextBlob(entries_of_month_str)
            all_words = journal_of_month.words

            sorted_freqs = getSortedFreqs(journal_of_month, all_words)
            all_monthly_freqs.append(sorted_freqs)

    top_increases = []

def reportNounFrequencies(all_entries):
    """Reports word frequencies for different time periods

    Args:
        all_entries (4d list of strings): 4d list of entries
    """
    reportOverallNounFrequencies(all_entries)
    # reportIncreasedFrequencies(all_entries)

###############################   FREQUENCY   #################################
###############################################################################

###############################################################################
##############################   WORD COUNTS   ################################

def reportYearlyWordCounts(all_entries):
    # For line graph
    x_vals = ['2014', '2015', '2016', '2017', '2018']
    y_vals = []

    cur_year = 2014
    for year in all_entries:
        entries_of_year_str = getEntriesOfYearStr(year)
        # Build up y variables
        y_vals.append(len(entries_of_year_str.split()))
        cur_year += 1


    # Plot Year vs. Word count line graph
    title = 'Word count by year'
    x_label = 'Year'
    y_label = 'Word count'
    plotLineGraph(title, x_label, y_label, x_vals, y_vals)

def reportMonthlyWordCounts(all_entries):
    # For line graph
    x_ticks = []
    y_vals = []

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
    cur_year = 14
    for year in all_entries:
        # Start of a new year
        if cur_year == 14:
            cur_month_idx = 8
        else:
            cur_month_idx = 0
        for month in year:
            # Build up x variables
            x_ticks.append(months[cur_month_idx] + '-' + str(cur_year))
            entries_of_month_str = getEntriesOfMonthStr(month)

            # Build up y variables
            y_vals.append(len(entries_of_month_str.split()))
            cur_month_idx += 1
        cur_year += 1

    # Plot Month vs. Word count line graph
    title = 'Word count by month'
    x_label = 'Month'
    y_label = 'Word count'
    x_vals = [i for i in range(len(y_vals))]
    plotLineGraph(title, x_label, y_label, x_vals, y_vals, x_ticks=x_ticks)

def reportDailyWordCounts(all_entries):
    # For line graph
    y_vals = []

    for year in all_entries:
        for month in year:
            for day in month:
                entries_of_day_str = getEntriesOfDayStr(day)
                # Build up y variables
                y_vals.append(len(entries_of_day_str.split()))

    # Plot Day vs Word count line graph
    x_vals = [i for i in range(len(y_vals))]
    title = 'Word count by day'
    x_label = 'Day'
    y_label = 'Word count'
    plotLineGraph(title, x_label, y_label, x_vals, y_vals, marker=False)

def reportTop10WordCounts(all_entries):
    top_vals = []
    top_dates = []
    top_entries = []

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
    cur_year = 14

    for year in all_entries:
        # Start of a new year
        if cur_year == 14:
            cur_month_idx = 8
        else:
            cur_month_idx = 0
        for month in year:
            cur_day = 1
            for day in month:
                entries_of_day_str = getEntriesOfDayStr(day)
                wc_of_day = len(entries_of_day_str.split())

                # Build up top 5
                if len(top_vals) < 10:
                    top_vals.append(wc_of_day)
                    cur_date = months[cur_month_idx] + ' ' \
                            + str(cur_day) + ', ' + str(cur_year)
                    top_dates.append(cur_date)
                    top_entries.append(entries_of_day_str)
                elif min(top_vals) < wc_of_day:
                    min_idx = top_vals.index(min(top_vals))

                    top_vals[min_idx] = wc_of_day
                    cur_date = months[cur_month_idx] + ' ' \
                            + str(cur_day) + ', ' + str(cur_year)
                    top_dates[min_idx] = cur_date
                    top_entries[min_idx] = entries_of_day_str

                cur_day += 1
            cur_month_idx += 1
        cur_year += 1

    # for i in range(len(top_vals)):
        # print(top_dates[i] + ': ' + str(top_vals[i]))
        # print((top_entries[i]))
    # Plot Word count vs. entry date bar graph
    plt.figure(figsize=(11,7))

    plt.title('Top 10 word count entries')
    plt.xlabel('Dates')
    plt.ylabel('Word count')
    plt.xticks(rotation='vertical')
    plt.bar(top_dates, top_vals)
    plt.draw() # draw the plot
    plt.pause(5) # show it for 5 seconds

def getWordCounts(all_entries):
    word_counts = []
    for year in all_entries:
        for month in year:
            for day in month:
                entries_of_day_str = getEntriesOfDayStr(day)
                # Build up word_counts variables
                word_counts.append(len(entries_of_day_str.split()))
    return word_counts

def getMaxSum(word_counts, window_len):
    max_sum = 0
    max_sum_idx = 0
    # TODO: If you keep it in your code, optimize it so it's O(n) time by
    # subtracting and adding to cur_sum
    for i in range(0,len(word_counts) - window_len):
        start = i
        end = i + window_len
        cur_sum = sum(word_counts[start:end])
        if cur_sum > max_sum:
            max_sum = cur_sum
            max_sum_idx = i
    return max_sum_idx

def reportMaxWeekWordCounts(word_counts):
    start_of_month_idx = getMaxSum(word_counts, 7)
    return start_of_week_idx

def reportMaxMontWordCounts(word_counts):
    start_of_month_idx = getMaxSum(word_counts, 30)
    return start_of_month_id

def reportWordCounts(all_entries):
    """Reports word counts for different time periods

    Args:
        all_entries (4d list of strings): 4d list of entries

    Returns:
        None
    """
    # reportYearlyWordCounts(all_entries)
    # reportMonthlyWordCounts(all_entries)
    # reportDailyWordCounts(all_entries)
    reportTop10WordCounts(all_entries)
    # word_counts = getWordCounts(all_entries)
    # reportMaxWeekWordCounts(word_counts)
    # reportMaxMontWordCounts(word_counts)

##############################   WORD COUNTS   ################################
###############################################################################


def getPopularWords(all_titles):
    num_popular_words = 30
    titles = []
    for year in all_titles:
        for month in year:
            for day in month:
                titles.extend(day.split())
    counts = Counter(titles)
    return counts.most_common()[:num_popular_words]

def reportPopularTitleWords(all_titles):
    popular_words = getPopularWords(all_titles)
    x_ticks = [word[0] for word in popular_words]
    x = [i for i in range(len(popular_words))]
    y = [word[1] for word in popular_words]
    # Plot Year vs. Polarity line graph
    plt.figure(figsize=(11,7))
    plt.title('Top 30 words used in entry titles')
    plt.bar(x, y)
    plt.ylabel('Frequency')
    plt.xlabel('Top 30 words')
    plt.xticks(x, x_ticks, rotation=45, fontsize=6)
    plt.draw() # draw the plot
    plt.pause(5) # show it for 5 seconds

def reportTopFrequencies(all_entries):
    # Append all entries into one string
    all_entries_str = ''
    for year in all_entries:
        for month in year:
            for day in month:
                for entry in day[1]:
                    all_entries_str += (entry + '\n')
    entire_journal = TextBlob(all_entries_str)

    all_words = entire_journal.words

    # Ignore stop words, so top frequencies more interesting
    stop = set(stopwords.words('english'))
    non_stop_words = [w.lower() for w in all_words if not w.lower() in stop]

    sorted_freqs = getSortedFreqs(entire_journal, non_stop_words)
    words, scores = zip(*sorted_freqs)
    # Report overall noun frequencies
    for i in range(0,50):
        print(words[i], scores[i])

def test(all_entries):
    # For line graph
    x_labels = []
    y = []

    sid = SentimentIntensityAnalyzer()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
    cur_year = 14
    for year in all_entries:
        # Start of a new year
        if cur_year == 14:
            cur_month_idx = 8
        else:
            cur_month_idx = 0
        for month in year:
            # Build up x variables
            x_labels.append(months[cur_month_idx] + '-' + str(cur_year))
            # Append all entries from a month into one string
            entries_of_month_str = ''
            for day in month:
                for entry in day[1]:
                    entries_of_month_str += (entry + '\n')

            ss = sid.polarity_scores(entries_of_month_str)
            # Build up y variables
            y.append(ss['pos'])
            cur_month_idx += 1
        cur_year += 1

    # Plot Year vs. Polarity line graph
    x = [i for i in range(len(y))]
    plt.figure(figsize=(11,7))
    plt.title('Polarity by month')
    plt.xticks(x, x_labels, rotation='vertical')
    plt.plot(x,y,marker='o')
    plt.ylabel('Polarity')
    plt.xlabel('Month')
    plt.draw() # draw the plot
    plt.pause(5) # show it for 5 seconds

def reportTopNames(all_entries):
    # Append all entries into one string
    all_entries_str = ''
    for year in all_entries:
        for month in year:
            for day in month:
                for entry in day[1]:
                    all_entries_str += (entry + '\n')
    entire_journal = TextBlob(all_entries_str)

    all_words = entire_journal.words

    # Ignore stop words, so top frequencies more interesting
    with open('names.txt') as f:
        stop = f.read().splitlines()
    non_stop_words = [w.lower() for w in all_words if w.upper() in stop]

    sorted_freqs = getSortedFreqs(entire_journal, non_stop_words)
    words, scores = zip(*sorted_freqs)
    # Report overall noun frequencies
    for i in range(0,50):
        print(words[i], scores[i])

###############################################################################
##################################   MAIN   ###################################
def main():
    # 4d list of entries
    all_entries, all_titles = process.processJournals()

    reportSentiments(all_entries)
    # reportNounFrequencies(all_entries)
    # reportWordCounts(all_entries)
    # reportPopularTitleWords(all_titles)
    # reportTopFrequencies(all_entries)
    # reportTopNames(all_entries)

if __name__ == '__main__':
    main()

##################################   MAIN   ###################################
###############################################################################
