# list of languages with ISO 639-1 code and the English name of the language
LANGUAGES = (
    ('am', 'Amharic'),
    ('en', 'English'),
    ('fr', 'French'),
    ('sw', 'Swahili'),
)

ROLES = (
    ('F', 'Farmer'),
)

SEXES = (
    ('F', 'female'),
    ('M', 'male')
)

NAME_SCHEMA = {
    'first': {
        'required': True,
        'type': 'string',
        'maxlength': 30
    },
    'middle': {
        'type': 'string',
        'maxlength': 30
    },
    'last': {
        'required': True,
        'type': 'string',
        'maxlength': 30
    }
}

DATE_SCHEMA = {
    'day': {
        'type': 'integer'
    },
    'month': {
        'type': 'integer'
    },
    'year': {
        'required': True,
        'type': 'integer'
    }
}

STATUS = (
    ('NEW', 'new'),
    ('PROCESSING', 'processing'),
    ('RESOLVED', 'resolved'),
)
