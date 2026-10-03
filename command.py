
"""
Jarvis AI Assistant - Command Handler
Processes voice commands and performs the requested actions.
"""

from ai import ask_ai
from system_control import (
    open_youtube,
    open_google,
    google_search,
    get_time,
    open_calculator
)


def process_command(command):
    """Process a command and return Jarvis's response."""

    command = command.lower().strip()

    if not command:
        return "I didn't hear a command. Please try again."

    # Website commands
    if "open youtube" in command:
        open_youtube()
        return "Opening YouTube."

    elif "open google" in command:
        open_google()
        return "Opening Google."

    # Calculator
    elif "open calculator" in command:
        open_calculator()
        return "Opening calculator."

    # Time
    elif "what time is it" in command or "tell me the time" in command:
        current_time = get_time()
        return "The current time is " + str(current_time)

    # Google search
    elif command.startswith("search "):
        search_query = command[len("search "):].strip()

        if search_query:
            google_search(search_query)
            return "Searching Google for " + search_query

        return "What would you like me to search for?"

    # Greetings
    elif command in ("hello", "hi", "hey"):
        return "Hello! How can I help you?"

    # Assistant identity
    elif (
        "your name" in command
        or "what is your name" in command
        or "who are you" in command
    ):
        return "My name is Jarvis. I am your personal AI assistant."

    # General conversation
    elif "how are you" in command:
        return "I am doing great. Thank you for asking."

    # Sleep command
    elif "go to sleep" in command or "deactivate" in command:
        return "Going to sleep. Say Hey Jarvis when you need me."

    # Exit command
    elif command in ("stop", "exit", "bye", "quit"):
        return "Goodbye. It was nice talking to you."

    # Ask local AI for other questions
    else:
        return ask_ai(command)


if __name__ == "__main__":
    print("Testing Jarvis Command Handler")
    print("--------------------------------")

    test_commands = [
        "hello",
        "what is your name",
        "how are you",
        "what time is it"
    ]

    for test in test_commands:
        print(f"\nYou: {test}")
        print("Jarvis:", process_command(test))

    print("\nCommand handler test completed.")
