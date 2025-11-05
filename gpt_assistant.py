"""GPT-based conversational assistant using OpenAI API."""

from openai import OpenAI
import os

# Global OpenAI client initialised with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class GPTAssistant:
    """Manages conversation with GPT models, maintaining context history."""

    def __init__(self, config):
        """
        Initialise GPT assistant with configuration.

        Args:
            config: Configuration dictionary containing LLM settings
        """
        self.engine = config["llm"]["engine"]
        self.model_path = config["llm"]["model_path"]
        self.prompt_file = config["llm"]["prompt_file"]

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

    def _ask_local(self, user_input):
        """Placeholder for local LLM implementation."""
        return "Local LLM not implemented yet."
