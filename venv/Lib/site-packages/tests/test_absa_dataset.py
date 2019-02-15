# -*- coding: utf-8 -*-
import pytest
import numpy as np
import pandas as pd
from anacode.agg import aggregation as agg


@pytest.fixture
def frame_absa():
    ent_header = ['doc_id', 'text_order', 'entity_name', 'entity_type',
                  'surface_string', 'text_span']
    ents = pd.DataFrame([
        [0, 0, 'Lenovo', 'brand', 'lenovo', '4-9'],
        [0, 1, 'VisualAppearance', 'feature_subjective', 'looks', '0-4'],
        [0, 1, 'Samsung', 'brand', 'samsung', '15-21'],
        [0, 1, 'Lenovo', 'brand', 'Lenovo', '154-159'],
        [0, 1, 'Lenovo', 'brand', 'Lenovo', '210-215'],
        [0, 1, 'VisualAppearance', 'feature_subjective', 'looks', '30-34'],
    ], columns=ent_header)
    texts_header = ['doc_id', 'text_order', 'normalized_text']
    texts = pd.DataFrame([
        [0, 0, 'Hey lenovo'],
        [0, 1, '安全性能很好，很帅气。'],
    ], columns=texts_header)
    rel_header = ['doc_id', 'text_order', 'relation_id', 'opinion_holder',
                  'restriction', 'sentiment_value', 'is_external',
                  'surface_string', 'text_span']
    rels = pd.DataFrame([
        [0, 0, 0, '', '', 2.0, False, '安全', '0-2'],
        [0, 0, 1, '', '', 3.5, False, '很帅气', '7-10'],
        [0, 1, 0, '', '', 1.0, False, '安全', '0-2'],
        [0, 1, 1, '', '', 2.5, False, '很帅气', '7-10'],
    ], columns=rel_header)
    rel_ent_header = ['doc_id', 'text_order', 'relation_id',
                      'entity_type', 'entity_name']
    rel_entities = pd.DataFrame([
        [0, 0, 0, 'feature_quantitative', 'Safety'],
        [0, 0, 0, 'feature_objective', 'Hardiness'],
        [0, 0, 1, 'feature_subjective', 'VisualAppearance'],
        [0, 1, 0, 'feature_quantitative', 'Safety'],
        [0, 1, 1, 'feature_subjective', 'VisualAppearance'],
    ], columns=rel_ent_header)
    eval_header = ['doc_id', 'text_order', 'evaluation_id', 'sentiment_value',
                   'surface_string', 'text_span']
    evals = pd.DataFrame([
        [0, 0, 0, 2.0, '安全', '0-2'],
        [0, 0, 1, 3.5, '很帅气', '7-10'],
        [0, 1, 0, 1.0, '安全', '0-2'],
        [0, 1, 1, 2.5, '很帅气', '7-10'],
    ], columns=eval_header)
    eval_ents_header = ['doc_id', 'text_order', 'evaluation_id', 'entity_type',
                        'entity_name']
    eval_entities = pd.DataFrame([
        [0, 0, 0, 'feature_quantitative', 'Safety'],
        [0, 0, 1, 'feature_subjective', 'VisualAppearance'],
        [0, 1, 0, 'feature_quantitative', 'Safety'],
        [0, 1, 1, 'feature_subjective', 'VisualAppearance']
    ], columns=eval_ents_header)
    return {
        'entities': ents, 'normalized_texts': texts,
        'relations': rels, 'relations_entities': rel_entities,
        'evaluations': evals, 'evaluations_entities': eval_entities
    }


@pytest.fixture
def dataset(frame_absa):
    return agg.ABSADataset(**frame_absa)


@pytest.mark.parametrize('aggreg_func, args', [
    ('most_common_entities', []),
    ('least_common_entities', []),
    ('co_occurring_entities', ['lenovo']),
    ('best_rated_entities', []),
    ('worst_rated_entities', []),
    ('entity_texts', ['lenovo']),
    ('entity_sentiment', ['lenovo']),
])
def test_empty_dataset_failure(aggreg_func, args):
    dataset = agg.ABSADataset(None, None, None, None, None, None)
    with pytest.raises(agg.NoRelevantData):
        func = getattr(dataset, aggreg_func)
        func(*args)


@pytest.mark.parametrize('args,entities,freq', [
    ([1], ['Lenovo'], [3]),
    ([2], ['Lenovo', 'VisualAppearance'], [3, 2]),
    ([2, 'brand'], ['Lenovo', 'Samsung'], [3, 1]),
])
def test_most_common_entities(dataset, args, entities, freq):
    result = dataset.most_common_entities(*args)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities
    assert (result == freq).all()


@pytest.mark.parametrize('args,entities,freq', [
    ([1], ['Lenovo'], [3.0/6]),
    ([2], ['Lenovo', 'VisualAppearance'], [3.0/6, 2.0/6]),
    ([2, 'brand'], ['Lenovo', 'Samsung'], [3.0/4, 1.0/4]),
])
def test_most_common_entities_normalized(dataset, args, entities, freq):
    result = dataset.most_common_entities(*args, normalize=True)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities
    assert (result == freq).all()


@pytest.mark.parametrize('args,entities,freq', [
    ([1], ['Samsung'], [1]),
    ([2], ['Samsung', 'VisualAppearance'], [1, 2]),
    ([10, 'feature_'], ['VisualAppearance'], [2])
])
def test_least_common_entities(dataset, args, entities, freq):
    result = dataset.least_common_entities(*args)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities
    assert (result == freq).all()


@pytest.mark.parametrize('args,entities,freq', [
    ([1], ['Samsung'], [1.0/6]),
    ([2], ['Samsung', 'VisualAppearance'], [1.0/6, 2.0/6]),
    ([10, 'feature_'], ['VisualAppearance'], [2.0/2])
])
def test_least_common_entities_normalized(dataset, args, entities, freq):
    result = dataset.least_common_entities(*args, normalize=True)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities
    assert (result == freq).all()


