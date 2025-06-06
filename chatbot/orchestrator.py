import logging
import os
from datetime import datetime
from chatbot.conversation import call_llm
from chatbot.memory import save_context_to_file
from tenacity import retry, stop_after_attempt, wait_exponential

# Define log file path relative to project root
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "orchestration.log")

# Remove existing handlers if any (to avoid conflicts)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    handler.flush()

# Configure logging to file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Logging initialized.")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def orchestrated_llm_call(user_input, context):
    start_time = datetime.now()
    logging.info("START orchestration pipeline")

    try:
        logging.info("Calling LLM with user input: %s", user_input)
        response, updated_context = call_llm(user_input, context)
        logging.info("LLM call completed successfully")

        # Save context to file (note: save_context_to_file() does NOT accept 'username' argument)
        filename = f"medical_session_{updated_context.get('session_id', 'unknown')}.json"
        save_msg = save_context_to_file(updated_context, filename=filename)
        logging.info("Context saved: %s", save_msg)

        duration = (datetime.now() - start_time).total_seconds()
        logging.info("Orchestration finished in %.2f seconds", duration)

        return response, updated_context

    except Exception as e:
        logging.error("LLM call failed: %s", str(e))
        raise  # triggers retry
