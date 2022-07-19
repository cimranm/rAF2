#! /usr/bin/env python3
"""Load graphs from list of PDB files"""


"""
usage: python load.py ../datasets/yeast_full.txt structures/yeast-AF2 saved_graphs
"""



# Pomegranate
from protein.phosphosite import get_surface_motif
from validate import get_database

import pickle
import pathlib
from graphein.protein.graphs import construct_graph
from graphein.protein.config import ProteinGraphConfig
from graphein.protein.edges.distance import *	

from graphein.protein.config import DSSPConfig
from graphein.protein.features.nodes import rsa

from pathlib import Path

import click as c



import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


import os
import urllib as ul

from validate import get_database

# TODO: use Path types instead of strs
def load_graphs(
    pdb_path: str = None,       # directory containing local pdb files
    psite_list: str = None,          # path to file containing list of psites
    radius_threshold: float = 10.0,
    rsa_threshold: float = 0.0,
    verbose: bool = True,
):

    psite_path = Path(psite_list)
    if not psite_path.is_file():
        raise ValueError(f"No such file {psite_list}")
    
    df = pd.read_csv(psite_path, sep='\t', header=0)

    
    accs = [a for a in df['acc']]

    # remove duplicates
    accs = list(set(accs))
    
    # Default directory
    if pdb_path == None:
        pdb_path = STRUCTURE_PATH + "/yeast"

    if not os.path.isdir(pdb_path):
        raise ValueError(f"Path {pdb_path} is not a directory.")
    
    # for each entry: 
    for acc in accs:

        filename = f"{pdb_path}/{acc}.pdb" 
        
        if os.path.exists(filename):
            if verbose:
                print(f"{filename} already exists.")

        else:

            #print(f"No such file {filename}")
            

            filename = acc + ".pdb"

            if get_database(acc) == 'uniprot':
                print(f"Downloading {acc} from AF2...", end=" ")
                try:
                    url = f"https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v2.pdb"
                    ul.request.urlretrieve(url, pdb_path+f"/{filename}")
                    if verbose:
                        print("DOWNLOADED.")
                except:
                    if verbose:
                        print(f"FAILED to download from AF2.")
            else:
                if verbose:
                    print(f"Skipping non-uniprot ID '{acc}'.")
        
    pdb_dir = pdb_path 

    # Each phosphosite
    graphs = {}
    edge_fns = [
            #add_aromatic_interactions,
            add_hydrophobic_interactions,
            #add_aromatic_sulphur_interactions,
            #add_cation_pi_interactions,
            #add_disulfide_interactions,
            #add_hydrogen_bond_interactions,
            #add_ionic_interactions,
            add_peptide_bonds
        ]
    config = ProteinGraphConfig(
        edge_construction_functions=edge_fns, 
        graph_metadata_functions=[rsa], 
        dssp_config=DSSPConfig(),
        pdb_dir=pdb_dir,
    )
    for idx, row in df.iterrows():

        #print(index, row['acc'], row['position'], row['code'])
        if type(row['kinases']) == str:
            kinase = row['kinases']
        else:
            kinase = "UNKNOWN"
        #print(f"row kinase: {type(row['kinases'])}")
        index = idx
        #if True:
        try:
            pos = row['position'] 
            pdb_path = f"{pdb_dir}/{row['acc']}.pdb"
            g = construct_graph(config, pdb_path=pdb_path) 
            res = list(g.nodes())[pos-1]

            psite = g.nodes(data=True)[res]
            g = get_surface_motif(g, site=pos) # use default thresholds 
            g.name += f" @ {row['position']} {row['code']}"

            graph = {'graph': g, 'kinase': kinase, 'psite': psite, 'res': res}
            graphs[index] = graph

            if verbose:
                print(f"[{index}] Graph {graphs[index]['graph'].name}, RES: {res}")
            
        except:
            print(f"[FAILED] Graph")
            
    return graphs

@c.command()
@c.argument('phosphosite', nargs=1)
@c.argument('structures', nargs=1)
@c.argument('graphs', nargs=1)
@c.option(
    "-r",
    "--radius",
    help="The threshold radius of the motif",
    type=float,
    default=10.0,
)
@c.option(
    "--rsa",
    "--rsa-threshold",
    help="The RSA threshold of the motif",
    type=float,
    default=0.0,
)
def main(
    phosphosite, 
    structures,
    graphs,
    radius,
    rsa,
    ):

    # TODO: ensure that psite is always included; regardless of RSA

    graph_path = Path(graphs)
    if not graph_path.is_dir():
        raise ValueError(f"No such directory {graph_path}")
    
    filename = "graph_objects"
    out_path = os.path.join(graph_path, filename)

    # TODO: check if filename exists.  Prompt for new one / overwrite. 

    print(f"Output file is {out_path}.")
    

    graphs = load_graphs(
        pdb_path = structures,
        psite_list = phosphosite,
        radius_threshold=radius,
        rsa_threshold=rsa,
    )

    print(f"Loaded {len(graphs.keys())} graphs with radius {radius} and RSA {rsa}.")
    
    # Save graphs to file
    print("Saving graphs...", end=" ")
    outfile =  open(out_path, 'wb')
    pickle.dump(graphs, outfile)
    outfile.close()
    print("DONE.")

    return

    # Unpickle
    infile = open(in_path,'rb')
    loaded_graphs = pickle.load(infile)
    infile.close()




    



if __name__ == "__main__":
    main()