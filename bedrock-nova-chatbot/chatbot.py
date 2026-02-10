import boto3
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

print(" Daksh Manohar Chatbot  (type 'exit' to quit)\n")

messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": [{"text": user_input}]
    })

    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=messages,
        inferenceConfig={
            "maxTokens": 400,
            "temperature": 0.7,
            "topP": 0.9
        }
    )

    assistant_reply = response["output"]["message"]["content"][0]["text"]

    messages.append({
        "role": "assistant",
        "content": [{"text": assistant_reply}]
    })

    print("\nDaksh:", assistant_reply, "\n")
