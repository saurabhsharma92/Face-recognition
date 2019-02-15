# -*- coding: utf-8 -*-
import os
import pytest
import pandas as pd
from anacode.api import writers
from anacode.agg import aggregation as agg


@pytest.mark.parametrize('call_type,dataset_name,data', [
    ('categories', 'categories', pd.DataFrame([1])),
    ('concepts', 'concepts', pd.DataFrame([2])),
    ('concepts', 'concepts_surface_strings', pd.DataFrame([3])),
    ('sentiments', 'sentiments', pd.DataFrame([4])),
    ('absa', 'absa_entities', pd.DataFrame([5])),
    ('absa', 'absa_normalized_texts', pd.DataFrame([6])),
    ('absa', 'absa_relations', pd.DataFrame([7])),
    ('absa', 'absa_relations_entities', pd.DataFrame([8])),
    ('absa', 'absa_evaluations', pd.DataFrame([9])),
    ('absa', 'absa_evaluations_entities', pd.DataFrame([0])),
])
def test_init_correct_assignments(call_type, dataset_name, data):
    dataset = agg.DatasetLoader(**{dataset_name: data})
    has_dataset_name = 'has_' + call_type
    dataset_attr_name = '_' + dataset_name
    assert getattr(dataset, dataset_attr_name, None) is data
    assert getattr(dataset, has_dataset_name, False)


@pytest.mark.parametrize('call_type,dataset_name,data', [
    ('categories', 'categories', pd.DataFrame([1])),
    ('concepts', 'concepts', pd.DataFrame([2])),
    ('concepts', 'concepts_surface_strings', pd.DataFrame([3])),
    ('sentiments', 'sentiments', pd.DataFrame([4])),
    ('absa', 'absa_entities', pd.DataFrame([5])),
    ('absa', 'absa_normalized_texts', pd.DataFrame([6])),
    ('absa', 'absa_relations', pd.DataFrame([7])),
    ('absa', 'absa_relations_entities', pd.DataFrame([8])),
    ('absa', 'absa_evaluations', pd.DataFrame([9])),
    ('absa', 'absa_evaluations_entities', pd.DataFrame([0])),
])
def test_init_api_dataset_creation(call_type, dataset_name, data):
    dataset_class_map = {
        'concepts': agg.ConceptsDataset,
        'categories': agg.CategoriesDataset,
        'sentiments': agg.SentimentDataset,
        'absa': agg.ABSADataset,
    }
    dataset = agg.DatasetLoader(**{dataset_name: data})
    api_dataset = getattr(dataset, call_type)
    assert isinstance(api_dataset, dataset_class_map[call_type])


@pytest.mark.parametrize('call_type,dataset_name,data', [
    ('categories', 'categories', pd.DataFrame([1])),
    ('concepts', 'concepts', pd.DataFrame([2])),
    ('concepts', 'concepts_surface_strings', pd.DataFrame([3])),
    ('sentiments', 'sentiments', pd.DataFrame([4])),
    ('absa', 'absa_entities', pd.DataFrame([5])),
    ('absa', 'absa_normalized_texts', pd.DataFrame([6])),
    ('absa', 'absa_relations', pd.DataFrame([7])),
    ('absa', 'absa_relations_entities', pd.DataFrame([8])),
    ('absa', 'absa_evaluations', pd.DataFrame([9])),
    ('absa', 'absa_evaluations_entities', pd.DataFrame([0])),
])
def test_init_api_dataset_creation_failure(call_type, dataset_name, data):
    all_calls = {'categories', 'concepts', 'sentiments', 'absa'}
    dataset = agg.DatasetLoader(**{dataset_name: data})
    for call in all_calls - {call_type}:
        with pytest.raises(agg.NoRelevantData):
            getattr(dataset, call)


