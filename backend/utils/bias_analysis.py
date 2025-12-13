import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_bias_analysis(df, target, out_dir):
    # CLASS DISTRIBUTION
    class_plot = df[target].value_counts()
    class_plot.plot(kind="bar")
    plt.title(f"Class Distribution for {target}")
    plt.savefig(f"{out_dir}/class_distribution.png")
    plt.clf()

    # CORRELATION MATRIX
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] > 1:
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Correlation Matrix")
        plt.savefig(f"{out_dir}/correlation_matrix.png")
        plt.clf()

    # DETECT SENSITIVE FEATURES
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    sensitive_cols = [c for c in cat_cols if df[c].nunique() <= 10 and c != target]

    report = []
    report.append(f"Dataset Shape: {df.shape}")
    report.append(f"Target Column: {target}")
    report.append("\nClass Distribution:\n" + str(df[target].value_counts()))

    # BIAS REPORTS
    for col in sensitive_cols:
        group_counts = df.groupby([col, target]).size().unstack(fill_value=0)
        report.append(f"\nBias Analysis for {col}:\n{group_counts}")

        group_counts.plot(kind="bar")
        plt.title(f"{col} vs {target}")
        plt.savefig(f"{out_dir}/sensitive_{col}_bias.png")
        plt.clf()

    with open(f"{out_dir}/bias_report.txt", "w") as f:
        f.write("\n\n".join(report))

    print(f"\nBias analysis completed. Sensitive columns detected: {sensitive_cols}")
    return sensitive_cols
