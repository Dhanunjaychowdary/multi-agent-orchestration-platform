"""Main entry point for the Multi-Agent Orchestration Platform."""

import os
import logging
from dotenv import load_dotenv
from agents.supervisor import SupervisorAgent

load_dotenv()

logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def main():
      """Run the multi-agent orchestration platform."""
      logger.info("Starting Multi-Agent Orchestration Platform...")

    # Validate required environment variables
      required_env = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]
      missing = [v for v in required_env if not os.getenv(v)]
      if missing:
                raise EnvironmentError(
                              f"Missing required environment variables: {', '.join(missing)}\n"
                              "Please set them in your .env file or environment."
                )

      supervisor = SupervisorAgent()

    print("\n" + "="*60)
    print(" Multi-Agent Orchestration Platform")
    print("="*60)
    print("Type your query below. Type 'exit' to quit.\n")

    while True:
              try:
                            user_input = input("You: ").strip()
                            if not user_input:
                                              continue
                                          if user_input.lower() in ("exit", "quit", "q"):
                                                            print("Shutting down. Goodbye!")
                                                            break

                            logger.info(f"Processing query: {user_input[:80]}...")
                            response = supervisor.run(user_input)
                            print(f"\nAgent: {response}\n")

              except KeyboardInterrupt:
                            print("\nShutting down. Goodbye!")
                            break
except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"\nError: {e}\n")


if __name__ == "__main__":
      main()
  
