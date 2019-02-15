# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from freezegun import freeze_time
from anacode.api import writers


@freeze_time(datetime(2016, 12, 6, 18, 0, 6))
class TestBackup:
    def test_backup_works(self, tmpdir):
        target = tmpdir.mkdir('target')
        target.join('concepts.csv').write('content')
        writers.backup(str(target), ['concepts.csv'])
        contents = [f.basename for f in target.listdir()]
        assert 'concepts.csv' not in contents
        assert 'concepts.csv_20161206180006' in contents

    def test_backup_returns_files(self, tmpdir):
        target = tmpdir.mkdir('target')
        target.join('concepts.csv').write('content')
        backed_up = writers.backup(str(target), ['concepts.csv'])
        assert backed_up == ['concepts.csv_20161206180006']

    def test_no_file_no_backup(self, tmpdir):
        target = tmpdir.mkdir('target')
        target.join('concepts.csv').write('content')
        backed_up = writers.backup(str(target), ['nofile.csv'])
        contents = [f.basename for f in target.listdir()]
        assert len(backed_up) == 0
        assert contents == ['concepts.csv']


def test_csvwriter_init_with_directory():
    csv_writer = writers.CSVWriter('/tmp/test')
    assert csv_writer.target_dir == '/tmp/test'


@pytest.fixture
def target(tmpdir):
    return tmpdir.mkdir('target')


@pytest.fixture
def csv_concepts_reduced(target, concepts):
    for response in concepts:
        for concept in response:
            del concept['surface']
            del concept['relevance_score']
    csv_writer = writers.CSVWriter(str(target))
    csv_writer.init()
    csv_writer.write_concepts(concepts)
    csv_writer.close()
    return csv_writer


@pytest.fixture
def csv_concepts(target, concepts):
    csv_writer = writers.CSVWriter(str(target))
    csv_writer.init()
    csv_writer.write_concepts(concepts)
    csv_writer.close()
    return csv_writer


class TestCsvWriterConcepts:
    def test_no_other_csvs(self, target, csv_concepts):
        contents = [f.basename for f in target.listdir()]
        assert len(contents) == 2
        assert 'concepts.csv' in contents
        assert 'concepts_surface_strings.csv' in contents

    def test_no_other_csvs_reduced(self, target, csv_concepts_reduced):
        contents = [f.basename for f in target.listdir()]
        assert len(contents) == 1
        assert 'concepts.csv' in contents
        assert 'concepts_surface_strings.csv' not in contents

    def test_concepts_file_have_headers(self, target, csv_concepts):
        file_lines = target.join('concepts.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'concept', 'freq',
                          'relevance_score', 'concept_type']

    def test_concepts_file_have_headers(self, target, csv_concepts_reduced):
        file_lines = target.join('concepts.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'concept', 'freq',
                          'relevance_score', 'concept_type']

    def test_concepts_exprs_file_have_headers(self, target, csv_concepts):
        file_lines = target.join('concepts_surface_strings.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'concept', 'surface_string',
                          'text_span']

    def test_write_concepts(self, target, csv_concepts):
        file_lines = target.join('concepts.csv').readlines()
        assert len(file_lines) == 3
        row1 = file_lines[1].strip().split(',')
        row2 = file_lines[2].strip().split(',')
        assert row1 == ['0', '0', 'Lenovo', '1', '1.0', 'brand']
        assert row2 == ['1', '0', 'Samsung', '1', '1.0', 'brand']

    def test_write_exprs(self, target, csv_concepts):
        file_lines = target.join('concepts_surface_strings.csv').readlines()
        assert len(file_lines) == 3
        row1 = file_lines[1].strip().split(',')
        row2 = file_lines[2].strip().split(',')
        assert row1 == ['0', '0', 'Lenovo', 'lenovo', '0-6']
        assert row2 == ['1', '0', 'Samsung', 'samsung', '0-7']


class TestCsvWriterSentiment:
    def test_no_other_csvs(self, tmpdir, sentiments):
        target = tmpdir.mkdir('target')
        csv_writer = writers.CSVWriter(str(target))
        csv_writer.init()
        csv_writer.write_sentiment(sentiments)
        csv_writer.close()
        contents = [f.basename for f in target.listdir()]
        assert len(contents) == 1
        assert 'sentiments.csv' in contents

    def test_write_sentiment_headers(self, tmpdir, sentiments):
        target = tmpdir.mkdir('target')
        csv_writer = writers.CSVWriter(str(target))
        csv_writer.init()
        csv_writer.write_sentiment(sentiments)
        csv_writer.close()
        header = target.join('sentiments.csv').readlines()[0].strip()
        assert 'doc_id' in header
        assert 'text_order' in header
        assert 'sentiment_value' in header

    def test_write_sentiment_values(self, tmpdir, sentiments):
        target = tmpdir.mkdir('target')
        csv_writer = writers.CSVWriter(str(target))
        csv_writer.init()
        csv_writer.write_sentiment(sentiments)
        csv_writer.close()
        file_lines = target.join('sentiments.csv').readlines()
        assert len(file_lines) == 3
        row1 = file_lines[1].strip().split(',')
        assert row1[0] == '0'
        assert row1[1] == '0'
        assert row1[2].startswith('0.72')
        row2 = file_lines[2].strip().split(',')
        assert row2[0] == '1'
        assert row2[1] == '0'
        assert row2[2].startswith('0.66')