@pytest.mark.parametrize('args,entities', [
    (['lenovo', 1], ['VisualAppearance']),
    (['Lenovo', 1], ['VisualAppearance']),
    (['Lenovo', 1, 'brand'], ['Samsung']),
    (['VisualAppearance', 2], ['Lenovo', 'Samsung']),
])
def test_co_occurring_entities(dataset, args, entities):
    result = dataset.co_occurring_entities(*args)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities


@pytest.mark.parametrize('args,entities', [
    ([1], ['VisualAppearance']),
    ([1, 'feature_quantitative'], ['Safety']),
    ([2], ['VisualAppearance', 'Hardiness']),
    ([19], ['VisualAppearance', 'Hardiness', 'Safety'])
])
def test_best_rated_entities(dataset, args, entities):
    result = dataset.best_rated_entities(*args)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities


@pytest.mark.parametrize('args,entities', [
    ([1], ['Safety']),
    ([1, 'feature_subjective'], ['VisualAppearance']),
    ([2], ['Safety', 'Hardiness']),
    ([5], ['Safety', 'Hardiness', 'VisualAppearance']),
])
def test_worst_rated_entities(dataset, args, entities):
    result = dataset.worst_rated_entities(*args)
    assert isinstance(result, pd.Series)
    assert result.index.tolist() == entities


@pytest.mark.parametrize('args,counts', [
    (['Lenovo'], [3]),
    ([['Lenovo']], [3]),
    ([['Lenovo', 'VisualAppearance']], [3, 2]),
    ([['VisualAppearance', 'Lenovo']], [2, 3]),
    (['NotHere'], [0]),
    ([['NotHere']], [0]),
    ([['Samsung', 'NotHere']], [1, 0]),
    ([['Samsung', 'VisualAppearance'], 'brand'], [1, 0])
])
def test_entity_frequencies(dataset, args, counts):
    result = dataset.entity_frequency(*args)
    assert isinstance(result, pd.Series)
    assert (result == counts).all()


@pytest.mark.parametrize('args,counts', [
    (['Lenovo'], [3.0/6]),
    ([['Lenovo']], [3.0/6]),
    ([['Lenovo', 'VisualAppearance']], [3.0/6, 2.0/6]),
    ([['VisualAppearance', 'Lenovo']], [2.0/6, 3.0/6]),
    (['NotHere'], [0]),
    ([['NotHere']], [0]),
    ([['Samsung', 'NotHere']], [1.0/6, 0]),
    ([['Samsung', 'VisualAppearance'], 'brand'], [1.0/4, 0])
])
def test_entity_frequencies_normalized(dataset, args, counts):
    result = dataset.entity_frequency(*args, normalize=True)
    assert isinstance(result, pd.Series)
    assert (result == counts).all()


@pytest.mark.parametrize('entity,texts', [
    ('Safety', {'Safety': []}),
    ('VisualAppearance', {'VisualAppearance': ['安全性能很好，很帅气。']}),
    ('visualappearance', {'visualappearance': []}),
    (['Lenovo', 'Safety'], {'Lenovo': ['Hey lenovo', '安全性能很好，很帅气。'],
                            'Safety': []}),
])
def test_entity_texts(dataset, entity, texts):
    result = dataset.entity_texts(entity)
    assert isinstance(result, dict)
    assert result == texts


@pytest.mark.parametrize('entity,texts', [
    ('Safety', {'Safety': ['安全', '安全']}),
    ('Hardiness', {'Hardiness': ['安全']}),
    (['Safety', 'VisualAppearance'], {'VisualAppearance': ['很帅气', '很帅气'],
                                      'Safety': ['安全', '安全']}),
    ('NotHere', {'NotHere': []}),
    (['Safety', 'NotHere'], {'Safety': ['安全', '安全'], 'NotHere': []}),
])
def test_entity_surface_strings(dataset, entity, texts):
    result = dataset.surface_strings(entity)
    assert isinstance(result, dict)
    assert result == texts


@pytest.mark.parametrize('entity,sentiment_value', [
    ('Safety', [1.5]),
    ('VisualAppearance', [3.0]),
    ('Hardiness', [2.0]),
    ('NotHere', [np.nan]),
    (['Hardiness', 'NotHere'], [2.0, np.nan]),
    (['Safety', 'VisualAppearance'], [1.5, 3.0]),
])
def test_entity_sentiment(dataset, entity, sentiment_value):
    result = dataset.entity_sentiment(entity)
    np.testing.assert_equal(result.values, sentiment_value)


@pytest.mark.parametrize('agg,args,name', [
    ('entity_frequency', ['lenovo'], 'Entity'),
    ('entity_frequency', ['lenovo', 'brand'], 'Brand'),
    ('entity_frequency', ['VisualAppearance', 'feature'], 'Feature'),
    ('most_common_entities', [1], 'Entity'),
    ('most_common_entities', [1, 'brand'], 'Brand'),
    ('most_common_entities', [1, 'feature'], 'Feature'),
    ('least_common_entities', [1], 'Entity'),
    ('least_common_entities', [1, 'brand'], 'Brand'),
    ('least_common_entities', [1, 'feature'], 'Feature'),
    ('co_occurring_entities', ['Lenovo', 1], 'Entity'),
    ('co_occurring_entities', ['Lenovo', 1, 'brand'], 'Brand'),
    ('co_occurring_entities', ['BackSeats', 1, 'feature'], 'Feature'),
])
def test_entity_result_name(dataset, agg, args, name):
    result = getattr(dataset, agg)(*args)
    assert result.index.name == name