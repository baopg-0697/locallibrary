#All consts of catalog

#const models
MAX_LENGTH_1 = 1
MAX_LENGTH_200 = 200
MAX_LENGTH_13 = 13
MAX_LENGTH_1000 = 1000
MAX_LENGTH_100 = 100
#const of Bookinstance'table in models
LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

LOAN_STATUS_M = 'm'
LOAN_STATUS_O = 'o'
LOAN_STATUS_A = 'a'
LOAN_STATUS_R = 'r'

INITIAL_DATE = {'date_of_death': '11/11/2023'}
NUMBER_PAGINATE_BY = 10
