import decoupler as dc
import anndata as ad
import pandas as pd
import numpy as np

adata = ad.read_h5ad('/insomnia001/depts/morpheus/users/me2982/data/xenium_ovca_tutorial/data/tutadata_subset.h5ad')
progeny = dc.op.progeny(organism='human')

chunk_size = 5000
results = []

for i in range(0, adata.n_obs, chunk_size):
    print(f"Processing cells {i} to {min(i+chunk_size, adata.n_obs)}...")
    chunk = adata[i:i+chunk_size].copy()
    dc.mt.ulm(data=chunk, net=progeny)
    results.append(chunk.obsm['score_ulm'])

pathway_matrix = pd.concat(results)
pathway_matrix.index = adata.obs_names

pathways = ['EGFR', 'Androgen', 'Estrogen', 'JAK-STAT', 'VEGF', 'MAPK', 'PI3K', 'TGFb', 'NFkB', 'TNFa']
pathway_matrix[pathways].to_parquet('/insomnia001/depts/morpheus/users/me2982/data/xenium_ovca_tutorial/pathway_activation.parquet')
print("Saved successfully")
print(pathway_matrix.shape)
