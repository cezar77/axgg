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

STATUS = (
    ('NEW', 'new'),
    ('PROCESSING', 'processing'),
    ('RESOLVED', 'resolved'),
)
