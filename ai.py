import json
import urllib.request
import urllib.error


def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    try:
        request = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "Sorry, no response received.")

    except urllib.error.URLError:
        return "Ollama is not running. Please start Ollama."

    except Exception as e:
        return f"AI Error: {e}"