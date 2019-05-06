import numpy as np
import plotly
from Bio import Phylo
import numpy as np
import plotly.graph_objs as go
import ipywidgets as ipw
import plotly.plotly as py
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import Image

import plotly.tools as tls
def create_rectangular_tree():
    tree = Phylo.read('new.xml', 'phyloxml')
    traverse_order = 'preorder'
    def get_x_coordinates(tree):
        # Associates to  each clade a x-coord.
        # returns a dict {clade: x-coord}, i.e the key is a clade, and x-coord its value
        
        xcoords = tree.depths()
        # tree.depth() maps tree clades to depths (by branch length).
        # returns a dict {clade: depth} where clade runs over all Clade instances of the tree,
        # and depth is the distance from root to clade
        
        # If there are no branch lengths, assign unit branch lengths
        if not max(xcoords.values()):
            xcoords = tree.depths(unit_branch_lengths=True)
        return xcoords
    
    def get_y_coordinates(tree, dist=1.3):
        # y-coordinates are   multiple of dist (i*dist below); 
        # dist: vertical distance between two consecutive leafs; it is chosen such that to get a tree of 
        # reasonable height 
        # returns  a dict {clade: y-coord}
            
        maxheight = tree.count_terminals()#Counts the number of tree leafs.
    
        ycoords = dict((leaf, maxheight - i*dist) for i, leaf in enumerate(reversed(tree.get_terminals())))
        def calc_row(clade):
                for subclade in clade:
                    if subclade not in ycoords:
                        calc_row(subclade)
                ycoords[clade] = (ycoords[clade.clades[0]] +
                                ycoords[clade.clades[-1]]) / 2

        if tree.root.clades:
            calc_row(tree.root)
        return ycoords
    x_coords = get_x_coordinates(tree)
    y_coords = get_y_coordinates(tree)
    def get_clade_lines(orientation='horizontal', y_curr=0, x_start=0, x_curr=0, y_bot=0, y_top=0,
                        line_color='rgb(25,25,25)', line_width=0.5):
        # define a Plotly shape of type 'line', for each branch
        
        branch_line = dict(type= 'line',
                        layer='below',
                        line=dict(color=line_color, 
                                    width=line_width)
                        )
        if orientation == 'horizontal':
            branch_line.update(x0=x_start,
                            y0=y_curr,
                            x1=x_curr,
                            y1=y_curr)
        elif orientation == 'vertical':
            branch_line.update(x0=x_curr,
                            y0=y_bot,
                            x1=x_curr,
                            y1=y_top)
        else:
            raise ValueError("Line type can be 'horizontal' or 'vertical'")
        
        return branch_line    
            
        

    def draw_clade(clade, x_start,  line_shapes,  line_color='rgb(15,15,15)', line_width=1):
        # defines recursively  the tree  lines (branches), starting from the argument clade
        
        x_curr = x_coords[clade]
        y_curr = y_coords[clade]
    
        # Draw a horizontal line 
        branch_line=get_clade_lines(orientation='horizontal', y_curr=y_curr, x_start=x_start, x_curr=x_curr,  
                                    line_color=line_color, line_width=line_width)
    
        line_shapes.append(branch_line)
    
        if clade.clades:
            # Draw a vertical line connecting all children
            y_top = y_coords[clade.clades[0]]
            y_bot = y_coords[clade.clades[-1]]
        
            line_shapes.append(get_clade_lines(orientation='vertical', x_curr=x_curr, y_bot=y_bot, y_top=y_top,
                                            line_color=line_color, line_width=line_width))
        
            # Draw descendants
            for child in clade:
                draw_clade(child, x_curr, line_shapes)
        
    
    line_shapes = [] 
    draw_clade(tree.root, 0, line_shapes, line_color='rgb(25,25,25)', line_width=1)
    my_tree_clades = x_coords.keys()
    X = [] # list of nodes x-coordinates
    Y = [] # list of nodes y-coords
    text = [] #list of text to be displayed on hover over nodes

    for cl in my_tree_clades:
        X.append(x_coords[cl])
        Y.append(y_coords[cl])
        text.append(cl.name)
      
    intermediate_node_color = 'rgb(100,100,100)'
    nodes = dict(type='scatter',
                x=X,
                y=Y,
                mode="markers+text",
                marker=dict(color='rgb(200,20,20)', 
                            size=5),
                textposition="top left",
                opacity=1.0,
                text=text,
                hoverinfo='text'
                )

    layout = dict(title='Phylogenetic Tree',
                  font=dict(family='Balto', size=14),
                  width=700,
                  height=750,
                  autosize=False,
                  showlegend=False,
                  xaxis=dict(visible=False),
                  yaxis=dict(visible=False),
                  hovermode='closest',
                  plot_bgcolor='rgb(245,245,245)',
                  margin=dict(t=75),
                  shapes=line_shapes 
                  )
    fig = go.FigureWidget(
        data=[nodes], layout=layout)
    tls.set_credentials_file(username='madhushani', api_key='MKmrO7OfxfEvrQlkl2TJ')
    py.plot(fig, filename='rectangular_phyloxml',auto_open=False)

    tls.get_embed('https://plot.ly/~madhushani/4/phylogenetic-tree/')

