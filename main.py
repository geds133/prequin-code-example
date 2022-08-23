from bs4 import BeautifulSoup
from helpers import *
from base_logger import logger
import time

# start runtime
start_time = time.time()

if __name__ == '__main__':
    # Parameters required for script
    ticker = input('Please enter ticker of equity: ')
    print('loading sentiment...')

    # Getting the transcript list and selecting the nearest dated transcript
    transcripts = grab_transcripts(ticker)
    transcript = select_transcript(transcripts)

    # Loading in the sentiment model class
    model = sentiment_model()

    # Parsing the text and splitting it into both presentation and Q&A sections.
    transcript_text = ''.join(transcript[transcript['index'] == 'content']['attributes'].values)
    transcript_text = BeautifulSoup(transcript_text, 'html.parser').text
    split_text = transcript_text.split('Question-and-Answer Session')
    presentation = split_text[0]

    # Set Q&A if exists else log that it is not present.
    if not len(split_text) == 1:
        qna = split_text[1]
    else:
        qna = None
        logger.info(f'No Q&A section for {ticker}')

    # Calculating net scores for token_sizes of 512 for presentation and Q&A session
    presentation_sentiment = model.get_sentiment(presentation)
    qna_sentiment = model.get_sentiment(qna)

    # Print the sentiment of the presentation score and Q&N of the document.
    # Net score is % document positive - % document negative
    print('\n')
    print(f'Presentation sentiment: {presentation_sentiment}')
    print(f'Q&A sentiment: {qna_sentiment}')

    logger.info(f"Execution took {round((time.time() - start_time), 2)} seconds")

    print(f'\n')
