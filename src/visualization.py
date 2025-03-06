import io
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_scatter(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(num_cols) < 2:
        raise ValueError("At least two numerical columns are required for a scatter plot.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], ax=ax)
    ax.set_title(f"Scatter Plot: {num_cols[0]} vs {num_cols[1]}")
    return fig

def plot_bar(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if not num_cols or not cat_cols:
        raise ValueError("At least one numerical and one categorical column are required for a bar plot.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=df[cat_cols[0]], y=df[num_cols[0]], ax=ax)
    ax.set_title(f"Bar Chart: {num_cols[0]} by {cat_cols[0]}")
    plt.xticks(rotation=45)
    return fig

def plot_line(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(num_cols) < 2:
        raise ValueError("At least two numerical columns are required for a line plot.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x=df.index, y=df[num_cols[0]], ax=ax)
    ax.set_title(f"Line Plot: {num_cols[0]} over Index")
    return fig

def plot_histogram(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        raise ValueError("At least one numerical column is required for a histogram.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df[num_cols[0]], kde=True, ax=ax)
    ax.set_title(f"Histogram of {num_cols[0]}")
    return fig

def plot_boxplot(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        raise ValueError("At least one numerical column is required for a boxplot.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(y=df[num_cols[0]], ax=ax)
    ax.set_title(f"Box Plot of {num_cols[0]}")
    return fig

def plot_heatmap(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(num_cols) < 2:
        raise ValueError("At least two numerical columns are required for a heatmap.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig

def generate_pdf_report(df):
    """Generates a multi-page PDF report containing multiple visualizations."""
    pdf_buffer = io.BytesIO()
    # List of plotting functions to include in the PDF report
    plot_functions = [
        plot_scatter, 
        plot_bar, 
        plot_line, 
        plot_histogram, 
        plot_boxplot, 
        plot_heatmap
    ]
    with PdfPages(pdf_buffer) as pdf:
        for plot_func in plot_functions:
            try:
                fig = plot_func(df)
                pdf.savefig(fig)
                plt.close(fig)
            except Exception as e:
                print(f"Skipping {plot_func.__name__} due to error: {e}")
                continue
    pdf_buffer.seek(0)
    return pdf_buffer

def generate_best_viz(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(num_cols) == 0:
        raise ValueError("No numerical columns found for visualization.")
    fig, ax = plt.subplots(figsize=(10, 5))
    if len(num_cols) == 1:
        sns.histplot(df[num_cols[0]], kde=True, ax=ax)
        ax.set_title(f"Histogram of {num_cols[0]}")
    elif len(num_cols) == 2:
        sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], ax=ax)
        ax.set_title(f"Scatter Plot: {num_cols[0]} vs {num_cols[1]}")
    else:
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
    return fig
