
from voice import speak, listen
from command import process_command
from config import ASSISTANT_NAME

def show_event(event_type, message):
    """Send assistant events to the dashboard."""
    print(f"JARVIS_EVENT|{event_type}|{message}", flush=True)

def respond(message):
    """Display and speak the assistant's response."""
    show_event("assistant", message)
    speak(message)

def is_wake_command(command):
    return "hey jarvis" in command or "hey jar" in command

def is_exit_command(command):
    return command.strip() in ("stop", "exit", "bye", "quit")

def is_sleep_command(command):
    return (
        "go to sleep" in command
        or "deactivate" in command
        or command.strip() == "sleep"
    )

def main():
    show_event("status", "ONLINE")
    respond(f"{ASSISTANT_NAME} is online. Say Hey Jarvis to activate me.")

    while True:
        command = listen()

        if not command:
            continue

        command = command.lower().strip()
        show_event("user", command)

        # Wake Jarvis from standby
        if is_wake_command(command):
            show_event("status", "LISTENING")
            respond(f"Yes, I am listening. How can I help you?")

            while True:
                command = listen()

                if not command:
                    continue

                command = command.lower().strip()
                show_event("user", command)

                # Put Jarvis to sleep
                if is_sleep_command(command):
                    respond("Going to sleep. Say Hey Jarvis when you need me.")
                    show_event("status", "STANDBY")
                    break

                # Exit Jarvis
                if is_exit_command(command):
                    respond("Goodbye. It was nice talking to you.")
                    show_event("status", "OFFLINE")
                    return

                # Process commands through command.py
                show_event("status", "THINKING")
                answer = process_command(command)
                respond(answer)
                show_event("status", "LISTENING")

        # Allow exit while in standby
        elif is_exit_command(command):
            respond("Goodbye. See you again.")
            show_event("status", "OFFLINE")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        show_event("status", "OFFLINE")
        print("\nJarvis stopped.")
