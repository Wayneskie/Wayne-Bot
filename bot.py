import discord
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HUGGING_FACE_API_KEY = "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"

def query_hugging_face_api(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
            "temperature": 0.7,
            "top_p": 0.9,
        }
    }

    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)

    print(f"Response Status: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"Response Data: {response_data}")
            return response_data[0].get('generated_text', "No generated text found.")
        except KeyError as e:
            return f"Error: Unable to parse response - {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

@tree.command(name="information", description="Get information about the bot.")
async def information(interaction: discord.Interaction):
    information_text = (
        "```Information*\n"
        "This bot uses Hugging Face's GPT-2 model to generate responses. "
        "It processes user prompts and generates natural language replies. "
        "You can ask questions or chat with the bot using the `!ask` command.\n\n"
        "Details:\n"
        "- Model: GPT-2\n"
        "- API: Hugging Face Inference API\n"
        "- Features: Supports responses up to 150 tokens with adjustable randomness and diversity settings.\n\n"
        "Created by Wayne.\n"
        "```"
    )
    await interaction.response.send_message(information_text)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Received message: {message.content}")

    if message.content.startswith("!ai"):
        prompt = message.content[len("!ai "):].strip()
        if prompt:
            ai_response = query_hugging_face_api(prompt)
            await message.channel.send(ai_response)
        else:
            await message.channel.send("Please provide a prompt after the !ai command!")

client.run('Your-Token')
#Make By Wayne
