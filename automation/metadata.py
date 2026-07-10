import os
import json
from automation.utils import load_config

# Optional imports – only needed when using the corresponding provider
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import requests
except ImportError:
    requests = None


def generate_metadata(review_script: str, provider="ollama", config_path=None, **kwargs):
    """
    Generate YouTube title, description, and hashtags from a review script.
    
    Args:
        review_script (str): Bullet-point notes or full text of the review.
        provider (str): "openai", "gemini", "claude", or "ollama".
        config_path (str, optional): Path to config YAML (not used yet).
        **kwargs: Additional provider-specific args (e.g., api_key, model).
    
    Returns:
        dict with keys: "title", "description", "hashtags"
    """
    if provider == "openai":
        return _generate_openai(review_script, **kwargs)
    elif provider == "gemini":
        return _generate_gemini(review_script, **kwargs)
    elif provider == "claude":
        return _generate_claude(review_script, **kwargs)
    elif provider == "ollama":
        return _generate_ollama(review_script, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _prompt_from_script(script):
    """Build the prompt used for all providers."""
    return f"""
You are a YouTube SEO expert. Given the following game review notes, generate:
1. A catchy, click‑optimized YouTube Shorts title (max 60 characters).
2. A short description (max 200 characters) that includes the rating and a call‑to‑action to watch the full review.
3. 10 relevant hashtags (without the # symbol) separated by spaces.

Review notes:
{script}

Return the result as a JSON object with keys: "title", "description", "hashtags".
Only output the JSON, nothing else.
"""


def _generate_openai(script, model="gpt-4o-mini", api_key=None):
    if openai is None:
        raise ImportError("openai package not installed. Run: pip install openai")
    if api_key:
        openai.api_key = api_key
    elif "OPENAI_API_KEY" in os.environ:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    else:
        raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY env variable or pass api_key.")

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You output only valid JSON."},
            {"role": "user", "content": _prompt_from_script(script)}
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return json.loads(response.choices[0].message.content)


def _generate_gemini(script, model="gemini-1.5-flash", api_key=None):
    if genai is None:
        raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    if api_key:
        genai.configure(api_key=api_key)
    elif "GEMINI_API_KEY" in os.environ:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    else:
        raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY or pass api_key.")

    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(
        _prompt_from_script(script),
        generation_config={"temperature": 0.7, "max_output_tokens": 200}
    )
    # Gemini sometimes wraps JSON in ```json ... ```
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _generate_claude(script, model="claude-3-haiku-20240307", api_key=None):
    if anthropic is None:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
    elif "ANTHROPIC_API_KEY" in os.environ:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    else:
        raise ValueError("Anthropic API key not provided. Set ANTHROPIC_API_KEY or pass api_key.")

    message = client.messages.create(
        model=model,
        max_tokens=200,
        temperature=0.7,
        system="You output only valid JSON.",
        messages=[{"role": "user", "content": _prompt_from_script(script)}]
    )
    return json.loads(message.content[0].text)


def _generate_ollama(script, model="llama3", base_url="http://localhost:11434"):
    if requests is None:
        raise ImportError("requests package not installed. Run: pip install requests")
    response = requests.post(
        f"{base_url}/api/generate",
        json={
            "model": model,
            "prompt": _prompt_from_script(script),
            "stream": False,
            "options": {"temperature": 0.7}
        }
    )
    response.raise_for_status()
    text = response.json()["response"].strip()
    # Ollama may also wrap in ```json
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)
