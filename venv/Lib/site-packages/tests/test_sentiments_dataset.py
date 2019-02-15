# -*- coding: utf-8 -*-
import pytest
import pandas as pd
from anacode.agg import aggregation as agg


@pytest.fixture
def frame_sentiments():
    header = ['doc_id', 'text_order', 'sentiment_value']
    sentiments = pd.DataFrame([
        [0, 0, 0.5],
        [0, 1, -0.5],
        [0, 2, 0.5],
        [1, 0, -1.0],
        [2, 0, 1.0],
        [2, 1, 0.5],
        [2, 2, -0.5],
        [2, 3, -0.5],
    ], columns=header)
    return {'sentiments': sentiments}


@pytest.fixture
def dataset(frame_sentiments):
    return agg.SentimentDataset(**frame_sentiments)


def test_empty_dataset_failure():
    dataset = agg.SentimentDataset(None)
    with pytest.raises(agg.NoRelevantData):
        dataset.average_sentiment()


def test_average_sentiment(dataset):
    assert dataset.average_sentiment() == 0.0
