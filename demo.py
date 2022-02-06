#%%

from entropylab import *
from entropylab.api.plot import CirclePlotGenerator,LinePlotGenerator, ImShowPlotGenerator
from entropylab.api.data_writer import PlotSpec

from mock_instruments import MockScope
import numpy as np

from plots_library import LinfitPlotGenerator

db=SqlAlchemyDB(path='.')
labResources = ExperimentResources(db)    



#%% one node
def node_operation():
    return {'res':[1,2,3,6]}


node1 = PyNode(label="first_node", program=node_operation,output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1}, story="run_a") 

handle = experiment.run()



#%% one node with manual plot
def node_operation(context: EntropyContext):
    micro = 1e-6
    data = [
            [
                1 * micro,
                2 * micro,
                3 * micro,
                4 * micro,
                5 * micro,
                6 * micro,
                7 * micro,
                8 * micro,
            ],
            [0, 1, 2, 3, 4, 5, 6, 7],
        ]
    context.add_plot(
        PlotSpec(
            label="plot",
            story="created this plot in experiment",
            generator=CirclePlotGenerator,
        ),
        
        data=data,
    )
    
    context.add_plot(
        PlotSpec(
            label="plot2",
            story="created this plot in experiment",
            generator=LinePlotGenerator,
        ),
        
        data=data,
    )

    return {'res':data}


node1 = PyNode(label="first_node", program=node_operation,output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1}, story="run_a") 

handle = experiment.run()


#%% plot with overlay 
def node_operation():
    return {'res':[1,2,3,6]}


node1 = PyNode(label="first_node", program=node_operation,output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1}, story="run_a") 

handle = experiment.run()



#%% one node with overlay
def node_operation(context: EntropyContext):
    micro = 1e-6
    data = [
            np.linspace(0,10,100),
            np.linspace(0,10,100)+np.random.random(100)*5,

        ]

    context.add_plot(
        PlotSpec(
            label="plot",
            story="created this plot in experiment",
            generator=LinfitPlotGenerator,

        ),

        data=(data, {'xlabel':'my_x2','ylabel':'my_y'})
    )
    
    context.add_plot(
        PlotSpec(
            label="plot2",
            story="created this plot in experiment",
            generator=LinePlotGenerator,
        ),
        
        data=data,
    )

    return {'res':data}


node1 = PyNode(label="first_node", program=node_operation,output_vars={'res'})

experiment = Graph(resources=labResources, graph={node1}, story="run_a",label="meeeee2")

handle = experiment.run()


#%% two connected nodes

def node_with_input(x):
    return {'res':x+1}
node1 = PyNode(label="first node", program=lambda : {'res':np.cos(np.linspace(0,3))},output_vars={'res'})
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
    return {'res':[0,1,2,3,4]}

node1 = PyNode(label="first_node", program=work_with_scope,output_vars={'res'})
experiment = Graph(resources=labResources, graph={node1}, story="a scope",label='scope') 
handle = experiment.run()




# %%
