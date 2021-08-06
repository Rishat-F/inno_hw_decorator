LOCALE_TEST_CASES = {
    "valid": [
        {"locale": "en"},
        {"locale": "en_GB"},
        {"locale": "fr_FR"},
        {"locale": "ru_RU"},
        {"locale": "it_IT"},
    ],
    "invalid": [
        {"locale": "en_EN"},
        {"local": "es_ES"},
        {"locale": 12},
        {"locale": "35"},
        {"locale": "it_IT", "city": "Milan"},
    ]
}
FULLNAME_TEST_CASES = {
    "valid": [
        "Andy Miller", "Andrey Stepanovich Ivanov", "John Nicolsen",
        "Jenel Larone", "Lionel Messi", "Agatha Kristi",
        "Paul Van Deik", "Park U Soon", "Viktor An",
    ],
    "invalid": [
        "Andy", "Popov alexey Sergeevich", "Connor McDavid",
        "Koko D'Jardine", "Enrike Paulo-Antonio",
        "Martin St.Piere", "Romero Baptista jn",
    ]
}
