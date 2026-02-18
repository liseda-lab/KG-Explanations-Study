# KG-Explanations-Study
**Explaining Scientific Hypotheses in Drug Development with Knowledge Graphs**  
Resources, code, and data for our paper here.

---

##  Overview

We compare four KG-based explanation methods—**Minerva**, **PoLo**, **REx** and an ontology-free variant **RExLight**—across two drug-discovery tasks:

1. **Drug Repurposing**  
2. **Drug–Target Interaction**

Our evaluation combines:
- **Quantitative link-prediction metrics** (MRR, Hits@k)  
- **A user study** with 11 biomedical researchers rating explanations on scientific validity, completeness, and relevance. (Experts' qualitative and quantitative answers are present in the **evaluation/responses** directory)
- **Qualitative feedback** (topic modeling & visualization)

---

##  Datasets

| Graph    | Source                                                         |
| -------- | -------------------------------------------------------------- |
| **Hetionet**  | https://github.com/hetio/hetionet                           |
| **PrimeKG**   | https://github.com/mims-harvard/PrimeKG                     |
| **OREGANO**   | https://gitub.u-bordeaux.fr/erias/oregano                   |

---

##  Dataset Statistics

The table below reports overall graph size, then train/validation/test splits for each task.

| Category                    | Metric   | Hetionet  | PrimeKG   | OREGANO   |
| --------------------------- | -------- | --------- | --------- | --------- |
| **Global Stats**            | Triples  | 4 499 850 | 8 096 649 | 1 571 714 |
|                             | Entities |  45 158   | 129 313   |  98 602   |
|                             | Relations|    48     |    33     |    38     |
| **Drug Repurposing**        | Train    |    483    |  7 510    |    117    |
|                             | Valid    |    121    |    939    |     29    |
|                             | Test     |    151    |    939    |     63    |
| **Drug–Target Interaction** | Train    |  5 670    |    —      |  84 214   |
|                             | Valid    |  2 430    |    —      |  36 093   |
|                             | Test     |  3 471    |    —      |  51 560   |

---

##  Methods

We include the configuration files and saved models here to enable reproducibility (all hyperparameters were default); full implementations instructions are in their upstream repositories:

| Method     | GitHub                                          |
| ---------- | ----------------------------------------------- |
| **Minerva**  | https://github.com/shehzaadzd/MINERVA           |
| **PoLo**     | https://github.com/liu-yushan/PoLo               |
| **REx**      | https://github.com/liseda-lab/REx                |


| Method | GitHub| Reasoning / model | Explanation output | Ontology in explanation | How paths are guided / selected |
|---|---|---|---|---|---|
| MINERVA (Das et al., 2017) | https://github.com/shehzaadzd/MINERVA   | RL multi-hop traversal (LSTM policy) | Single path | No | Reward mainly for reaching correct target (predictive success), no explicit interpretability constraints |
| PoLo (Liu et al., 2021) |https://github.com/liu-yushan/PoLo | MINERVA + logical-rule guidance | Single path | No | Adds rule-based reward: encourages traversals aligned with predefined logical rules (with confidence scores) |
| REx (Nunes et al., 2025) | https://github.com/liseda-lab/REx  |RL with scientific explainability objectives | Multiple paths | Yes | Dual reward balances fidelity + relevance (information content), early stopping for simplicity, optional ontology expansions (NCIT/ChEBI for repurposing; GO for DTI) |
| RExLight | REx ablation | REx| Multiple paths | No | Same mechanism as REx, but removes ontology-derived nodes to isolate the effect of semantic abstraction |


---


## Other Analysis 
### Inter-Annotator Agreement
To assess how consistently experts applied each criterion, Inter-annotator agreement was assessed with the Intraclass Correlation Coefficient $ICC(3,k)$~\cite{shrout1979intraclass}, a two-way mixed-effects, consistency model that estimates how reliably a fixed set of raters assign the same score to the same item. In drug repurposing, agreement was substantial for all three criteria (relevance 0.88, completeness 0.78, validity 0.72; bootstrap 95\% $CIs \leq \pm 0.06$). In drug–target interaction, consistency remained high for relevance (0.73) and for completeness (0.70) but fell to 0.36 for validity, with a wide bootstrap interval ($CI = [0.01, 0.51]$), indicating much greater uncertainty about what counts as biologically plausible for this task.


### Qualitative Feedback via Topic Modeling
To complement our quantitative evaluation and expert ratings, we analyzed free-text comments from participants using BERTopic with custom embeddings and clustering. This allowed us to extract recurring themes and concerns from user feedback across explanation methods.

We clustered the feedback using UMAP-reduced embeddings and HDBSCAN, with topic representations generated via KeyBERT. This helped reveal latent concerns such as biological plausibility, path length complexity, and relation interpretability.

<div align="center"> <img src="evaluation/topic_modeling/umap_visualization.png" alt="Topic Modeling UMAP" width="600"/> </div>
Each point in the plot represents a participant comment, colored by its assigned topic. Circle sizes reflect model confidence, while numeric labels correspond to the most salient keywords.

The script is available in evaluation/topic_modeling/create_topics.py, with results saved to Excel for further inspection.



## Repository Structure

```text
KG-Explanations-UserStudy/
│
├── datasets/                   # Preprocessed KGs for each task with train, test, dev plus labels 
│   ├── dataset_dr/
│   ├── dataset_dt/
│   └── datasets_labels/
│
├── systems/                # Configs files and saved models for methods for each KG
│   ├── config_files/
│   └── saved_models/
│
├── evaluation/             # User-study materials, aggregated results, plots, rates and written feedback
│   ├── user_study/
│   ├── responses/
│   ├── topic_modeling/
│   └── figures/
│
├── scripts/                # Data preprocessing, evaluation, visualization
│   ├── correlation.py
│   ├── evaluate.py
│   └── visualize.py
│
└── README.md               # ← You are here

```






