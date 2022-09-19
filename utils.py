from flask import json

from main import get_data_by_sql


def step_5(name1='Rose McIver', name2='Ben Lamb'):
    sql = f'''
           select netflix.cast from netflix
           where netflix.cast like '%{name1}%' and netflix.cast like '%{name2}%'
    '''

    names_dict = {}

    for item in get_data_by_sql(sql):
        result = dict(item)

        names = set(result.get('cast').split(", ")) - set([name1, name2])

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(),0) + 1

    print(names_dict)

    for k, v in names_dict:
        if v > 2:
            print(k)

def step_6(types='Movie', year=2020, genre='Horror'):
    sql = f'''
               select * from netflix
               where type = '{types.title()}'
               and release_year = '{year}'
               and listed_in like '%{genre.title}%' 
        '''

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)