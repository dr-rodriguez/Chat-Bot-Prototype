"""CLI entry point for Chat-Bot-Prototype."""

import click
import sys
from typing import Optional

from chat_bot.agent.agent import ChatAgent
from chat_bot.config.settings import Settings


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Chat-Bot-Prototype - A simple AI chat bot using Langchain."""
    pass


@cli.command()
@click.option(
    "-p", "--provider",
    type=click.Choice(["ollama", "gemini"], case_sensitive=False),
    default="ollama",
    help="LLM provider to use (ollama or gemini)",
)
@click.option(
    "-m", "--model",
    type=str,
    help="Model name to use (provider-specific)",
)
def chat(provider: str, model: Optional[str]):
    """Start an interactive chat session."""
    settings = Settings()
    
    # Initialize agent with selected provider
    agent = ChatAgent(provider=provider, model=model, settings=settings)
    
    click.echo("Chat-Bot - Interactive Mode")
    click.echo("Type 'exit' or 'quit' to end the session\n")
    
    while True:
        try:
            user_input = click.prompt("You", type=str, default="")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            response = agent.invoke(user_input)
            click.echo(f"Bot: {response}")
        except KeyboardInterrupt:
            click.echo("\nExiting...")
            break
        except Exception as e:
            click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("message", required=True)
@click.option(
    "-p", "--provider",
    type=click.Choice(["ollama", "gemini"], case_sensitive=False),
    default="ollama",
    help="LLM provider to use (ollama or gemini)",
)
@click.option(
    "-m", "--model",
    type=str,
    help="Model name to use (provider-specific)",
)
def run(message: str, provider: str, model: Optional[str]):
    """Run a single message through the chat bot (non-interactive)."""
    settings = Settings()
    
    agent = ChatAgent(provider=provider, model=model, settings=settings)
    
    try:
        response = agent.invoke(message)
        click.echo(response)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()

