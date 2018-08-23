from flask import Flask
from flask import render_template, request

from CollationParser.collationParser import CollationParser

app = Flask(__name__)

@app.route('/', methods= ['GET'], strict_slashes=False)
def serve():

    return render_template('index.html')

@app.route('/parse', methods=['GET', 'POST'])
def process_data():
    """
    Process a collation formula from input in template. 
    """

    collateformula = request.args.get('data')
    parser = CollationParser(verbose=True)

    # result
    folia, resultlist = parser.parse(collateformula, use_parselist=True)

    resultlist = [{k:v for k,v in e.items() if v} for e in resultlist]

    return render_template('index.html', result=resultlist, folia=folia, collatieformule=collateformula)

@app.route('/result_ppn', methods=['POST'])
def process_ppn():
    """
    Process a collation formula from a sparql request givenin the web interface by ppn. 
    """

    parser = CollationParser(verbose=True)
    collateformula = fetch_ppn(request.form['ppn'])

    # result
    folia, resultlist = parser.parse(collateformula, use_parselist=True)

    resultlist = [{k:v for k,v in e.items() if v} for e in resultlist]

    return render_template('index.html', result=resultlist, folia=folia, collatieformule=collateformula)

def fetch_ppn(ppn):
    """

    """

    from SPARQLWrapper import SPARQLWrapper, JSON
    ENDPOINT_URL = 'http://openvirtuoso.kbresearch.nl/sparql'

    sparql = SPARQLWrapper(ENDPOINT_URL)

    sqlquery = """

    SELECT ?collatie WHERE {{

        kbc:{ppn} dcterms:extent ?formaat, ?collatie .

        FILTER (?formaat != ?collatie ) .
        FILTER regex(?formaat, "^[0-9]{{1,2}}°", "i") .
    }}
    """.format(ppn=ppn)

    sparql.setQuery(sqlquery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # {'head': {'link': [], 'vars': ['collatie']}, 'results': {'bindings': [{'collatie': {'value': '*`SUP`8`LO` A-S`SUP`8`LO` (S8 blank)', 'type': 'literal'}}], 'distinct': False, 'ordered': True}}

    result = results['results']['bindings'][0]['collatie']['value']

    return result

if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0')
    #socketio.run(app)

