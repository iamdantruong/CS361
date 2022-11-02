countries = ['algeria','japan', 'benin', 'egypt', 'libya', 'china', 'japan','india' , 'south korea', 'vietnam', 'taiwan', 'greece', 'italy', 'france', 'portugal', 'spain','canada','guatemala','cuba','brazil', 'colombia', 'argentina', 'chile']


country_curr = {
    "United States": 'USD',
    "Afghanistan": 'AFN',
    "Algeria": 'DZD',
    "Andorra": 'EUR',
    "Angola" : 'AOA',
    "Argentina": 'ARS',
    "Australia": 'AUD',
    "Belgium" : 'EUR',
    "Brazil" : 'BRL',
    "Chile" : 'CLP',
    "China" : 'CNY',
    "Colombia": 'COP',
    "Egypt" : 'EGP',
    "Fiji": 'FJD',
    "France": 'EUR',
    "Greece": 'EUR',
    "Greenland": 'DKK',
    "Italy": 'EUR',
    "India": 'INR',
    "Japan": 'JPY',
    "New Zealand" : 'NZD',
    "Papua New Guinea": 'PGK',
    "South Korea": 'KRW',
    "Taiwan" : 'TWD',
    "Uruguay": 'URU',
    }

curr_name = {
    'USD': 'US Dollar',
    'AFN': 'Afghani',
    'ARS': 'Argentine Peso',
    'DZD': 'Algerian Dinar',
    'BRL': 'Brazilean Real',
    'COP': 'Colombian Peso',
    'EUR': 'Euro',
    'FJD': 'Fijian Dollar',
    'AOA': 'Kwanza',
    'AUD': 'Australian Dollar',
    'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan',
    'DKK': 'Danish Krone',
    'EGP': 'Egyptian Pound',
    'INR': 'Indian Rupee',
    'JPY': 'Japanese Yen',
    'KRW': 'Korean Won',
    'PGK': 'Kina',
    'NZD': 'New Zealand Dollar',
    'TWD': 'New Taiwan Dollar',
    'URU': 'Uruguayan Peso',
}
def validate_country(search):
    if search.lower() not in countries:
        return False
    return True


#def validate_currency()