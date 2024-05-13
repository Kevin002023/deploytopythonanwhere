# flask server


from flask import Flask, jsonify, request, abort, render_template
from brokerDAO import brokerDAO

#create flask application 
app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Landing Page</title>
        <style>
            /*changing font/formatting */
            body {
                background-color: #00FFFF;
                font-family: Arial, sans-serif;
                color: #006400; /* Text color */
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                height: 100vh;
            }
            .heading {
                color: #008B8B; /* Heading color */
            }
            .content {
                font-size: 16px;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <h1 class="heading">Welcome to O'Leary Insurance Ltd</h1>
        <br/>
        <div class ="content">
            <p>To see a complete list of brokers distributing our product please click <a href="/broker_list.html">here</a></p>
            <p>Alternatively you can find a broker near you <a href="/find_my_broker.html">here</a></p> 
    </body>
    </html>    
    """
#return all brokers

@app.route('/brokers')
def getAll():
    #print("in getall")
    results = brokerDAO.getAll()
    sorted_results = sorted(results, key=lambda x: x['ID'])
    return jsonify(sorted_results)

#return specific broker by ID

@app.route('/brokers/<int:id>')
def findById(id):
    foundBroker = brokerDAO.findByID(id)
    return jsonify(foundBroker)

@app.route('/brokers', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    broker = {
        "Name": request.json['Name'],
        "Address": request.json['Address'],
        "County": request.json['County'],
        "Phone": request.json['Phone'],
        "Web": request.json['Web'],
    }
    addedbroker = brokerDAO.create(broker)
    
    return jsonify(addedbroker), 201 # create status code

@app.route('/brokers/<int:id>', methods=['PUT'])
def update(id):
    #error message if an invalid id is provided
    foundBroker = brokerDAO.findByID(id)
    if not foundBroker:
        abort(404) 
    
    #error message if the input isnt json
    if not request.json:
        abort(400)
        
    reqJson = request.json
    if 'Phone' in reqJson and type(reqJson['Phone']) is not int:
        abort(400)

    if 'Name' in reqJson:
        foundBroker['Name'] = reqJson['Name']
    if 'Address' in reqJson:
        foundBroker['Address'] = reqJson['Address']
    if 'County' in reqJson:
        foundBroker['County'] = reqJson['County']
    if 'Phone' in reqJson:
        foundBroker['Phone'] = reqJson['Phone']
    if 'Web' in reqJson:
        foundBroker['Web'] = reqJson['Web']
    
    brokerDAO.update(id,foundBroker)
    return jsonify(foundBroker)

@app.route('/brokers/<int:id>' , methods=['DELETE'])
def delete(id):
    brokerDAO.delete(id)
    return jsonify({"done":True})

@app.route('/find_my_broker')
def findBroker():
    county= request.args.get('county')
    localBroker = brokerDAO.findByCounty(county)

    if localBroker is None:
        return jsonify({"error": "No brokers found for the specifed county."}), 404
    sorted_localBroker = sorted(localBroker, key=lambda x: x['ID'])
    return jsonify(sorted_localBroker)

if __name__ == '__main__' :
    app.run(debug= True)