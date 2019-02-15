# -*- coding: utf-8 -*-
import pytest
from anacode.api import writers


@pytest.fixture
def concept_frames_reduced(concepts):
    for response in concepts:
        for concept in response:
            del concept['surface']
            del concept['relevance_score']
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_concepts(concepts)
    writer.close()
    return writer.frames


@pytest.fixture
def concept_frames(concepts):
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_concepts(concepts)
    writer.close()
    return writer.frames


class TestDataFrameWriterConcepts:
    def test_concepts_file_have_headers(self, concept_frames):
        assert 'concepts' in concept_frames
        header = concept_frames['concepts'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'concept', 'freq',
                          'relevance_score', 'concept_type']

    def test_reduced_concepts_file_have_headers(self, concept_frames_reduced):
        assert 'concepts' in concept_frames_reduced
        header = concept_frames_reduced['concepts'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'concept', 'freq',
                          'relevance_score', 'concept_type']

    def test_concepts_exprs_file_have_headers(self, concept_frames):
        assert 'concepts_surface_strings' in concept_frames
        header = concept_frames['concepts_surface_strings'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'concept', 'surface_string',
                          'text_span']

    def test_concepts_exprs_file_have_headers(self, concept_frames_reduced):
        assert 'concepts_surface_strings' not in concept_frames_reduced

    def test_write_concepts(self, concept_frames):
        concepts = concept_frames['concepts']
        assert concepts.shape == (2, 6)
        row1, row2 = concepts.iloc[0].tolist(), concepts.iloc[1].tolist()
        assert row1 == [0, 0, 'Lenovo', 1, 1.0, 'brand']
        assert row2 == [1, 0, 'Samsung', 1, 1.0, 'brand']

    def test_write_concepts(self, concept_frames_reduced):
        concepts = concept_frames_reduced['concepts']
        assert concepts.shape == (2, 6)
        row1, row2 = concepts.iloc[0].tolist(), concepts.iloc[1].tolist()
        assert row1 == [0, 0, 'Lenovo', 1, None, 'brand']
        assert row2 == [1, 0, 'Samsung', 1, None, 'brand']

    def test_write_exprs(self, concept_frames):
        surface_strings = concept_frames['concepts_surface_strings']
        assert surface_strings.shape == (2, 5)
        row1 = surface_strings.iloc[0].tolist()
        row2 = surface_strings.iloc[1].tolist()
        assert row1 == [0, 0, 'Lenovo', 'lenovo', '0-6']
        assert row2 == [1, 0, 'Samsung', 'samsung', '0-7']

    def test_write_exprs(self, concept_frames_reduced):
        assert 'concepts_surface_strings' not in concept_frames_reduced


@pytest.fixture
def sentiment_frames(sentiments):
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_sentiment(sentiments)
    writer.close()
    return writer.frames


class TestDataFrameWriterSentiment:
    def test_write_sentiment_headers(self, sentiment_frames):
        assert 'sentiments' in sentiment_frames
        header = sentiment_frames['sentiments'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'sentiment_value']

    def test_write_sentiment_values(self, sentiment_frames):
        sentiments = sentiment_frames['sentiments']
        assert sentiments.shape == (2, 3)
        row1, row2 = sentiments.iloc[0].tolist(), sentiments.iloc[1].tolist()
        assert row1 == [0, 0, 0.72995628929991951]
        assert row2 == [1, 0, 0.66687250944076981]


@pytest.fixture
def category_frames(categories):
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_categories(categories)
    writer.close()
    return writer.frames


class TestDataFrameWriterCategories:
    def test_write_categories_headers(self, category_frames):
        assert 'categories' in category_frames
        header = category_frames['categories'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'category', 'probability']

    def test_write_categories(self, category_frames):
        categories = category_frames['categories']
        assert categories.shape == (30 + 30, 4)

        cats = categories.category
        docs = categories.doc_id
        text = categories.text_order

        cam_filter = (docs == 0) & (text == 0) & (cats == 'camera')
        camera_prob = categories[cam_filter].probability.iloc[0]
        assert camera_prob == 0.44475978426332685
        mus_filter = (docs == 0) & (text == 0) & (cats == 'music')
        music_prob = categories[mus_filter].probability.iloc[0]
        assert music_prob == 0.0027084020379582676
        law_filter = (docs == 1) & (text == 0) & (cats == 'law')
        law_prob = categories[law_filter].probability.iloc[0]
        assert law_prob == 0.043237510768916632


