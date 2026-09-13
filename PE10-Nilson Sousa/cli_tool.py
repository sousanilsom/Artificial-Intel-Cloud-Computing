import click
import joblib
import logging
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Record lifecycle events and accuracy results in mlops.log
logging.basicConfig(
    filename="mlops.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@click.group()
def cli():
    """MLOps CLI tool to manage ML model lifecycle."""
    pass

@cli.command()
def train():
    """Train and save a simple Iris model."""
    logging.info("Training started.")
    click.echo("Training model...")
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/trained_model.pkl")

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    click.echo(f" Model trained with accuracy: {acc:.2f}")
    logging.info(f"Training completed with accuracy: {acc:.2f}")

@cli.command()
def evaluate():
    """Evaluate the trained model."""
    if not os.path.exists("model/trained_model.pkl"):
        click.echo(" No model found! Run 'python cli_tool.py train' first.")
        logging.warning("Evaluation skipped: no trained model found.")
        return

    logging.info("Model evaluation started.")
    click.echo("🔍 Evaluating model...")
    X, y = load_iris(return_X_y=True)
    model = joblib.load("model/trained_model.pkl")
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    click.echo(f" Overall dataset accuracy: {acc:.2f}")
    logging.info(f"Evaluation completed with accuracy: {acc:.2f}")

if __name__ == "__main__":
    cli()