@pytest.fixture
def csv_categories(target, categories):
    csv_writer = writers.CSVWriter(str(target))
    csv_writer.init()
    csv_writer.write_categories(categories)
    csv_writer.close()
    return csv_writer


class TestCsvWriterCategories:
    def test_no_other_csvs(self, target, csv_categories):
        contents = [f.basename for f in target.listdir()]
        assert len(contents) == 1
        assert 'categories.csv' in contents

    def test_write_categories_headers(self, target, csv_categories):
        file_lines = target.join('categories.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'category', 'probability']

    def test_write_categories(self, target, csv_categories):
        file_lines = target.join('categories.csv').readlines()
        assert len(file_lines) == 30 + 30 + 1
        assert any(line.startswith('0,0,camera,0.444') for line in file_lines)
        assert any(line.startswith('0,0,music,0.002') for line in file_lines)
        assert any(line.startswith('1,0,law,0.043') for line in file_lines)


@pytest.fixture
def csv_absa(target, absa):
    csv_writer = writers.CSVWriter(str(target))
    csv_writer.init()
    csv_writer.write_absa(absa)
    csv_writer.close()
    return csv_writer


class TestCsvWriterAbsa:
    def test_no_other_csvs(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert len(contents) == 6
        assert 'absa_entities.csv' in contents
        assert 'absa_normalized_texts.csv' in contents
        assert 'absa_relations.csv' in contents
        assert 'absa_relations_entities.csv' in contents
        assert 'absa_evaluations.csv' in contents
        assert 'absa_evaluations_entities.csv' in contents

    def test_absa_entities_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_entities.csv' in contents
        file_lines = target.join('absa_entities.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'entity_name', 'entity_type',
                          'surface_string', 'text_span']

    def test_absa_normalized_text_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_normalized_texts.csv' in contents
        file_lines = target.join('absa_normalized_texts.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'normalized_text']

    def test_absa_relations_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_relations.csv' in contents
        file_lines = target.join('absa_relations.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'relation_id',
                          'opinion_holder', 'restriction', 'sentiment_value',
                          'is_external', 'surface_string', 'text_span']

    def test_absa_rel_entities_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_relations_entities.csv' in contents
        file_lines = target.join('absa_relations_entities.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'relation_id',
                          'entity_type', 'entity_name']

    def test_absa_evaluations_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_evaluations.csv' in contents
        file_lines = target.join('absa_evaluations.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'evaluation_id',
                          'sentiment_value', 'surface_string', 'text_span']

    def test_absa_eval_entities_headers(self, target, csv_absa):
        contents = [f.basename for f in target.listdir()]
        assert 'absa_evaluations_entities.csv' in contents
        file_lines = target.join('absa_evaluations_entities.csv').readlines()
        header = file_lines[0].strip().split(',')
        assert header == ['doc_id', 'text_order', 'evaluation_id',
                          'entity_type', 'entity_name']

    def test_write_absa_entities(self, target, csv_absa):
        file_lines = target.join('absa_entities.csv').readlines()
        assert len(file_lines) == 3
        entity0 = file_lines[1].strip().split(',')
        entity1 = file_lines[2].strip().split(',')
        assert entity0 == ['0', '0', 'OperationQuality', 'feature_subjective',
                           '性能', '2-4']
        assert entity1 == ['1', '0', 'OperationQuality', 'feature_subjective',
                           '性能', '0-2']

    def test_write_absa_normalized_texts(self, target, csv_absa):
        file_lines = target.join('absa_normalized_texts.csv').readlines()
        assert len(file_lines) == 3
        entity0 = file_lines[1].strip().split(',')
        entity1 = file_lines[2].strip().split(',')
        assert entity0 == ['0', '0', '安全性能很好，很帅气。']
        assert entity1 == ['1', '0', '性能']

    def test_write_absa_relations(self, target, csv_absa):
        file_lines = target.join('absa_relations.csv').readlines()
        assert len(file_lines) == 2
        relation = file_lines[1].strip().split(',')
        assert relation == ['0', '0', '0', '', '', '2.0', 'False',
                            '安全性能', '0-4']

    def test_write_absa_relation_entities(self, target, csv_absa):
        file_lines = target.join('absa_relations_entities.csv').readlines()
        assert len(file_lines) == 3
        entity1 = file_lines[1].strip().split(',')
        entity2 = file_lines[2].strip().split(',')
        assert entity1 == ['0', '0', '0', 'feature_quantitative', 'Safety']
        assert entity2 == ['0', '0', '0', 'feature_subjective',
                           'OperationQuality']

    def test_write_evaluations(self, target, csv_absa):
        file_lines = target.join('absa_evaluations.csv').readlines()
        assert len(file_lines) == 3
        eval1 = file_lines[1].strip().split(',')
        eval2 = file_lines[2].strip().split(',')
        assert eval1 == ['0', '0', '0', '2.0', '安全', '0-2']
        assert eval2 == ['0', '0', '1', '3.5', '很帅气', '7-10']

    def test_write_evaluation_entities(self, target, csv_absa):
        file_lines = target.join('absa_evaluations_entities.csv').readlines()
        assert len(file_lines) == 3
        entity1 = file_lines[1].strip().split(',')
        entity2 = file_lines[2].strip().split(',')
        assert entity1 == ['0', '0', '0', 'feature_quantitative', 'Safety']
        assert entity2 == ['0', '0', '1', 'feature_subjective',
                           'VisualAppearance']
