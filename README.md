# Multimodal Latent Alignment

**By:** Marissa Esteban  
**Affiliation:** Woappi Lab / Dumitrascu Lab, Columbia University

---

## Project Goal

To reconstruct volumetric gene expression across serial tissue sections by integrating spatial transcriptomics (ST) and H&E histology. Specifically, we are building a model that:

1. Trains separate encoders for H&E patches and ST gene expression
2. Aligns them into a **shared latent space** where morphology and transcriptomics co-exist as comparable representations
3. Uses H&E images at unmeasured sections as direct spatial anchors — mapping them into the shared latent space to infer gene expression

Future Steps:
- integrate spatial context in embeddings and gene predictor

---

## Driving Question

> Given a shared latent space aligned between H&E and ST, how faithfully can H&E alone recover a position in that space — and is that fidelity sufficient to anchor 3D interpolation of gene expression between sections?

---

## Proof of Concept Roadmap

Before building the full architecture, I am first validating the key assumptions using existing tools:

**Step 1 — Generate aligned embeddings using SpatialFusion**  
SpatialFusion (Dann et al., 2026) trains a multimodal autoencoder (mAE) that aligns H&E embeddings (via UNI) and ST embeddings (via scGPT) into a shared 64-dimensional latent space. We use this as our alignment framework before building our own.

**Step 2 — Test whether H&E alone can predict gene expression**  
Using the three embeddings output by SpatialFusion (z_HE, z_ST, z_joint), I train a small MLP gene expression predictor and evaluate prediction quality (~/trainMLP.ipynb)

**Step 3 — Establish a quantitative baseline**  
Gap between z_HE and z_ST performance as a baseline?

---

## Repository Structure

```
multimodal-representation/
│
├── spatial_fusion/                  # Running SpatialFusion on our datasets
│   ├── xenium_ovca/                 # OvCa Xenium tutorial data (from SpatialFusion paper)
│   │   └── notebooks for embedding extraction and visualization
│   └── unwounded_woappi/            # Woappi lab Visium HD mouse wound healing data
│       └── notebooks for embedding extraction (note: requires mouse→human gene remapping)
│
├── gexp_prediction/                 # Gene expression prediction from embeddings
│   └── trainMLP.ipynb               # Full pipeline: generate embeddings → preprocess → train MLP → evaluate
│
└── exploration/                     # Learning notebooks (PyTorch, CNNs, tutorials)
    └── not part of main pipeline
```

spatial_fusion: folder that runs SpatialFusion on two main datasets. Includes benchmarking scripts and visualizations from SpatialFusion paper.

---

## Methods

**Embeddings:** Generated using SpatialFusion's multimodal autoencoder. H&E patches (256×256px) encoded via frozen UNI (1536-dim), gene expression encoded via frozen scGPT (512-dim), both projected into a shared 64-dim latent space via a trained mAE.

**Gene expression prediction:** Small MLP (3 hidden layers × 256 units, LeakyReLU, Softplus output) trained with AdamW (lr=1e-4, weight_decay=0.01), batch size 128, early stopping patience 20. Targets: log-normalized gene expression (CP10K + log1p) per-gene robust-scaled to [0,1]. Train/val split: 80/20 on spot indices.

**Evaluation:** Mean Pearson and Spearman correlation per gene across validation spots.

**Data:**
- OvCa Xenium tutorial crop: 46,691 cells × 5,101 genes (proof of concept dataset)
- NEXT: [Full OVCA data](https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-ovarian-cancer)
- Unwounded Woappi Visium HD: ~113k spots × 19k genes (mouse; requires ortholog remapping? Or geneformer mouse foundation model)

---

## Known Limitations / Open Questions

- Current results are on a crop of the OvCa tutorial data — full tissue run pending
- SpatialFusion foundation models (UNI, scGPT) are trained on human data; applying to mouse Woappi data requires mouse→human gene name remapping OR different gexp foundation model
- Unwounded mouse data is at spot level (256×256px patches, ~128µm physical at 0.5 MPP for Visium HD) — each patch covers ~16×16 Visium HD bins, creating a scale mismatch between the image embedding and individual bin-level gene expression labels
- Not including spatial context in embeddings or in prediction

---

## Key References

- Dann et al. (2026). *SpatialFusion: A lightweight multimodal foundation model for pathway-informed spatial niche mapping.* bioRxiv.
- Chen et al. (2026). *sCellST: predicting single-cell gene expression from H&E images.* Nature Communications.