@pytest.fixture
def absa_frames(absa):
    writer = writers.DataFrameWriter()
    writer.init()
    writer.write_absa(absa)
    writer.close()
    return writer.frames


class TestDataFrameWriterAbsa:
    def test_absa_entities_headers(self, absa_frames):
        assert 'absa_entities' in absa_frames
        header = absa_frames['absa_entities'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'entity_name', 'entity_type',
                          'surface_string', 'text_span']

    def test_absa_normalized_text_headers(self, absa_frames):
        assert 'absa_normalized_texts' in absa_frames
        header = absa_frames['absa_normalized_texts'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'normalized_text']

    def test_absa_relations_headers(self, absa_frames):
        assert 'absa_relations' in absa_frames
        header = absa_frames['absa_relations'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'relation_id',
                          'opinion_holder', 'restriction', 'sentiment_value',
                          'is_external', 'surface_string', 'text_span']

    def test_absa_rel_entities_headers(self, absa_frames):
        assert 'absa_relations_entities' in absa_frames
        header = absa_frames['absa_relations_entities'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'relation_id',
                          'entity_type', 'entity_name']

    def test_absa_evaluations_headers(self, absa_frames):
        assert 'absa_evaluations' in absa_frames
        header = absa_frames['absa_evaluations'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'evaluation_id',
                          'sentiment_value', 'surface_string', 'text_span']

    def test_absa_eval_entities_headers(self, absa_frames):
        assert 'absa_evaluations_entities' in absa_frames
        header = absa_frames['absa_evaluations_entities'].columns.tolist()
        assert header == ['doc_id', 'text_order', 'evaluation_id',
                          'entity_type', 'entity_name']

    def test_write_absa_entities(self, absa_frames):
        entities = absa_frames['absa_entities']
        assert entities.shape == (2, 6)
        entity0 = entities.iloc[0].tolist()
        entity1 = entities.iloc[1].tolist()
        assert entity0 == [0, 0, 'OperationQuality', 'feature_subjective',
                           '性能', '2-4']
        assert entity1 == [1, 0, 'OperationQuality', 'feature_subjective',
                           '性能', '0-2']

    def test_write_absa_normalized_texts(self, absa_frames):
        texts = absa_frames['absa_normalized_texts']
        assert texts.shape == (2, 3)
        entity0 = texts.iloc[0].tolist()
        entity1 = texts.iloc[1].tolist()
        assert entity0 == [0, 0, '安全性能很好，很帅气。']
        assert entity1 == [1, 0, '性能']

    def test_write_absa_relations(self, absa_frames):
        relations = absa_frames['absa_relations']
        assert relations.shape == (1, 9)
        relation = relations.iloc[0].tolist()
        assert relation == [0, 0, 0, None, None, 2.0, False,
                            '安全性能', '0-4']

    def test_write_absa_relation_entities(self, absa_frames):
        entities = absa_frames['absa_relations_entities']
        assert entities.shape == (2, 5)
        entity1, entity2 = entities.iloc[0].tolist(), entities.iloc[1].tolist()
        assert entity1 == [0, 0, 0, 'feature_quantitative', 'Safety']
        assert entity2 == [0, 0, 0, 'feature_subjective', 'OperationQuality']

    def test_write_evaluations(self, absa_frames):
        evaluations = absa_frames['absa_evaluations']
        assert evaluations.shape == (2, 6)
        eval1 = evaluations.iloc[0].tolist()
        eval2 = evaluations.iloc[1].tolist()
        assert eval1 == [0, 0, 0, 2.0, '安全', '0-2']
        assert eval2 == [0, 0, 1, 3.5, '很帅气', '7-10']

    def test_write_evaluation_entities(self, absa_frames):
        entities = absa_frames['absa_evaluations_entities']
        assert entities.shape == (2, 5)
        entity1, entity2 = entities.iloc[0].tolist(), entities.iloc[1].tolist()
        assert entity1 == [0, 0, 0, 'feature_quantitative', 'Safety']
        assert entity2 == [0, 0, 1, 'feature_subjective', 'VisualAppearance']
