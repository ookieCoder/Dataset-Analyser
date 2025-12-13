from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pandas as pd
import matplotlib.pyplot as plt

def run_smote(df, target, out_dir):
    numeric_df = df.select_dtypes(include="number")
    if target not in numeric_df.columns:
        return  # SMOTE only works on numeric targets

    X = numeric_df.drop(columns=[target])
    y = df[target].astype(int)

    # Before SMOTE
    y.value_counts().plot(kind="bar")
    plt.title("Before SMOTE")
    plt.savefig(f"{out_dir}/smote_before.png")
    plt.clf()

    sm = SMOTE(random_state=42)
    X_resampled, y_resampled = sm.fit_resample(X, y)

    # After SMOTE
    pd.Series(y_resampled).value_counts().plot(kind="bar")
    plt.title("After SMOTE")
    plt.savefig(f"{out_dir}/smote_after.png")
    plt.clf()

    # Train-test split for demonstration
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.3, random_state=42
    )

    # Save resampled dataset
    pd.concat([X_train, y_train], axis=1).to_csv(f"{out_dir}/smote_train.csv", index=False)
    pd.concat([X_test, y_test], axis=1).to_csv(f"{out_dir}/smote_test.csv", index=False)

    print("\nSMOTE oversampling completed.")
