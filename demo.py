#%%

from entropylab import *
from entropylab.api.plot import CirclePlotGenerator,LinePlotGenerator, ImShowPlotGenerator
from entropylab.api.data_writer import PlotSpec

from mock_instruments import MockScope
import numpy as np

db=SqlAlchemyDB(path='.')
labResources = ExperimentResources(db)    



#%% one node
def node_operation():
    return {'res':[1,2,3,4]}


node1 = PyNode(label="first_node", program=node_operation,output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1}, story="run_a") 

handle = experiment.run()



#%% two connected nodes

def node_with_input(x):
    return {'res':x+1}
node1 = PyNode(label="first node", program=lambda : {'res':np.array([1,2,3,4])},output_vars={'res'})
node2 = PyNode(label="second node", program=node_with_input, input_vars={'x':node1.outputs["res"]},output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1,node2}, story="run_a") 
handle = experiment.run()

experiment.dot_graph()
#%% nodes with instruments

labResources.add_temp_resource(
        "scope_1", MockScope("1.1.1.1","")
    )
#%%
def work_with_scope(context:EntropyContext):
    scope = context.get_resource('scope_1')
    scope.connect()
    scope.get_trig()
    return {'res':[0]}

node1 = PyNode(label="first_node", program=work_with_scope,output_vars={'res'})
experiment = Graph(resources=labResources, graph={node1}, story="a scope",label='scope') 
handle = experiment.run()




# %%
