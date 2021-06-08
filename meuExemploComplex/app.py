from flask import Flask, render_template

import plotly.graph_objs as go
import pandas as pd
from plotly.offline import plot
import plotly
import plotly.express as px
import json             
import numpy as np     
                    
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj) 

app = Flask(__name__)
#decorator para a homepage
@app.route('/')
def index():
    return 'Bem vindo!'

@app.route('/graph')
def graph():

    df = pd.read_csv('letter.csv')

    fig = px.pie(df.iloc[:,-2], values= df.iloc[:,-1], names= df.iloc[:,0], title='Porcentagem de letras nas palavras de língua inglesa')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # converte em string (apresentado no slide)
    return render_template('graph.html',
                           ids='letters',
                           graphJSON=graphJSON)


@app.route('/table')
def table():
    df = pd.read_csv('letter.csv')

    #meas = [dffinal.iloc[i].to_dict() for i in range(dffinal.shape[0])]
    meas = [list(map(str, df.iloc[i].values)) for i in range(df.shape[0])]  
    #meas = {'data': meas}
    ddffinal = json.dumps(meas, cls=NpEncoder)
    return render_template('table.html',
                           dffinal=ddffinal)



if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
