# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def concepts():
    return [
        [
            {
                'concept': 'Lenovo',
                'surface': [
                    {'surface_string': 'lenovo', 'span': (0, 6)}
                ],
                'freq': 1,
                'relevance_score': 1.0,
                'type': 'brand'
            }
        ],
        [
            {
                'concept': 'Samsung',
                'surface': [
                    {'surface_string': 'samsung', 'span': (0, 7)}
                ],
                'freq': 1,
                'relevance_score': 1.0,
                'type': 'brand'
            }
        ]
    ]


@pytest.fixture
def sentiments():
    return [
        {'sentiment_value': 0.7299562892999195},
        {'sentiment_value': 0.6668725094407698},
    ]


@pytest.fixture
def categories():
    return [
        [
            {'label': 'camera', 'probability': 0.44475978426332685},
            {'label': 'travel', 'probability': 0.2279223877672652},
            {'label': 'hr', 'probability': 0.09173477160494019},
            {'label': 'auto', 'probability': 0.06708061556120234},
            {'label': 'fashion', 'probability': 0.025414852323138004},
            {'label': 'finance', 'probability': 0.018507594185656784},
            {'label': 'food', 'probability': 0.010119412627783536},
            {'label': 'law', 'probability': 0.00965379302613669},
            {'label': 'education', 'probability': 0.009582090685450925},
            {'label': 'ce', 'probability': 0.009340358982552241},
            {'label': 'furniture', 'probability': 0.008684932567501653},
            {'label': 'internet', 'probability': 0.00778506882501582},
            {'label': 'babies', 'probability': 0.007096874411645032},
            {'label': 'fitness', 'probability': 0.0069576834053539675},
            {'label': 'health', 'probability': 0.006145046000728843},
            {'label': 'sports', 'probability': 0.006031221668762928},
            {'label': 'entertainment', 'probability': 0.005231272080964669},
            {'label': 'mobile', 'probability': 0.004967572280467443},
            {'label': 'beauty', 'probability': 0.00494888795526646},
            {'label': 'realestate', 'probability': 0.004493574861362339},
            {'label': 'energy', 'probability': 0.0040505145283132385},
            {'label': 'airline', 'probability': 0.003390457074009262},
            {'label': 'art', 'probability': 0.0028687491478624947},
            {'label': 'architecture', 'probability': 0.002822605573936816},
            {'label': 'music', 'probability': 0.0027084020379582676},
            {'label': 'hotel', 'probability': 0.002295792656008564},
            {'label': 'appliances', 'probability': 0.002193479986584827},
            {'label': 'books', 'probability': 0.001483402884988822},
            {'label': 'games', 'probability': 0.0010261026838245006},
            {'label': 'business', 'probability': 0.0007026983419913149}
        ],
        [
            {'label': 'games', 'probability': 0.39789969578523887},
            {'label': 'travel', 'probability': 0.11634739448945783},
            {'label': 'fashion', 'probability': 0.09168535069430538},
            {'label': 'law', 'probability': 0.04323751076891663},
            {'label': 'auto', 'probability': 0.041857526739422356},
            {'label': 'airline', 'probability': 0.035446480105636335},
            {'label': 'ce', 'probability': 0.03478883675405762},
            {'label': 'camera', 'probability': 0.02719330000509693},
            {'label': 'food', 'probability': 0.024219656311877134},
            {'label': 'finance', 'probability': 0.02301679246976262},
            {'label': 'education', 'probability': 0.022459608009340545},
            {'label': 'architecture', 'probability': 0.017837572573750626},
            {'label': 'beauty', 'probability': 0.015451481313075766},
            {'label': 'fitness', 'probability': 0.014332460323421978},
            {'label': 'babies', 'probability': 0.011144662880568099},
            {'label': 'health', 'probability': 0.010945923020829255},
            {'label': 'furniture', 'probability': 0.010466338721162467},
            {'label': 'hr', 'probability': 0.009210314423265968},
            {'label': 'mobile', 'probability': 0.008598212480182528},
            {'label': 'music', 'probability': 0.008036079511276282},
            {'label': 'internet', 'probability': 0.006370603094547427},
            {'label': 'hotel', 'probability': 0.005955447551681576},
            {'label': 'realestate', 'probability': 0.005121969573881132},
            {'label': 'entertainment', 'probability': 0.004570734302611687},
            {'label': 'energy', 'probability': 0.00424202672617446},
            {'label': 'appliances', 'probability': 0.004177990415535009},
            {'label': 'art', 'probability': 0.0021153603845123245},
            {'label': 'books', 'probability': 0.0013904052961039273},
            {'label': 'sports', 'probability': 0.0010192722188369773},
            {'label': 'business', 'probability': 0.0008609930554701703}
        ]
    ]


@pytest.fixture
def absa():
    return [{
        'entities': [
            {
                'semantics': [
                    {'type': 'feature_subjective', 'value': 'OperationQuality'}
                ],
                'surface': {'span': [2, 4], 'surface_string': '性能'}
            }
        ],
        'evaluations': [
            {
                'semantics': {
                    'entity': [
                        {'type': 'feature_quantitative', 'value': 'Safety'}
                    ],
                    'sentiment_value': 2.0
                },
                'surface': {'span': [0, 2], 'surface_string': '安全'}
            },
            {
                'semantics': {
                    'entity': [
                        {'type': 'feature_subjective', 'value': 'VisualAppearance'}
                    ],
                    'sentiment_value': 3.5
                },
                'surface': {'span': [7, 10], 'surface_string': '很帅气'}
            }
        ],
        'normalized_text': '安全性能很好，很帅气。',
        'relations': [
            {
                'external_entity': False,
                'semantics': {
                    'entity': [
                        {'type': 'feature_quantitative', 'value': 'Safety'},
                        {'type': 'feature_subjective', 'value': 'OperationQuality'}
                    ],
                    'opinion_holder': None,
                    'restriction': None,
                    'sentiment_value': 2.0
                },
                'surface': {'span': [0, 4], 'surface_string': '安全性能'}
            }
        ]
    }, {
        'entities': [
            {
                'semantics': [
                    {'type': 'feature_subjective', 'value': 'OperationQuality'}
                ],
                'surface': {'span': [0, 2], 'surface_string': '性能'}
            }
        ],
        'evaluations': [], 'relations': [], 'normalized_text': '性能',
    }]


@pytest.fixture
def analysis(concepts, categories, sentiments, absa):
    return {
        'concepts': concepts, 'categories': categories,
        'sentiment': sentiments, 'absa': absa,
    }