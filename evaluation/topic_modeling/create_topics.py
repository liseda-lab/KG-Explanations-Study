#!/usr/bin/env python
# coding: utf-8


"""
Topic Modeling & Visualization Script
-------------------------------------
This script loads comments from an Excel file, applies BERTopic for clustering,
visualizes the results using UMAP, and exports results to an Excel file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patheffects as PathEffects
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN
import umap


def load_comments(filepath: str) -> list:
    df = pd.read_excel(filepath)
    return df["comment"].dropna().tolist(), df


def create_topic_model(comments: list) -> tuple:
    embedding_model = SentenceTransformer("all-mpnet-base-v2")
    vectorizer_model = CountVectorizer(stop_words="english")
    umap_model = umap.UMAP(n_neighbors=25, min_dist=0.0)
    hdbscan_model = HDBSCAN(min_cluster_size=5, min_samples=1)

    topic_model = BERTopic(
        representation_model=KeyBERTInspired(),
        embedding_model=embedding_model,
        vectorizer_model=vectorizer_model,
        verbose=True
    )

    topics, probs = topic_model.fit_transform(comments)
    embeddings = topic_model._extract_embeddings(comments, method="document")
    reduced_embeddings = umap_model.fit_transform(embeddings)

    return topic_model, topics, probs, reduced_embeddings


def map_topics(topic_model, topics) -> tuple:
    topic_info = topic_model.get_topic_info()
    mapped_ids, labels = {}, {}
    next_id = 1

    for _, row in topic_info.iterrows():
        tid = row["Topic"]
        if tid != -1:
            mapped_ids[tid] = next_id
            top_words = [word for word, _ in topic_model.get_topic(tid)][:3]
            labels[next_id] = ", ".join(top_words)
            next_id += 1

    return mapped_ids, labels


def plot_umap(df_umap, mapped_ids, labels, output_path: str = "umap_visualization.png"):
    pastel_colors = [
        "#7aaed6", "#d684a0", "#82b39b", "#d6a97c", "#a48cc7",
        "#70b7c7", "#c3a470", "#8aa96e", "#b68d84", "#91a8d0",
        "#c77c91", "#aab97e", "#c67f7f", "#a7a7c8", "#78b3aa"
    ]
    pastel_colors *= (len(labels) // len(pastel_colors) + 1)
    cmap = ListedColormap(pastel_colors[:len(labels)])

    plt.figure(figsize=(10, 8), dpi=300)
    mask = df_umap["topic"] != -1
    unique_topics = sorted(df_umap.loc[mask, "topic"].unique())

    plt.scatter(
        df_umap.loc[mask, "x"],
        df_umap.loc[mask, "y"],
        c=df_umap.loc[mask, "topic_mapped"],
        cmap=cmap,
        alpha=0.75,
        s=50 + df_umap.loc[mask, "probability"] * 100,
        edgecolors='white',
        linewidths=0.4
    )

    for topic_id in unique_topics:
        topic_mask = df_umap["topic"] == topic_id
        cx, cy = df_umap.loc[topic_mask, ["x", "y"]].mean()
        label_id = mapped_ids[topic_id]
        txt = plt.text(
            cx, cy, str(label_id),
            fontsize=12, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3')
        )
        txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])

    legend_elements = [
        plt.Line2D(
            [0], [0],
            marker='o',
            color='w',
            markerfacecolor=pastel_colors[i],
            markersize=10,
            label=f"Topic {mapped_ids[tid]}: {labels[mapped_ids[tid]]}"
        )
        for i, tid in enumerate(unique_topics)
    ]

    plt.legend(
        handles=legend_elements,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.05),
        fancybox=False,
        shadow=False,
        ncol=2,
        fontsize=9
    )
    plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.4)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    for spine in plt.gca().spines.values():
        spine.set_visible(True)
        spine.set_color('#cccccc')
        spine.set_linewidth(0.8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def export_results(df, df_umap, mapped_ids, labels, topics, output_excel: str):
    df_umap["topic_mapped"] = df_umap["topic"].map(mapped_ids)
    df_umap["comment"] = df["comment"]

    summary_data = []
    for tid in sorted(mapped_ids.keys()):
        mapped_id = mapped_ids[tid]
        topic_mask = df_umap["topic"] == tid
        example = df.loc[topic_mask, "comment"].iloc[0][:300]
        count = topic_mask.sum()
        summary_data.append({
            "Topic": mapped_id,
            "Top Keywords": labels[mapped_id],
            "Example Comment": example,
            "Count": count
        })

    summary_df = pd.DataFrame(summary_data)
    umap_export = df_umap[["x", "y", "topic_mapped", "probability", "comment"]].rename(columns={"topic_mapped": "Topic"})

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Topic Summary", index=False)
        umap_export.to_excel(writer, sheet_name="UMAP Coordinates", index=False)

    print("✅ Final UMAP + Excel export complete with Topic IDs starting at 1.")


def main():
    input_file = "comments.xlsx"
    output_plot = "umap_visualization.png"
    output_excel = "topic_umap_output.xlsx"

    comments, df = load_comments(input_file)
    topic_model, topics, probs, reduced_embeddings = create_topic_model(comments)

    df_umap = pd.DataFrame(reduced_embeddings, columns=["x", "y"])
    df_umap["topic"] = topics
    df_umap["probability"] = probs

    mapped_ids, labels = map_topics(topic_model, topics)

    df_umap["topic_mapped"] = df_umap["topic"].map(mapped_ids)
    plot_umap(df_umap, mapped_ids, labels, output_plot)
    export_results(df, df_umap, mapped_ids, labels, topics, output_excel)


if __name__ == "__main__":
    main()
