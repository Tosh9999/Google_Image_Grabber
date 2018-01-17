from lib import app
from flask import request, render_template, url_for
from apiclient.discovery import build

@app.route('/')
@app.route('/search')
def index():
    return render_template('search.html')

@app.route('/searchResults', methods=['POST'])
def search_results():
    entry = request.form['searchTerms']
    search_terms = entry.split('\n')

    search_engine_id = request.form['search_engine_id']
    api_key = request.form['api_key']
    safe_search_level = request.form['safe_search_level']
    picture_rights = request.form['picture_rights']

    try:
        num_results_per_term = int(request.form['results_per_term'])
    except ValueError:
        num_results_per_term = 10


    service = build('customsearch', 'v1', developerKey=api_key)

    results_dictionary = {}
    for term in search_terms:
        res = service.cse().list(
            q=term,
            cx=search_engine_id,
            searchType='image',
            num=num_results_per_term,
            safe=safe_search_level,
            rights=picture_rights
        ).execute()
        results_dictionary[term] = res

    return render_template('results.html', results=results_dictionary)

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
