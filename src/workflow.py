import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Set up logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

# Open and read the YAML file
with open("./src/visa.yaml", encoding="utf-8") as f:
    prompts_data = yaml.safe_load(f)

system_prompt = prompts_data.get('system_prompt', '')
user_prompt = prompts_data.get('user_prompt', '')

def visa_question_answering_batch(question: str, country: str = "US", model: str = "gpt-4o") -> str:
    """
    Function to answer visa-related questions using OpenAI's API in a batch manner.

    Parameters:
    - question: The visa-related question to be answered.
    - country: The country context for the question (default is "US").
    - model: The OpenAI model to use for generating the answer (default is "gpt-4o").

    Returns:
    - A string containing the complete answer to the question.
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Populate prompts with dynamic content
    system_prompt_populated = system_prompt.replace("<country>", country)
    user_prompt_populated = user_prompt.replace("<question>", question)

    try:
        # Create a chat completion request without streaming
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt_populated},
                {"role": "user", "content": user_prompt_populated},
            ]
        )

        # Return the complete response
        return completion.choices[0].message.content

    except Exception as e:
        logger.error("Error during OpenAI API call: %s", e)
        raise

def visa_question_answering_stream(question: str, country: str = "US", model: str = "gpt-4o"):
    logger.info("Starting stream for question: %s, country: %s", question, country)
    system_prompt_populated = system_prompt.replace("<country>", country)
    user_prompt_populated = user_prompt.replace("<question>", question)
    logger.info("System prompt: %s", system_prompt_populated)
    logger.info("User prompt: %s", user_prompt_populated)
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt_populated},
                {"role": "user", "content": user_prompt_populated},
            ],
            stream=True
        )
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content is not None:
                logger.info("Streaming chunk: %s", content)
                yield content
        logger.info("Stream completed successfully")
    except Exception as e:
        logger.error("Error during OpenAI API call: %s", e)
        raise
    finally:
        logger.info("Stream closed")