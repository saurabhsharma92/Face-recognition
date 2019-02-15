import os
import mock
import pytest
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from anacode.agg import aggregation as agg
from anacode.agg import plotting


@pytest.fixture
def frame_concepts():
    con_header = ['doc_id', 'text_order', 'concept', 'freq', 'relevance_score',
                  'concept_type']
    exp_header = ['doc_id', 'text_order', 'concept', 'surface_string']
    cons = pd.DataFrame([
        [0, 0, 'Lenovo', 1, 1.0, 'brand'],
        [0, 1, 'Samsung', 1, 1.0, 'brand'],
        [0, 1, 'Lenovo', 2, 1.0, 'brand'],
        [0, 1, 'VisualAppearance', 2, 1.0, 'feature'],
    ], columns=con_header)
    exps = pd.DataFrame([
        [0, 0, 'Lenovo', 'lenovo'],
        [0, 1, 'Samsung', 'samsung'],
    ], columns=exp_header)
    return {'concepts': cons, 'surface_strings': exps}


@pytest.fixture
def concept_dataset(frame_concepts):
    return agg.ConceptsDataset(**frame_concepts)


@pytest.mark.parametrize('aggregation,args,plotmethod', [
    ('concept_frequency', [['Lenovo', 'Samsung']], 'barhchart'),
    ('most_common_concepts', [], 'barhchart'),
    ('least_common_concepts', [], 'barhchart'),
    ('co_occurring_concepts', ['Lenovo'], 'barhchart'),
    ('concept_frequencies', [], 'concept_cloud'),
])
def test_concept_aggregation_image_plot(concept_dataset, aggregation, args,
                                        plotmethod):
    agg_result = getattr(concept_dataset, aggregation)(*args)
    plot_result = getattr(plotting, plotmethod)(agg_result)
    assert isinstance(plot_result, Axes)


@pytest.mark.parametrize('aggregation,args,plotmethod', [
    ('concept_frequency', [['Lenovo', 'Samsung']], 'barhchart'),
    ('most_common_concepts', [], 'barhchart'),
    ('least_common_concepts', [], 'barhchart'),
    ('co_occurring_concepts', ['Lenovo'], 'barhchart'),
    ('concept_frequencies', [], 'concept_cloud'),
])
def test_concept_cloud_save_throws_no_error(concept_dataset, aggregation, args,
                                            plotmethod, tmpdir):
    target = tmpdir.mkdir('target')
    plot_path = os.path.join(str(target), 'test.png')
    agg_result = getattr(concept_dataset, aggregation)(*args)
    getattr(plotting, plotmethod)(agg_result, path=plot_path)
    assert os.path.isfile(plot_path)


@pytest.fixture
def frame_categories():
    cat_header = ['doc_id', 'text_order', 'category', 'probability']
    cats = pd.DataFrame([
        [0, 0, 'music', 0.1],
        [0, 0, 'law', 0.9],
        [0, 0, 'auto', 0.5],
        [0, 0, 'law', 0.5],
    ], columns=cat_header)
    return {'categories': cats}


@pytest.fixture
def categories_dataset(frame_categories):
    return agg.CategoriesDataset(**frame_categories)


def test_categories_direct_plot(categories_dataset):
    plot = plotting.piechart(categories_dataset.categories())
    assert isinstance(plot, Axes)


def test_categories_plot(categories_dataset):
    with mock.patch.object(plotting, 'piechart') as obj:
        plot = plotting.plot(categories_dataset.categories())
    obj.assert_called_once()


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
def absa_dataset(frame_absa):
    return agg.ABSADataset(**frame_absa)


@pytest.mark.parametrize('aggregation,args,plotmethod', [
    ('entity_frequency', [['Lenovo', 'Samsung']], 'barhchart'),
    ('most_common_entities', [], 'barhchart'),
    ('least_common_entities', [], 'barhchart'),
    ('co_occurring_entities', ['Lenovo'], 'barhchart'),
    ('best_rated_entities', [], 'barhchart'),
    ('worst_rated_entities', [], 'barhchart'),
    ('entity_sentiment', [['Safety', 'VisualAppearance']], 'barhchart'),
])
def test_absa_aggregation_image_plot(absa_dataset, aggregation, args,
                                     plotmethod):
    agg_result = getattr(absa_dataset, aggregation)(*args)
    plot_result = getattr(plotting, plotmethod)(agg_result)
    assert isinstance(plot_result, Axes)


@pytest.mark.parametrize('aggregation,args,plotmethod', [
    ('entity_frequency', [['Lenovo', 'Samsung']], 'barhchart'),
    ('most_common_entities', [], 'barhchart'),
    ('least_common_entities', [], 'barhchart'),
    ('co_occurring_entities', ['Lenovo'], 'barhchart'),
    ('best_rated_entities', [], 'barhchart'),
    ('worst_rated_entities', [], 'barhchart'),
    ('entity_sentiment', [['Safety', 'VisualAppearance']], 'barhchart'),
])
def test_absa_cloud_save_throws_no_error(absa_dataset, aggregation, args,
                                         plotmethod, tmpdir):
    target = tmpdir.mkdir('target')
    plot_path = os.path.join(str(target), 'test.png')
    agg_result = getattr(absa_dataset, aggregation)(*args)
    getattr(plotting, plotmethod)(agg_result, path=plot_path)
    assert os.path.isfile(plot_path)


@pytest.mark.parametrize('plot_name,series,expected', [
    ('Most Common Concepts', 'Person', 'Most Common Persons'),
    ('Concept Frequencies', 'Brand', 'Brand Frequencies'),
    ('Entities Sentiment', 'Product', 'Products Sentiment'),
    ('Least Common Entities', 'Feature', 'Least Common Features'),
])
def test_correct_title_change(plot_name, series, expected):
    result = plotting.chart_title(plot_name, series)
    assert result == expected


@pytest.mark.parametrize('string,exploded', [
    ('ProductType',  'Product Type'),
    ('SmartCar', 'Smart Car'),
    ('BMW', 'BMW'),
    ('Space', 'Space'),
    ('Nimbus2000', 'Nimbus 2000'),
    ('24Bank', '24 Bank'),
])
def test_explode_concepts(string, exploded):
    assert plotting.explode_capitalized(string) == exploded
