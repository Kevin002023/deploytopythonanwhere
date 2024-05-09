# flask server


from flask import Flask, jsonify, request, abort
from brokerDAO import brokerDAO

#create flask application 
app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return "Hello, Kevin!"

#return all brokers

@app.route('/brokers')
def getAll():
    #print("in getall")
    results = brokerDAO.getAll()
    return jsonify(results)

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


if __name__ == '__main__' :
    app.run(debug= True)