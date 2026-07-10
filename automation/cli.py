import typer
from pathlib import Path
from automation.folder_setup import create_project_structure
from automation.audio import clean_audio
from automation.captions import generate_captions

app = typer.Typer(help="Game Review Pipeline - Pre-editing automation")

@app.command()
def run(
    voice: str = typer.Option(..., help="Path to raw voiceover audio file"),
    output_dir: str = typer.Option("./output", help="Base output directory for the project"),
    config_path: str = typer.Option(None, help="Path to config YAML"),
):
    """
    Full pre‑edit pipeline: folder structure, audio cleaning, captions.
    """
    typer.echo("Running full pipeline...")
    create_project_structure(output_dir)
    typer.echo("✓ Project structure created.")
    
    voice_clean = str(Path(output_dir) / "Voice" / "voice_clean.wav")
    success = clean_audio(voice, voice_clean, config_path)
    if not success:
        typer.echo("Audio cleaning failed. Aborting.")
        raise typer.Exit(code=1)
    typer.echo("✓ Audio cleaned.")
    
    captions_dir = str(Path(output_dir) / "Voice")
    generate_captions(voice_clean, captions_dir, config_path)
    typer.echo("✓ Captions generated.")
    
    typer.echo(f"\nAll done! Check {output_dir} for results.")

@app.command()
def audio(
    voice: str = typer.Option(..., help="Path to raw voiceover audio file"),
    output: str = typer.Option("./voice_clean.wav", help="Output path for cleaned audio"),
    config_path: str = typer.Option(None, help="Path to config YAML"),
):
    """Clean a voiceover audio file."""
    success = clean_audio(voice, output, config_path)
    if not success:
        typer.echo("Audio cleaning failed.")

@app.command()
def captions(
    audio: str = typer.Option(..., help="Path to cleaned audio file (WAV recommended)"),
    output_dir: str = typer.Option("./captions", help="Directory to save captions.srt"),
    config_path: str = typer.Option(None, help="Path to config YAML"),
):
    """Generate word-level captions (SRT) from an audio file."""
    generate_captions(audio, output_dir, config_path)

@app.command()
def folder(
    output_dir: str = typer.Option("./my_project", help="Base directory to create the folder structure"),
    config_path: str = typer.Option(None, help="Path to config YAML"),
):
    """Create the standard project folder structure."""
    create_project_structure(output_dir, config_path)
    typer.echo(f"✓ Folder structure created in {output_dir}")

@app.command()
def metadata(
    script_file: str = typer.Option(..., help="Path to a text file containing review notes"),
    provider: str = typer.Option("ollama", help="LLM provider: openai, gemini, claude, ollama"),
    model: str = typer.Option(None, help="Model name (provider-specific)"),
    api_key: str = typer.Option(None, help="API key (if not using environment variable)"),
    output: str = typer.Option("./metadata.json", help="Output JSON file for generated metadata"),
):
    """
    Generate YouTube title, description, and hashtags from a review script.
    """
    import json
    from automation.metadata import generate_metadata

    with open(script_file, "r") as f:
        script = f.read()

    typer.echo(f"Generating metadata using {provider}...")
    try:
        result = generate_metadata(
            script,
            provider=provider,
            model=model if model else None,
            api_key=api_key,
        )
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    with open(output, "w") as f:
        json.dump(result, f, indent=2)

    typer.echo(f"✓ Metadata saved to {output}")
    typer.echo(f"  Title: {result['title']}")
    typer.echo(f"  Description: {result['description']}")
    typer.echo(f"  Hashtags: {result['hashtags']}")

if __name__ == "__main__":
    app()
