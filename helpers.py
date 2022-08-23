import requests
import pandas as pd
import re
from datetime import date
import textwrap
import torch
from statistics import mode
from transformers import AutoTokenizer, AutoModelForSequenceClassification

headers = {'x-rapidapi-host': "seeking-alpha.p.rapidapi.com",
           'x-rapidapi-key': API KEY}

class sentiment_model():

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


    def get_sentiment(self, text, token_size=512):
        '''
        Calculating a single score for the given text and storing result.
        :param text: text to be split and scored on the model.
        :param num: number of token to split into.
        '''

        # Splitting text according to tokens size
        label_list = ['positive', 'negative', 'neutral']
        s = textwrap.wrap(text, token_size)

        # Tokenizing the text and feeding into model to obtain result.
        inputs = self.tokenizer(s, return_tensors="pt", padding=True, truncation=True, max_length=512)
        output = self.model(**inputs)
        results = [label_list[torch.argmax(i)] for i in output[0]]
        return mode(results)


def grab_transcripts(ticker):
    """
    Function that grabs all the metadata for transcripts for selected ticker.
    :param ticker: string of ticker for which you want the transcripts
    :return: returns all earnings call transcripts in date order
    """

    # Setting the base url fot transcripts
    list_url = "https://seeking-alpha.p.rapidapi.com/transcripts/list"
    transcripts = pd.DataFrame(requests.get(list_url, headers=headers,
                                            params={"id": ticker, "until": "0", "size": "20"}).json()['data'])
    if not transcripts.empty:
        # Creating a date index from the nested information.
        transcripts['date'] = [pd.to_datetime(x['publishOn']).replace(tzinfo=None) for x in
                                    transcripts['attributes']]
        transcripts.index = [pd.to_datetime(x['publishOn']).replace(tzinfo=None) for x in
                                  transcripts['attributes']]

    # Selecting only transcript types and selecting titles with Earnings Call in using regex
    transcripts = transcripts[transcripts.type == 'transcript']
    transcripts.attributes = transcripts.attributes.apply(
        lambda i: i if re.findall('(Earning.*Call)', i['title'], flags=re.IGNORECASE) else None)
    transcripts.dropna(subset=['attributes'], inplace=True)
    return transcripts

def select_transcript(transcripts, date=pd.to_datetime(date.today())):
    """
    Function that returns the closest transcript before the selected date.
    :param transcripts: dataframe of all transcript information.
    :param date: date selected. Chooses todays date by default.
    :return: Returns dataframe of latest transcript
    """
    details_url = "https://seeking-alpha.p.rapidapi.com/transcripts/get-details"
    current = transcripts.iloc[transcripts.index.get_loc(date, method='backfill')]
    # Getting the transcript details.
    selected_id = current.id
    selected_transcript = pd.DataFrame(requests.get(details_url, headers=headers,
                                                  params={"id": selected_id}).json()['data']).reset_index()
    return selected_transcript

