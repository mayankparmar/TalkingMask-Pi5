"""LLM-based conversational assistant supporting multiple providers."""

from openai import OpenAI
import os
import subprocess
import json

# Global OpenAI client initialised with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class GPTAssistant:
    """Manages conversation with various LLM providers, maintaining context history."""

    def __init__(self, config):
        """
        Initialise LLM assistant with configuration.

        Args:
            config: Configuration dictionary containing LLM settings
        """
        self.engine = config["llm"]["engine"]
        self.model_path = config["llm"].get("model_path", "")
        self.prompt_file = config["llm"]["prompt_file"]

        # OpenAI-specific configuration
        if self.engine == "openai":
            self.model = config["llm"]["model"]
            self.openai_model = "gpt-" + str(self.model)

        self.conversation = []
        self.pre_prompt = self._load_prompt()

    def _load_prompt(self):
        """Load system prompt from file."""
        try:
            with open(self.prompt_file, "r") as f:
                return f.read().strip()
        except Exception as e:
            print("Error loading prompt:", e)
            return ""

    def ask(self, user_input):
        """
        Send user input to the LLM and return response.

        Args:
            user_input: User's spoken text

        Returns:
            LLM's text response
        """
        if self.engine == "openai":
            return self._ask_openai(user_input)
        elif self.engine == "claude":
            return self._ask_claude(user_input)
        elif self.engine == "gemini":
            return self._ask_gemini(user_input)
        elif self.engine == "codex":
            return self._ask_codex(user_input)
        elif self.engine == "local":
            return self._ask_local(user_input)
        else:
            return "LLM engine not recognised."

    def _ask_openai(self, user_input):
        """Query OpenAI GPT model with conversation history."""
        self.conversation.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "system", "content": self.pre_prompt}] + self.conversation,
                temperature=0.7,
                max_tokens=300
            )
            reply = response.choices[0].message.content
            self.conversation.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print("OpenAI error:", e)
            return "Sorry, I encountered a problem."

    def _ask_claude(self, user_input):
        """
        Query Claude via CLI.

        Requires: Anthropic CLI installed and configured
        Install: pip install anthropic-cli or use official Claude CLI
        """
        self.conversation.append({"role": "user", "content": user_input})

        try:
            # Build conversation context for Claude
            conversation_text = f"{self.pre_prompt}\n\n"
            for msg in self.conversation:
                role = msg["role"].capitalize()
                conversation_text += f"{role}: {msg['content']}\n"
            conversation_text += "Assistant:"

            # Call Claude CLI (adjust command based on your CLI installation)
            result = subprocess.run(
                ["claude", "--no-stream"],
                input=conversation_text,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                reply = result.stdout.strip()
                self.conversation.append({"role": "assistant", "content": reply})
                return reply
            else:
                print("Claude CLI error:", result.stderr)
                return "Sorry, I encountered a problem with Claude."

        except FileNotFoundError:
            print("Claude CLI not found. Please install it first.")
            return "Claude CLI is not installed."
        except Exception as e:
            print("Claude error:", e)
            return "Sorry, I encountered a problem."

    def _ask_gemini(self, user_input):
        """
        Query Google Gemini via CLI.

        Requires: Google AI CLI or gemini-cli installed and configured
        Install: pip install google-generativeai
        """
        self.conversation.append({"role": "user", "content": user_input})

        try:
            # Build conversation context
            conversation_text = f"{self.pre_prompt}\n\n"
            for msg in self.conversation:
                role = "User" if msg["role"] == "user" else "Model"
                conversation_text += f"{role}: {msg['content']}\n"

            # Call Gemini CLI (adjust based on your installation)
            # Alternative: Use Python API directly if CLI is not preferred
            result = subprocess.run(
                ["gemini", "chat", "--message", user_input],
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, "GEMINI_SYSTEM_PROMPT": self.pre_prompt}
            )

            if result.returncode == 0:
                reply = result.stdout.strip()
                self.conversation.append({"role": "assistant", "content": reply})
                return reply
            else:
                print("Gemini CLI error:", result.stderr)
                return "Sorry, I encountered a problem with Gemini."

        except FileNotFoundError:
            print("Gemini CLI not found. Please install it first.")
            return "Gemini CLI is not installed."
        except Exception as e:
            print("Gemini error:", e)
            return "Sorry, I encountered a problem."

    def _ask_codex(self, user_input):
        """
        Query OpenAI Codex/GPT via OpenAI CLI.

        Requires: OpenAI CLI installed and configured
        Install: pip install openai-cli
        Note: Codex is deprecated; this uses standard OpenAI models
        """
        self.conversation.append({"role": "user", "content": user_input})

        try:
            # Build messages for OpenAI format
            messages = [{"role": "system", "content": self.pre_prompt}] + self.conversation
            messages_json = json.dumps(messages)

            # Call OpenAI CLI
            result = subprocess.run(
                ["openai", "api", "chat.completions.create",
                 "-m", "gpt-3.5-turbo",
                 "-g", "user", user_input],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Parse JSON response
                response_data = json.loads(result.stdout)
                reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if reply:
                    self.conversation.append({"role": "assistant", "content": reply})
                    return reply
                else:
                    return "Sorry, received empty response."
            else:
                print("Codex CLI error:", result.stderr)
                return "Sorry, I encountered a problem with Codex."

        except FileNotFoundError:
            print("OpenAI CLI not found. Please install it first.")
            return "OpenAI CLI is not installed."
        except json.JSONDecodeError as e:
            print("Failed to parse Codex response:", e)
            return "Sorry, I encountered a problem."
        except Exception as e:
            print("Codex error:", e)
            return "Sorry, I encountered a problem."

    def _ask_local(self, user_input):
        """Placeholder for local LLM implementation."""
        return "Local LLM not implemented yet."
