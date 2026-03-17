"""Info and utility commands."""

import click

from sora_cli.core.config import settings
from sora_cli.core.output import console, print_models


@click.command()
def models() -> None:
    """List available Sora models."""
    print_models()


@click.command()
def orientations() -> None:
    """List available video orientations."""
    from rich.table import Table

    table = Table(title="Available Orientations")
    table.add_column("Orientation", style="bold cyan")
    table.add_column("Description")

    table.add_row("landscape", "Horizontal video (wider)")
    table.add_row("portrait", "Vertical video (taller)")

    console.print(table)


@click.command()
def sizes() -> None:
    """List available video sizes."""
    from rich.table import Table

    table = Table(title="Available Video Sizes")
    table.add_column("Size", style="bold cyan")
    table.add_column("Description")

    table.add_row("480p", "Standard definition")
    table.add_row("720p", "HD")
    table.add_row("1080p", "Full HD")

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Sora CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)
