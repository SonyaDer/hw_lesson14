import sqlite3
from flask import Flask, json, jsonify

app = Flask(__name__)

def get_data_by_sql(sql):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()

    return result

@app.get("/movie/<title>/")
def step_1(title):
    result = {}
    for item in get_data_by_sql(sql=f'''
           select title, country, release_year, genre, description
           from netflix
           where title = '{title}'
           order by release_year desc
           limit 1
           '''):
        result = dict(item)
    return jsonify(result)


@app.get("/movie/<int:year1>/to/<int:year2>/")
def step_2(year1, year2):
    result = {}
    sql=f'''
    select * from netflix
    where release_year between {year1} and {year2}
    limit 100
    '''

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return jsonify(result)

@app.get("/rating/<rating>/")
def step_3(rating):
    my_rating = {
        'children': ("G", "G"),
        'family': ("G", "PG", "PG-13"),
        "adult": ("R", "NR-17")
    }
    sql = f'''
           select * from netflix
           where rating in {my_rating.get(rating)}
    '''

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return jsonify(result)


@app.get("/genre/<genre>/")
def step_4(genre):
    sql = f'''
           select title, description from netflix
           where listed_in like '%{str(genre).title()}%'
           limit 10
    '''

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='localhost', port=8081, debug=True)

