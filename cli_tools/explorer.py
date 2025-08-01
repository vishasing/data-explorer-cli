import click
import pandas as pd
import os

DATA_PATH = "../data/dataset.csv"
CLEANED_PATH= "../data/cleaned_dataset.csv"

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
@click.option('--file', default=CLEANED_PATH, help='Path to your dataset CSV file.')
def load1(file):
    """Load dataset and show shape and columns."""
    if not os.path.exists(file):
        click.echo(f"File not found: {file}")
        return

    df = pd.read_csv(file)
    click.echo(f"C_Shape: {df.shape}")
    click.echo(f"C_Columns: {list(df.columns)}")



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

@cli.command()
@click.option('--file', default=DATA_PATH, help='Dataset CSV file.')
@click.option('--output', default='../data/cleaned_dataset.csv', help='Output file to save cleaned data.')
@click.option('--dropna', is_flag=True, help='Drop rows with missing values.')
@click.option('--fillna', type=float, help='Fill missing numeric values with this value.')
def clean(file, output, dropna, fillna):
    """Clean dataset by dropping or filling missing values."""
    if not os.path.exists(file):
        click.echo(f"File not found: {file}")
        return
    df = pd.read_csv(file)
    if dropna:
        df = df.dropna()
        click.echo("Dropped rows with missing values.")
    elif fillna is not None:
        df = df.fillna(fillna)
        click.echo(f"Filled missing values with {fillna}.")
    else:
        click.echo("Specify --dropna or --fillna <value>")
        return
    df.to_csv(output, index=False)
    click.echo(f"Cleaned data saved to {output}")

@cli.command()
@click.option('--file', default=DATA_PATH, help='Input dataset CSV file.')
@click.option('--output', default='../data/filtered_dataset.csv', help='Output file for filtered data.')
@click.option('--column', required=True, help='Column name to filter.')
@click.option('--min', type=float, help='Minimum value for filtering.')
@click.option('--max', type=float, help='Maximum value for filtering.')
def filter(file, output, column, min, max):
    """Filter rows by column value range."""
    if not os.path.exists(file):
        click.echo(f"File not found: {file}")
        return
    df = pd.read_csv(file)
    if column not in df.columns:
        click.echo(f"Column {column} not found in dataset.")
        return

    filtered_df = df
    if min is not None:
        filtered_df = filtered_df[filtered_df[column] >= min]
    if max is not None:
        filtered_df = filtered_df[filtered_df[column] <= max]

    filtered_df.to_csv(output, index=False)
    click.echo(f"Filtered data saved to {output} ({filtered_df.shape[0]} rows)")


if __name__ == "__main__":
    cli()
