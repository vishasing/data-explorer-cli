import click
import pandas as pd
import os

DATA_PATH = "../data/dataset.csv"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--file', default=DATA_PATH, help='Path to your dataset CSV file.')
def load(file):
    """Load dataset and show shape and columns."""
    if not os.path.exists(file):
        click.echo(f"File not found: {file}")
        return

    df = pd.read_csv(file)
    click.echo(f"Shape: {df.shape}")
    click.echo(f"Columns: {list(df.columns)}")

@cli.command()
@click.option('--file', default=DATA_PATH, help='Path to your dataset CSV file.')
def summary(file):
    """Compute and display summary statistics for numeric columns."""
    if not os.path.exists(file):
        click.echo(f"File not found: {file}")
        return

    df = pd.read_csv(file)
    num_cols = df.select_dtypes(include='number')
    if num_cols.empty:
        click.echo("No numeric columns found in dataset.")
        return

    summary_df = pd.DataFrame({
        'mean': num_cols.mean(),
        'median': num_cols.median(),
        'std': num_cols.std()
    })
    summary_df = summary_df.reset_index().rename(columns={'index': 'column'})

    click.echo(summary_df.to_string(index=False))

if __name__ == "__main__":
    cli()
