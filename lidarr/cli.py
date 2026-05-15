import json
import click
from rich.console import Console
from rich.table import Table
from .api import LidarrAPI

console = Console()
api = LidarrAPI()

@click.group()
@click.option("--json", "output_json", is_flag=True, help="Output in JSON format")
@click.pass_context
def cli(ctx, output_json):
    """Lidarr CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["json"] = output_json

def print_result(data, table_func, ctx):
    if ctx.obj.get("json"):
        import sys
        if isinstance(data, list):
            output = json.dumps([item.model_dump() if hasattr(item, "model_dump") else item for item in data], indent=2)
        elif hasattr(data, "model_dump"):
            output = json.dumps(data.model_dump(), indent=2)
        else:
            output = json.dumps(data, indent=2)
        print(output)
    else:
        table_func()

@cli.command()
@click.pass_context
def status(ctx):
    """Show Lidarr system status."""
    try:
        status_data = api.get_system_status()
        def show_table():
            console.print(f"[bold green]Lidarr Version:[/bold green] {status_data.version}")
            console.print(f"[bold blue]OS:[/bold blue] {status_data.osName}")
        print_result(status_data, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.option("--search", help="Search for an artist")
@click.option("--page", default=1, help="Page number to show")
@click.option("--limit", default=20, help="Number of items per page")
@click.pass_context
def artists(ctx, search, page, limit):
    """List or search artists with pagination."""
    try:
        if search:
            artists_data = api.search_artists(search)
            title_base = f"Search Results for '{search}'"
        else:
            artists_data = api.get_artists()
            title_base = "Artists in Library"

        # Client-side pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_data = artists_data[start:end]

        def show_table():
            title = f"{title_base} (Page {page}, Limit {limit}, Total {len(artists_data)})"
            table = Table(title=title)
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Monitored", style="yellow")

            for artist in paginated_data:
                table.add_row(
                    str(artist.id),
                    artist.artistName or "N/A",
                    artist.status or "N/A",
                    "Yes" if artist.monitored else "No"
                )
            console.print(table)

        print_result(paginated_data, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.option("--artist-id", type=int, help="Filter by artist ID")
@click.option("--page", default=1, help="Page number to show")
@click.option("--limit", default=20, help="Number of items per page")
@click.pass_context
def albums(ctx, artist_id, page, limit):
    """List albums with pagination."""
    try:
        albums_data = api.get_albums(artist_id)
        
        # Client-side pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_data = albums_data[start:end]

        def show_table():
            table = Table(title=f"Albums (Page {page}, Limit {limit}, Total {len(albums_data)})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Monitored", style="yellow")

            for album in paginated_data:
                table.add_row(
                    str(album.id),
                    album.title or "N/A",
                    album.status or "N/A",
                    "Yes" if album.monitored else "No"
                )
            console.print(table)
        print_result(paginated_data, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.argument("name")
@click.pass_context
def command(ctx, name):
    """Execute a Lidarr command."""
    try:
        res = api.post_command(name)
        def show_table():
            console.print(f"Command '{name}' triggered. Status: {res.get('status')}")
        print_result(res, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.option("--page", default=1, help="Page number to show")
@click.option("--limit", default=20, help="Number of items per page")
@click.pass_context
def queue(ctx, page, limit):
    """Show the download queue with pagination."""
    try:
        items = api.get_queue(page=page, page_size=limit)
        def show_table():
            table = Table(title=f"Download Queue (Page {page}, Limit {limit})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Progress", style="yellow")

            for item in items:
                progress = f"{((item.size - item.sizeleft) / item.size * 100):.1f}%" if item.size > 0 else "0%"
                status_str = item.status or "N/A"
                if item.trackedDownloadStatus == "warning":
                    status_str = f"[bold yellow]⚠ {status_str}[/bold yellow]"
                
                table.add_row(
                    str(item.id),
                    item.title or "N/A",
                    status_str,
                    progress
                )
                
                # Add messages as sub-rows if they exist
                for msg in item.statusMessages:
                    table.add_row(
                        "",
                        f"  [dim]└─ {msg.title}[/dim]",
                        "",
                        ""
                    )
            console.print(table)
        print_result(items, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.option("--limit", default=10, help="Number of items to show")
@click.pass_context
def history(ctx, limit):
    """Show activity history."""
    try:
        items = api.get_history(page_size=limit)
        def show_table():
            table = Table(title="History")
            table.add_column("Date", style="cyan")
            table.add_column("Event", style="magenta")
            table.add_column("Title", style="green")

            for item in items:
                table.add_row(
                    item.date or "N/A",
                    item.eventType or "N/A",
                    item.sourceTitle or "N/A"
                )
            console.print(table)
        print_result(items, show_table, ctx)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
