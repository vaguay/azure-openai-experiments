import os

import azure.identity
import openai
from dotenv import load_dotenv
import sys

#prompt = "Say hello!"
#if len(sys.argv) > 1:
 #   prompt = " ".join(sys.argv[1:])

 history = []
while True:
    user = input("you> ").strip()
    if user.lower() in {"exit", "quit"}:
        break
    history.append({"role":"user","content":user})
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role":"system","content":"You are a helpful assistant."}] + history
    )
    reply = resp.choices[0].message.content
    print("bot>", reply)
    history.append({"role":"assistant","content":reply})



# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that makes lots of cat references and uses emojis."},
        {"role": "user", "content": "Write a haiku about a hungry cat who wants tuna"},
    ],
)

print(f"Response from {API_HOST}: \n")
print(response.choices[0].message.content)
