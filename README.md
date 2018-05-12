# Personal-journal-analysis
One of our group members, Jason, has been consistently journaling since the
start of his high school senior year (Sept 2014), producing around
283,000 words (or 350 pages of single-spaced 12 font) of unfiltered
thoughts.

This is a unique source of personal data which we can use to reveal trends
in his life. We are particularly interested in identifying trends that
promote happier writing, which may be correlated to a happier life!

There is a non-trivial amount of processing to be done on the journals
as he has journals for different years in different file types and
formats. He has a single .docx file for 2014, 2015, and 2016; a single
.tex file for 2017; and his 2018 entries have all been in Dropbox
Paper. Each of these different file formats have a different scheme of
formatting journal entries. We need to consider a data structure to
make analysis possible across varying time frames, i.e., weeks,
months, years. At the same time, our data format needs to be
compatible with various natural language processing libraries.

We experimented with [TextBlob](http://textblob.readthedocs.io/en/dev/),
NLTK's [VADER](http://www.nltk.org/howto/sentiment.html), and Stanford's
[CoreNLP](https://stanfordnlp.github.io/CoreNLP/) sentiment analyzers.
We tested all three on a random sample of our journal entries, and found
that VADER was the best at accurately reflecting our protagonist's sentiments.

We also used RNNs and LSTMs via [textgenrnn](https://github.com/minimaxir/textgenrnn) to generate Jason-like entries.
