# # #
# بِسْمِ ٱللّٰهِ ٱلرَّحْمٰنِ ٱلرَّحِيمِ
# Bismillāh ir-raḥmān ir-raḥīm
# 
# In the name of God, the Most Gracious, the Most Merciful
# Em nome de Deus, o Clemente, o Misericordioso
# # #
# # #


# #
# Imports
import os
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Literal, Any
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

OutputFormat = Literal['.md', '.txt', '.html']
def document_model(
    model: LogisticRegression | RandomForestClassifier,
    model_name: str,
    model_metadata: dict[str, Any],
    model_features: list[str],
    x: pd.DataFrame,
    y: pd.Series,
    output_format: OutputFormat = '.md',
    timestamp: bool = False
) -> None:
    # Helper functions to format dataframe and series documentation strings
    def format_model_input_summary(df: pd.DataFrame) -> str:
        first_row = df.iloc[0]

        # Determine column widths
        col1_width = max(len("Column Name"), *(len(col) for col in df.columns))
        values = [str(first_row[col]) for col in df.columns]
        col2_width = max(len("First row value"), *(len(v) for v in values))
        dtypes = [str(df[col].dtype) for col in df.columns]
        col3_width = max(len("Dtype"), *(len(d) for d in dtypes))

        # Header row (left-aligned is standard)
        header = (
            f"| {'Column Name'.ljust(col1_width)} "
            f"| {'First row value'.ljust(col2_width)} "
            f"| {'Dtype'.ljust(col3_width)} |"
        )

        # Markdown-compatible separator row
        separator = (
            f"| {'-' * col1_width} "
            f"| {'-' * col2_width} "
            f"| {'-' * col3_width} |"
        )

        lines = [header, separator]

        # Data rows
        for col in df.columns:
            value = str(first_row[col])
            dtype = str(df[col].dtype)
            lines.append(
                f"| {col.ljust(col1_width)} "
                f"| {value.ljust(col2_width)} "
                f"| {dtype.ljust(col3_width)} |"
            )

        return "\n".join(lines)
    
    def format_model_output_summary(
        series: pd.Series,
        model,
        x_subset: pd.DataFrame,
        target_name: str = "y"
    ) -> str:
        # Predict values
        preds = model.predict(x_subset)
        probas = model.predict_proba(x_subset)

        dtype = str(series.dtype)

        # Prepare formatted strings
        y_labels = [f"{target_name}{i}" for i in range(min(5, len(series)))]
        pred_strs = [str(preds[i]) for i in range(len(y_labels))]
        proba_strs = [
            np.array2string(probas[i], precision=2, separator=',', floatmode='fixed')
            for i in range(len(y_labels))
        ]

        # Determine column widths
        col1_width = max(len("y_i"), *(len(label) for label in y_labels))
        col2_width = max(len("model.predict()"), *(len(s) for s in pred_strs))
        col3_width = max(len("model.predict_proba()"), *(len(s) for s in proba_strs))
        col4_width = max(len("dtype"), len(dtype))

        # Header
        header = (
            f"| {'y_i'.ljust(col1_width)} "
            f"| {'model.predict()'.ljust(col2_width)} "
            f"| {'model.predict_proba()'.ljust(col3_width)} "
            f"| {'dtype'.ljust(col4_width)} |"
        )

        # Separator
        separator = (
            f"| {'-' * col1_width} "
            f"| {'-' * col2_width} "
            f"| {'-' * col3_width} "
            f"| {'-' * col4_width} |"
        )

        lines = [header, separator]

        # Data rows
        for i in range(len(y_labels)):
            lines.append(
                f"| {y_labels[i].ljust(col1_width)} "
                f"| {pred_strs[i].ljust(col2_width)} "
                f"| {proba_strs[i].ljust(col3_width)} "
                f"| {dtype.ljust(col4_width)} |"
            )

        return "\n".join(lines)
    
    # Format tabular output for markdown and txt
    x_head_text = format_model_input_summary(x)
    y_head_text = format_model_output_summary(y, model=model, x_subset=x)

    # For HTML version only
    x_head_html = x.head().to_html()
    y_head_html = y.head().to_frame(name="target").to_html()

    specs = model_metadata
    model_type = specs['model']
    parameters = specs['specifications']

    # Garante que o diretório ./models/ exista
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    os.makedirs(models_dir, exist_ok=True)

    # Output filename
    filename = f'model_documentation_{model_name}{output_format}'

    # Se timestamp=True, adiciona YYYYMMDD_HHMMSS ao nome do arquivo
    filename_raw = filename
    if timestamp:
        base, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{ts}{ext}"
        filename_raw = f"{base}_{ts}"

    # Caminho completo para salvar o arquivo
    filepath = os.path.join(models_dir, filename)

    # Write content based on format
    if output_format == '.md':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Model Documentation: {model_type}\n\n")
            f.write("## Specifications\n")
            for k, v in parameters.items():
                f.write(f"- **{k}**: `{v}`\n")
            f.write("\n## Expected Features\n")
            for feature in model_features:
                f.write(f"- {feature}\n")
            f.write("\n## Sample Input - X.head(1)\n")
            f.write("\n" + x_head_text + "\n\n")
            f.write("\n## Sample Output - y.head()\n")
            f.write("\n" + y_head_text + "\n\n")

    elif output_format == '.txt':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Model Documentation: {model_type}\n\n")
            f.write("Specifications:\n")
            for k, v in parameters.items():
                f.write(f"- {k}: {v}\n")
            f.write("\nExpected Features:\n")
            for feature in model_features:
                f.write(f"- {feature}\n")
            f.write("\nSample Input - X.head(1):\n")
            f.write(x_head_text + "\n")
            f.write("Sample Output - y.head():\n")
            f.write(y_head_text + "\n")

    elif output_format == '.html':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"<h1>Model Documentation: {model_type}</h1>\n")
            f.write("<h2>Specifications</h2>\n<ul>\n")
            for k, v in parameters.items():
                f.write(f"<li><b>{k}</b>: {v}</li>\n")
            f.write("</ul>\n<h2>Expected Features</h2>\n<ul>\n")
            for feature in model_features:
                f.write(f"<li>{feature}</li>\n")
            f.write("</ul>\n<h2>Sample Input - X.head(1)</h2>\n")
            f.write(x_head_html)
            f.write("\n<h2>Sample Output - y.head()</h2>\n")
            f.write(y_head_html)

    else:
        raise ValueError("Invalid output_format. Choose from '.md', '.txt', or '.html'.")

    print(f"📁 Arquivo salvo com sucesso:")
    print(f"   → ./models/{filename_raw}{output_format}")