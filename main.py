import os
import openai
from datetime import date
import discord
import discord.ext
import interactions
from dotenv import load_dotenv
load_dotenv()
bot = interactions.Client(token=os.getenv('token'))
openai.api_key = os.getenv('apikey')

@bot.command(
    name="chatgpt",
    description="Ask ChatGPT a question!",
    scope=630048726823731230,
    options = [
        interactions.Option(
            name="prompt",
            description="ChatGPT Prompt",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def chatgpt(ctx: interactions.CommandContext, prompt: str):
    waitEmbed=interactions.Embed(title="ChatGPT", description="Please wait..", color=0xfee75c)
    waitEmbed.set_footer(text=f"Your question was: '{prompt}'")
    message = await ctx.send(embeds=waitEmbed)
    completion = openai.Completion.create(
        engine="text-chat-davinci-002-20221122",
        prompt=f"Respond conversationally. If the response is code, after the first three backticks put the coding languages name. example: ```py then at the end of the code put another three backticks, ```. If it is not code do not put any backticks at all. \n\nUser:\n{prompt}<|im_sep|>\nAI:",
        max_tokens=3000,
        n=1,
        stop=['<|im_end|>'],
        temperature=0.8,
        presence_penalty=1
    )
    response = completion.choices[0].text
    successEmbed=interactions.Embed(title="ChatGPT", description=response, color=0x57f287)
    successEmbed.set_footer(text=f"Your question was: '{prompt}'")
    await message.edit(embeds=successEmbed)

@bot.command(
    name="imagegpt",
    description="Generate an image using GPT-3!",
    scope=630048726823731230,
    options = [
        interactions.Option(
            name="image",
            description="ImageGPT Prompt",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def imagegpt(ctx: interactions.CommandContext, image: str):
    waitEmbed=interactions.Embed(title="ImageGPT", description="Please wait..", color=0xfee75c)
    waitEmbed.set_footer(text=f"Your image was: '{image}'")
    message = await ctx.send(embeds=waitEmbed)
    response = openai.Image.create(
      prompt=image,
      n=1,
      size="1024x1024"
    )
    print(response['data'][0]['url'])
    type(response)
    successEmbed=interactions.Embed(title="ImageGPT", description=response, color=0x57f287)
    successEmbed.set_footer(text=f"Your image was: '{image}'")
    successEmbed.set_image(url=f"{response['data'][0]['url']}")
    await message.edit(embeds=successEmbed)
    


bot.start()
