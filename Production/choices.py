PROCESS_TYPE = (
    ('SHAPING', 'Façonnage'),
    ('PRINTING', 'Impression'),
    ('MIXING', 'Mélange'),
    ('EXTRUSION', 'Extrusion'),
    ('FINISHED_PRODUCT','Production'),
)

STATE_PRODUCTION = (
    ('PENDING', 'En Cours'),
    ('FINISHED', 'Terminé'),
)

CONSUMED = (
    ('CONSUMED', 'Consommé'),
    ('NOT_CONSUMED','Non Consommé'),
)

CORRECTION_TYPE = (
    ('POSITIVE', 'Ecart Positif'),
    ('NEGATIVE','Ecart Négatif'),
)