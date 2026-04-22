import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from brain.db import init_db, get_connection
from brain.search import search_entries

app = typer.Typer()
console = Console()

def format_row(row):
    id_, content, type_, language, tags, created_at, pinned = row
    pin_marker = "📌" if pinned else ""
    return id_, content, type_ or "-", language or "-", tags or "-", created_at, pin_marker

@app.command()
def add(
    content: str = typer.Argument(..., help="Note, link or snippet to save"),
    tag: str = typer.Option(None, "--tag", "-t", help="Comma separated tags"),
    type_: str = typer.Option("note", "--type", help="note | link | snippet"),
    language: str = typer.Option(None, "--lang", help="Language for snippets")
):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (content, type, language, tags, created_at) VALUES (?, ?, ?, ?, ?)",
        (content, type_, language, tag, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    console.print(f"[green]✓ Saved![/green]")

@app.command()
def list_all():
    init_db()
    rows = search_entries()
    if not rows:
        console.print("[yellow]No entries found.[/yellow]")
        return
    _print_table(rows)

@app.command()
def search(
    keyword: str = typer.Argument(None, help="Keyword to search"),
    tag: str = typer.Option(None, "--tag", "-t"),
    type_: str = typer.Option(None, "--type"),
    today: bool = typer.Option(False, "--today")
):
    init_db()
    rows = search_entries(keyword=keyword, tag=tag, entry_type=type_, today=today)
    if not rows:
        console.print("[yellow]No results found.[/yellow]")
        return
    _print_table(rows)

@app.command()
def delete(id: int = typer.Argument(..., help="ID of entry to delete")):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    console.print(f"[red]Deleted entry {id}[/red]")

@app.command()
def edit(id: int = typer.Argument(..., help="ID of entry to edit")):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries WHERE id = ?", (id,))
    row = cursor.fetchone()
    if not row:
        console.print(f"[red]No entry found with ID {id}[/red]")
        conn.close()
        return

    import tempfile, subprocess, os
    id_, content, type_, language, tags, created_at = row

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        tmp_path = f.name

    editor = os.environ.get("EDITOR", "notepad")
    subprocess.call([editor, tmp_path])

    with open(tmp_path, 'r') as f:
        new_content = f.read().strip()

    os.unlink(tmp_path)

    cursor.execute("UPDATE entries SET content = ? WHERE id = ?", (new_content, id))
    conn.commit()
    conn.close()
    console.print(f"[green]✓ Entry {id} updated![/green]")

@app.command()
def export(
    format: str = typer.Option("markdown", "--format", "-f", help="markdown | json")
):
    init_db()
    rows = search_entries()
    if not rows:
        console.print("[yellow]No entries to export.[/yellow]")
        return

    import json, os
    output_dir = os.path.expanduser("~/.second-brain")

    if format == "json":
        data = []
        for row in rows:
            id_, content, type_, language, tags, created_at = row
            data.append({
                "id": id_,
                "content": content,
                "type": type_,
                "language": language,
                "tags": tags,
                "created_at": created_at
            })
        out_path = os.path.join(output_dir, "export.json")
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2)
        console.print(f"[green]✓ Exported to {out_path}[/green]")

    else:
        lines = ["# Second Brain Export\n"]
        for row in rows:
            id_, content, type_, language, tags, created_at = row
            lines.append(f"## [{id_}] {type_.upper()}")
            lines.append(f"**Tags:** {tags or '-'}")
            lines.append(f"**Created:** {created_at}")
            lines.append(f"\n{content}\n")
            lines.append("---\n")
        out_path = os.path.join(output_dir, "export.md")
        with open(out_path, "w") as f:
            f.write("\n".join(lines))
        console.print(f"[green]✓ Exported to {out_path}[/green]")

@app.command()
def today():
    init_db()
    rows = search_entries(today=True)
    if not rows:
        console.print("[yellow]No entries today.[/yellow]")
        return
    console.print(f"[cyan]Today's entries:[/cyan]")
    _print_table(rows)

@app.command()
def pin(id: int = typer.Argument(..., help="ID of entry to pin/unpin")):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pinned FROM entries WHERE id = ?", (id,))
    row = cursor.fetchone()
    if not row:
        console.print(f"[red]No entry found with ID {id}[/red]")
        conn.close()
        return
    new_pinned = 0 if row[0] == 1 else 1
    cursor.execute("UPDATE entries SET pinned = ? WHERE id = ?", (new_pinned, id))
    conn.commit()
    conn.close()
    if new_pinned:
        console.print(f"[cyan]📌 Entry {id} pinned![/cyan]")
    else:
        console.print(f"[yellow]📌 Entry {id} unpinned.[/yellow]")

@app.command()
def copy(id: int = typer.Argument(..., help="ID of entry to copy to clipboard")):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM entries WHERE id = ?", (id,))
    row = cursor.fetchone()
    if not row:
        console.print(f"[red]No entry found with ID {id}[/red]")
        conn.close()
        return
    import pyperclip
    pyperclip.copy(row[0])
    conn.close()
    console.print(f"[green]✓ Copied to clipboard![/green]")

def _print_table(rows):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Pin", width=4)
    table.add_column("ID", width=4)
    table.add_column("Content", width=50)
    table.add_column("Type", width=8)
    table.add_column("Lang", width=8)
    table.add_column("Tags", width=15)
    table.add_column("Created", width=20)

    for item in rows:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], tuple):
            score, row = item
            id_, content, type_, language, tags, created_at, pinned = row
            pin_marker = "📌" if pinned else ""
            table.add_row(pin_marker, str(id_), content, type_ or "-", language or "-", tags or "-", created_at)
        else:
            id_, content, type_, language, tags, created_at, pinned = item
            pin_marker = "📌" if pinned else ""
            table.add_row(pin_marker, str(id_), content, type_ or "-", language or "-", tags or "-", created_at)

    console.print(table)

if __name__ == "__main__":
    app()