### Earnings Call transcript sentiment
The purpose of the script is to classify the sentiment of a company's latest quarterly earnings call transcript. This is done by classifying the presentation section and the question and answer section of the transcript separately to give a positive, neutral and negative sentiment.

# How to run
Firstly please install the requirements through:
`pip install -r requirements.txt`

Please run main.py from the command line with:
`python main.py`

When prompted please enter your required ticker.

For an API KEY there is a free tier available from :
https://rapidapi.com/apidojo/api/seeking-alpha/pricing
- Please replace API KEY (line 11) in headers from helper.py file.

# Logging
A logger file will also be populated in the working directory with the execution time.
