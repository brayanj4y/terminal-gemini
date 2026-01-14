
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich import print as rprint

# Rich Console
console = Console()

def configure_api_key():
    """
    Configures API key.
    """
    load_dotenv() 
    
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        console.print("[bold red]GEMINI_API_KEY not found in environment variables.[/bold red]")
        console.print("Please enter your Gemini API key below.")
        console.print("You can get one from: [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link]")
        try:
            api_key = Prompt.ask("[bold yellow]API Key[/bold yellow]")
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            sys.exit(0)

    if not api_key:
        console.print("[bold red]Error: API Key is required to proceed.[/bold red]")
        sys.exit(1)
        
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        console.print(f"[bold red]Error configuring API key: {e}[/bold red]")
        sys.exit(1)
    
    return api_key

def main():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]Gemini Terminal Assistant[/bold cyan]\n[dim]Powered by Google Gemini 2.5 Flash[/dim]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    configure_api_key()

    # Init model
    try:
        # User preferred model
        model_name = 'gemini-2.5-flash'
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        console.print(f"[green]Successfully connected to {model_name}![/green]\n")
    except Exception as e:
        console.print(f"[bold red]Error initializing model: {e}[/bold red]")
        sys.exit(1)

    console.print("[bold yellow]Type 'exit', 'quit' to stop.[/bold yellow]")
    console.print("--------------------------------------------------")

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold blue]Goodbye![/bold blue]")
                break
            
            if not user_input.strip():
                continue

            # Spinner
            console.print("[bold cyan]Gemini:[/bold cyan]")
            
            # Stream response
            with Live(Spinner("dots", text="Thinking...", style="cyan"), refresh_per_second=10, transient=True) as live:
                response = chat.send_message(user_input, stream=True)
                full_text = ""
                for chunk in response:
                    text_chunk = chunk.text
                    full_text += text_chunk
                    # Update live display with markdown
                    live.update(Markdown(full_text))
            
            # Final output
            console.print(Markdown(full_text))
            console.print() # Newline

        except KeyboardInterrupt:
            console.print("\n\n[bold blue]Goodbye![/bold blue]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
