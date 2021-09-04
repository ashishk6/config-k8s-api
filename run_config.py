from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

configs=[]

"""Recursively find the root of in dict d """
def find(element, json):
    keys = element.split('.')
    rv = json
    for key in keys:
        rv = rv[key]
    return rv

@app.route('/configs', methods=['GET'])
def getConfigs():
    my_dict = {}
    my_dict['configs']=configs
    return (my_dict)

@app.route('/configs', methods=['POST'])
def createConfigs():
    my_dict = {}
    request_data = request.get_json()
    print(request_data)
    if {"name", "metadata"} <= request_data.keys():
    #if request_data['name'] and request_data['metadata']:
        configs.append(request_data)
    else:
        my_dict['error']='Not a valid input !!'
        return (my_dict)
    my_dict['configs']=configs
    return (my_dict) 

@app.route('/configs/<name>', methods=['GET'])
def getNameConfigs(name):
    temp=[]
    my_dict = {}
    for i in configs:
        if i['name']==name:
            temp.append(i)
    my_dict['configs']=temp
    return (my_dict)

@app.route("/configs/<name>", methods=["DELETE"])
def deleteConfig(name):
    temp=[]
    my_dict = {}
    result=getNameConfigs(name)
    if len(result['configs'])<1:
        my_dict['message']='No element found !!'
        return(my_dict)
    else:
        for i in range(len(configs)):
            if configs[i]['name']==name:
                temp.append(configs.pop(i))
    my_dict['configs']=temp
    return (my_dict)

@app.route("/configs/<name>", methods=["PUT"])
def updateConfig(name):
    temp=[]
    my_dict = {}
    result=getNameConfigs(name)
    if len(result['configs'])<1:
        my_dict['message']='No element found !!'
        return(my_dict)
    else:
        for i in range(len(configs)):
            if configs[i]['name']==name:
                request_data = request.get_json()
                if {"name", "metadata"} <= request_data.keys():
                #if request_data['name'] and request_data['metadata']:
                    configs[i]['metadata']=request_data['metadata']
                else:
                    my_dict['message']='Not a valid input !!'
                    return (my_dict)
    my_dict['configs']=configs
    return (my_dict)


@app.route('/search', methods=['GET'])
def getFieldSelectorConfigs():
    temp=[]
    my_dict = {}
    encoding = 'utf-8'
    x1=(request.query_string.decode(encoding))
    y1=x1.split('=')
    z1=x1.split('.')
    key_val=(z1[len(z1)-1].split('='))
    for x in configs:
        final_res=(find(y1[0],x))
        print(final_res)
        if final_res==key_val[1]:
            temp.append(x)
    if len(temp)>0:
        my_dict['configs']=temp
        return (my_dict)
    else:
        my_dict['message']='No element found !!'
        return(my_dict)


if __name__ == '__main__':
    PORT=os.environ.get('SERVE_PORT')
    #PORT="5000"
    if PORT is not None:
        app.run(host= '0.0.0.0',debug=True, port=PORT)
