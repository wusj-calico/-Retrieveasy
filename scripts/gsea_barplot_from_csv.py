#!/usr/bin/env python3
"""
gsea_barplot_from_csv.py

Create a horizontal bar plot of NES (x) vs gene_set_name (y) and use padj to color bars.

Usage:
  python3 scripts/gsea_barplot_from_csv.py --csv <file.csv> --out <out.png> --top 25

Creates the output file and a colorbar showing -log10(padj).
"""
import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


def main():
    p = argparse.ArgumentParser(description="GSEA NES horizontal bar plot with padj heatmap")
    p.add_argument("--csv", required=True, help="Path to GSEA CSV file")
    p.add_argument("--out", default="plots/gsea_barplot.png", help="Output image path")
    p.add_argument("--top", type=int, default=25, help="Top N gene sets to display (by abs NES)")
    p.add_argument("--sort", choices=["abs","NES","padj"], default="abs", help="Sort by abs (default), NES, or padj")
    p.add_argument("--cmap", default="Reds_r", help="Colormap for padj -> color mapping")
    args = p.parse_args()

    df = pd.read_csv(args.csv)

    # expected columns in this file
    gene_col = "gene_set_name"
    nes_col = "NES"
    padj_col = "padj"

    if gene_col not in df.columns or nes_col not in df.columns or padj_col not in df.columns:
        print("ERROR: required columns not found. Found columns:", list(df.columns))
        return

    df = df[[gene_col, nes_col, padj_col]].copy()
    df = df.dropna(subset=[gene_col, nes_col, padj_col])
    df[nes_col] = pd.to_numeric(df[nes_col], errors="coerce")
    df[padj_col] = pd.to_numeric(df[padj_col], errors="coerce")
    df = df.dropna(subset=[nes_col, padj_col])

    if args.sort == "abs":
        df = df.reindex(df[nes_col].abs().sort_values(ascending=False).index)
    elif args.sort == "NES":
        df = df.reindex(df[nes_col].sort_values(ascending=False).index)
    else:
        df = df.reindex(df[padj_col].sort_values(ascending=True).index)

    df_top = df.head(args.top).copy()
    # reverse for plotting (largest at top)
    df_top = df_top.iloc[::-1]

    # compute significance mapping: -log10(padj)
    eps = 1e-300
    df_top["_sig"] = -np.log10(df_top[padj_col].clip(lower=eps))

    norm = mpl.colors.Normalize(vmin=df_top["_sig"].min(), vmax=df_top["_sig"].max())
    cmap = mpl.cm.get_cmap(args.cmap)
    colors = [cmap(norm(v)) for v in df_top["_sig"]]

    sns.set(style="whitegrid")
    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)

    fig_height = max(4, 0.35 * len(df_top))
    fig, ax = plt.subplots(figsize=(10, fig_height))

    y_labels = df_top[gene_col].astype(str)
    x_vals = df_top[nes_col].astype(float)
    y_pos = np.arange(len(df_top))

    bars = ax.barh(y_pos, x_vals, color=colors, edgecolor="k", linewidth=0.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=9)
    ax.set_xlabel("NES")
    ax.set_title("GSEA — NES by Gene Set (bar color = -log10(padj))")
    ax.axvline(0, color="gray", linewidth=0.6)

    # annotate NES numeric value to the right of bars
    maxabs = max(1e-6, np.max(np.abs(x_vals)))
    for i, xi in enumerate(x_vals):
        sign = 1 if xi >= 0 else -1
        ax.text(xi + sign * 0.02 * maxabs, i, f"{xi:.2f}", va="center", fontsize=8)

    # colorbar for padj (shows -log10(padj))
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", pad=0.02)
    cbar.set_label("-log10(padj)")

    plt.tight_layout()
    fig.savefig(args.out, dpi=300)
    print(f"Saved plot to {args.out}")


if __name__ == "__main__":
    main()
