# mlopscli/cli.py
import typer
from pathlib import Path
from mlopscli.runner import run_pipeline

app = typer.Typer()


@app.command()
def job(
    job_name: str = typer.Option(
        ..., "--job", help="Job name (e.g., prepare_train_pipeline)"
    ),
    job_config: Path = typer.Option(..., "--job_config", help="Path to job_order.yaml"),
    render_dag: bool = typer.Option(
        True, "--render_dag/--no-render_dag", help="Render DAG to image"
    ),
):
    typer.echo(f"Running job: {job_name}")
    run_pipeline(job_name, job_config, render_dag)


if __name__ == "__main__":
    app()
