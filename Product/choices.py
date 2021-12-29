PRINT_CHOICES = (
    ("MANTOUDJ_BLADI", "Mantoudj Bladi"),
    ("BEST_MARKET", "Best Market"),
    ("SUPERETTE", "Superette"),
    ("SUPER_MARKET", "Super Market"),
    ("LIKE", "Like"),
    ("Q&P", "Qualité/Prix"),
    ("THANKS", "Thanks"),
    ("BEST_OF_SHOPPING", "Best Of Shopping"),
    ("BIG_SHOP", "Big Shop"),
    ("THANK_YOU", "Thank You"),
    ("FAMILY_STORE", "Family Store"),
    ("TASSAOUK_AL_AFDAL", "Tassaouk Al Afdal"),
    ("FRUITS_ET_LEGUMES", "Fruits Et Légumes"),
    ("SHOP_EXPRESS", "Shop Express"),
    ("SURPRISE", "Surprise"),
    ("FRED_PERRY", "Fred Perry"),
    ("I_LOVE_SHOPPING", "I Love Shopping"),
    ("TOMMY_HILFIGER", "Tommy Hilfiger"),
    ("HACKETT", "Hackett"),
    ("PHARMACIE", "Pharmacie"),
    ("PIZZA", "Pizza"),
    ("BOUCHERIE", "Boucherie"),
    (None, "--------"),
)

SIZE = (
    (None,"---------"),
    ("SMALL","Petit Modèle"),
    ("MEDIUM","Moyen Modèle"),
    ("BIG","Grand Modèle"),
)

RANGE_CATEGORY = (
    ("RAW_MATTER", "Matière Première"),
    ("FINAL_PRODUCT", "Produit Fini"),
)

TYPE_PRODUCT = (
    (None, '---------'),
    ('HAUTE_DENSITE', 'Haute Densité'),
    ('BASSE_DENSITE', 'Basse Densité'),
    ('LINEAIRE', 'Linéaire'),
    ('AUTRE', 'Autre'),
)
DEFECTIVE_CHOICES = (
    ('DEFECTIVE', 'Défectueuse'),
    ('NON_DEFECTIVE', 'Normale'),
)

TYPE_TRASH = (
    ('HAUTE_DENSITE', 'Haute Densité'),
    ('BASSE_DENSITE', 'Basse Densité'),
)

TRASH_STATE = (
    ('PENDING', 'En attente de validation'),
    ('VALIDATED', 'Validé'),
)

TYPE_PIECE = (
    ('ELECTRIQUE', 'Electrique'),
    ('ELECTRONIQUE', 'Electronique'),
    ('MECANIQUE', 'Mécanique'),
    ('PNEUMATIQUE', 'Pneumatique'),
    ('HYDROLIQUE', 'Hydrolique'),
    ('AUTRE', 'AUTRE'),
)

TAPE_TYPE = (
    ('BIG', 'Grand Modèle'),
    ('SMALL', 'Petit Modèle'),
)

CATEGORY_TYPE = (
    ('MACHINE', 'Machine'),
    ('PRODUCT', 'Produit'),
)

PERFUMED = (
    ('NOT_PERFUMED', 'Non Parfumé'),
    ('PERFUMED', 'Parfumé'),
)

COIL_STATUS = (
    ('PENDING_EXTRUSION', "En cours d'extrusion"),
    ('PENDING_DATA', "En attente d'informations"),
    ('IN_STOCK', 'En Stock'),
    ('PENDING_PRINTING', "En cours d'impression"),
    ('PENDING_SHAPING', 'En cours de soudure'),
    ('CONSUMED', 'Consommée'),
    ('SOLD', 'Vendue'),
    ('QUARANTINE', 'En Quarantaine'),
    ('TO_BE_DESTROYED', 'A Détruire'),
    ('CUT', 'Coupée')
)

PRINTED = (
    ('PRINTED', "Imprimée"),
    ('NOT_PRINTED', 'Non Imprimée'),
)