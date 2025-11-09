"""Unit tests for CLI commands."""

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from chat_bot.cli.main import cli


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.prompt")
@patch("chat_bot.cli.main.click.echo")
def test_cli_chat_command(mock_echo, mock_prompt, mock_settings, mock_chat_agent):
    """Test that chat command initializes agent and starts interactive loop (mocked).
    
    Verifies that the chat command correctly initializes a ChatAgent
    and handles user input in an interactive loop, displaying responses.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.get_model_name.return_value = "llama3.2:3b"
    mock_agent_instance.invoke.return_value = "Test response"
    mock_chat_agent.return_value = mock_agent_instance
    
    # Simulate user input: first message, then exit
    mock_prompt.side_effect = ["Hello", "exit"]
    
    # Call chat command using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["chat", "--provider", "ollama"])
    
    # Verify agent was created
    mock_chat_agent.assert_called_once_with(
        provider="ollama",
        model=None,
        settings=mock_settings_instance
    )
    
    # Verify echo was called for initial messages
    assert mock_echo.call_count >= 2


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.prompt")
@patch("chat_bot.cli.main.click.echo")
def test_cli_chat_command_exit(mock_echo, mock_prompt, mock_settings, mock_chat_agent):
    """Test that chat command handles exit/quit commands.
    
    Verifies that the chat command correctly exits when the user
    types 'exit' or 'quit'.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.get_model_name.return_value = "llama3.2:3b"
    mock_chat_agent.return_value = mock_agent_instance
    
    # Simulate user typing 'quit' immediately
    mock_prompt.return_value = "quit"
    
    # Call chat command using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["chat", "--provider", "ollama"])
    
    # Verify agent was created but invoke was not called
    mock_chat_agent.assert_called_once()
    mock_agent_instance.invoke.assert_not_called()


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.prompt")
@patch("chat_bot.cli.main.click.echo")
def test_cli_chat_command_error(mock_echo, mock_prompt, mock_settings, mock_chat_agent):
    """Test that chat command handles errors gracefully.
    
    Verifies that the chat command continues running even when
    an error occurs during agent invocation, displaying the error
    message to the user.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.get_model_name.return_value = "llama3.2:3b"
    mock_agent_instance.invoke.side_effect = Exception("Test error")
    mock_chat_agent.return_value = mock_agent_instance
    
    # Simulate user input: message that causes error, then exit
    mock_prompt.side_effect = ["Test message", "exit"]
    
    # Call chat command using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["chat", "--provider", "ollama"])
    
    # Verify error was displayed
    error_calls = [call for call in mock_echo.call_args_list if "Error" in str(call)]
    assert len(error_calls) > 0


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.echo")
def test_cli_run_command(mock_echo, mock_settings, mock_chat_agent):
    """Test that run command processes message and outputs response.
    
    Verifies that the run command correctly processes a single message
    and outputs the agent's response.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.invoke.return_value = "Test response"
    mock_chat_agent.return_value = mock_agent_instance
    
    # Call run command using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["run", "Test message", "--provider", "ollama"])
    
    # Verify agent was created and invoked
    mock_chat_agent.assert_called_once_with(
        provider="ollama",
        model=None,
        settings=mock_settings_instance
    )
    mock_agent_instance.invoke.assert_called_once_with("Test message")
    mock_echo.assert_called_once_with("Test response")


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.echo")
@patch("chat_bot.cli.main.sys.exit")
def test_cli_run_command_error(mock_exit, mock_echo, mock_settings, mock_chat_agent):
    """Test that run command handles errors and exits with code 1.
    
    Verifies that the run command correctly handles errors during
    agent invocation, displays the error message, and exits with
    code 1.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.invoke.side_effect = Exception("Test error")
    mock_chat_agent.return_value = mock_agent_instance
    
    # Call run command using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["run", "Test message", "--provider", "ollama"])
    
    # Verify error was displayed and exit was called with code 1
    error_calls = [call for call in mock_echo.call_args_list if "Error" in str(call)]
    assert len(error_calls) > 0
    # Check that sys.exit(1) was called (may be called multiple times by CliRunner)
    mock_exit.assert_any_call(1)


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.prompt")
@patch("chat_bot.cli.main.click.echo")
def test_cli_provider_option(mock_echo, mock_prompt, mock_settings, mock_chat_agent):
    """Test that provider option is passed to agent.
    
    Verifies that the provider option from the CLI is correctly
    passed to the ChatAgent constructor.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.get_model_name.return_value = "gemini-2.5-flash"
    mock_chat_agent.return_value = mock_agent_instance
    
    # Simulate user typing exit immediately
    mock_prompt.return_value = "exit"
    
    # Call chat command with gemini provider using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["chat", "--provider", "gemini"])
    
    # Verify agent was created with correct provider
    mock_chat_agent.assert_called_once_with(
        provider="gemini",
        model=None,
        settings=mock_settings_instance
    )


@patch("chat_bot.cli.main.ChatAgent")
@patch("chat_bot.cli.main.Settings")
@patch("chat_bot.cli.main.click.prompt")
@patch("chat_bot.cli.main.click.echo")
def test_cli_model_option(mock_echo, mock_prompt, mock_settings, mock_chat_agent):
    """Test that model option is passed to agent.
    
    Verifies that the model option from the CLI is correctly
    passed to the ChatAgent constructor.
    """
    # Setup mocks
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance
    
    mock_agent_instance = MagicMock()
    mock_agent_instance.get_model_name.return_value = "llama3.2:1b"
    mock_chat_agent.return_value = mock_agent_instance
    
    # Simulate user typing exit immediately
    mock_prompt.return_value = "exit"
    
    # Call chat command with model option using CliRunner
    runner = CliRunner()
    _ = runner.invoke(cli, ["chat", "--provider", "ollama", "--model", "llama3.2:1b"])
    
    # Verify agent was created with correct model
    mock_chat_agent.assert_called_once_with(
        provider="ollama",
        model="llama3.2:1b",
        settings=mock_settings_instance
    )