@pytest.fixture
def csv_writer(tmpdir, concepts, sentiments, categories, absa):
    target = tmpdir.mkdir('target')
    csv_writer = writers.CSVWriter(str(target))
    csv_writer.init()
    csv_writer.write_categories(categories)
    csv_writer.write_sentiment(sentiments)
    csv_writer.write_concepts(concepts)
    csv_writer.write_absa(absa)
    csv_writer.close()
    return csv_writer


@pytest.fixture
def data_folder(csv_writer):
    return csv_writer.target_dir


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_load_from_path(data_folder, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_path(data_folder)
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == shape


@pytest.fixture
def backup_folder(csv_writer):
    folder = csv_writer.target_dir
    for fname in os.listdir(folder):
        file_path = os.path.join(folder, fname)
        os.rename(file_path, file_path + '_backup')
    return folder


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_backup_load_from_path(backup_folder, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_path(backup_folder, 'backup')
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == shape


@pytest.mark.parametrize('dataset_name,shape', [
    ('categories', (60, 4)),
    ('sentiments', (2, 3)),
    ('concepts', (2, 6)),
    ('concepts_surface_strings', (2, 5)),
    ('absa_entities', (2, 6)),
    ('absa_normalized_texts', (2, 3)),
    ('absa_relations', (1, 9)),
    ('absa_relations_entities', (2, 5)),
    ('absa_evaluations', (2, 6)),
    ('absa_evaluations_entities', (2, 5))
])
def test_data_frame_getitem_access(data_folder, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_path(data_folder)
    dataset = dataset_loader[dataset_name]
    assert dataset is not None
    assert isinstance(dataset, pd.DataFrame)
    assert dataset.shape == shape


@pytest.fixture
def frame_writer(concepts, sentiments, categories, absa):
    frame_writer = writers.DataFrameWriter()
    frame_writer.init()
    frame_writer.write_categories(categories)
    frame_writer.write_sentiment(sentiments)
    frame_writer.write_concepts(concepts)
    frame_writer.write_absa(absa)
    frame_writer.close()
    return frame_writer


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_load_from_api_result(analysis, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_api_result(analysis)
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == shape


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_load_from_api_result_list(analysis, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_api_result([analysis, analysis])
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == (shape[0] * 2, shape[1])


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_load_from_csv_writer(csv_writer, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_writer(csv_writer)
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == shape


@pytest.mark.parametrize('dataset_name,shape', [
    ('_categories', (60, 4)),
    ('_sentiments', (2, 3)),
    ('_concepts', (2, 6)),
    ('_concepts_surface_strings', (2, 5)),
    ('_absa_entities', (2, 6)),
    ('_absa_normalized_texts', (2, 3)),
    ('_absa_relations', (1, 9)),
    ('_absa_relations_entities', (2, 5)),
    ('_absa_evaluations', (2, 6)),
    ('_absa_evaluations_entities', (2, 5))
])
def test_data_load_from_frame_writer(frame_writer, dataset_name, shape):
    dataset_loader = agg.DatasetLoader.from_writer(frame_writer)
    dataset = getattr(dataset_loader, dataset_name)
    assert dataset is not None
    assert dataset.shape == shape


def test_dataset_loader_remove_concepts(frame_writer):
    dataset = agg.DatasetLoader.from_writer(frame_writer)
    dataset.remove_concepts(['Lenovo'])
    assert (dataset.concepts.concept_frequency(['Lenovo']) == [0]).all()


@pytest.fixture
def concept_dataset_writer_reduced(concepts):
    for response in concepts:
        for concept in response:
            del concept['surface']
            del concept['relevance_score']
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_concepts(concepts)
    writer.close()
    return writer


def test_load_incomplete_concepts(concept_dataset_writer_reduced):
    dataset = agg.DatasetLoader.from_writer(concept_dataset_writer_reduced)
    concepts = dataset.concepts
    assert isinstance(concepts, agg.ConceptsDataset)
    assert concepts.concept_frequency(['Lenovo', 'Samsung']).tolist() == [1, 1]
