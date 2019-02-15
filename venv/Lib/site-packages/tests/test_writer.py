import mock
import pytest
from anacode.api import writers


def dummy_write(*args, **kwargs):
    pass


@pytest.mark.parametrize('data,inc', [
    ({'concepts': [None] * 3}, 3),
    ({'categories': [None] * 5}, 5),
    ({'sentiment': [None] * 3}, 3),
    ({'absa': [None] * 20}, 20),
    ({'concepts': [None] * 3, 'categories': [None] * 3}, 3),
    ({'concepts': [None] * 3, 'single_document': True}, 1),
    ({'categories': [None], 'single_document': True}, 1),
    ({'sentiment': [None], 'single_document': True}, 1),
    ({'absa': [None] * 10, 'single_document': True}, 1),
    ({'absa': [None] * 10, 'sentiment': [None], 'single_document': True}, 1),
])
@mock.patch('anacode.api.writers.Writer.write_concepts', dummy_write)
@mock.patch('anacode.api.writers.Writer.write_categories', dummy_write)
@mock.patch('anacode.api.writers.Writer.write_sentiment', dummy_write)
@mock.patch('anacode.api.writers.Writer.write_absa', dummy_write)
def test_id_increase(data, inc):
    writer = writers.Writer()
    initial_id = writer.ids['analyze']
    writer.write_analysis(data)
    end_id = writer.ids['analyze']
    assert (end_id - initial_id) == inc


def test_concepts_to_list_many_document(concepts):
    result = writers.concepts_to_list(1, concepts)
    concepts = result['concepts']
    assert concepts[0] == [1, 0, 'Lenovo', 1, 1.0, 'brand']
    assert concepts[1] == [2, 0, 'Samsung', 1, 1.0, 'brand']


def test_concepts_to_list_one_document(concepts):
    result = writers.concepts_to_list(1, concepts, single_document=True)
    concepts = result['concepts']
    assert concepts[0] == [1, 0, 'Lenovo', 1, 1.0, 'brand']
    assert concepts[1] == [1, 1, 'Samsung', 1, 1.0, 'brand']


def test_categories_to_list_many_documents(categories):
    result = writers.categories_to_list(10, categories)
    categories = result['categories']
    assert len(categories) == 60
    assert set(cat[0] for cat in categories) == {10, 11}
    assert set(cat[1] for cat in categories) == {0}


def test_categories_to_list_one_document(categories):
    result = writers.categories_to_list(20, [categories[0]], True)
    categories = result['categories']
    assert len(categories) == 30
    assert set(cat[0] for cat in categories) == {20}
    assert set(cat[1] for cat in categories) == {0}


def test_sentiment_to_list_many_documents(sentiments):
    result = writers.sentiments_to_list(3, sentiments)
    sentiments = result['sentiments']
    assert sentiments[0] == [3, 0, 0.7299562892999195]
    assert sentiments[1] == [4, 0, 0.6668725094407698]


def test_sentiment_to_list_one_document(sentiments):
    result = writers.sentiments_to_list(2, [sentiments[0]], True)
    sentiments = result['sentiments']
    assert sentiments[0] == [2, 0, 0.7299562892999195]


def test_absa_to_list_many_documents(absa):
    result = writers.absa_to_list(77, absa)
    absa = result['absa_entities']
    assert absa[0] == [77, 0, 'OperationQuality', 'feature_subjective', '性能',
                       '2-4']
    assert absa[1] == [78, 0, 'OperationQuality', 'feature_subjective', '性能',
                       '0-2']


def test_absa_to_list_one_document(absa):
    result = writers.absa_to_list(80, absa, True)
    absa = result['absa_entities']
    assert absa[0] == [80, 0, 'OperationQuality', 'feature_subjective', '性能',
                       '2-4']
    assert absa[1] == [80, 1, 'OperationQuality', 'feature_subjective', '性能',
                       '0-2']
