# Diffusion and Dragons
[stable-diffusion-web-ui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension that generates detailed prompts with ChatGPT

## About
This is in early testing. As of now, all it does is take a simple natural language prompt and make a more detailed one that's formatted as an image generation prompt. You need to manually put your [openAI API key](https://platform.openai.com/account/api-keys) into [main.py](https://github.com/hunter-meloche/sd-diffusion-dragons/blob/fd7337df5107b2626ce4e703f7fc8089a8483665/scripts/main.py#L9). I'll be adding a button through the UI that takes care of this for you later on. Shoutout to [controlnet](https://github.com/Mikubill/sd-webui-controlnet) and [text2prompt](https://github.com/toshiaki1729/stable-diffusion-webui-text2prompt) because I frankensteined your code together to make this.

## Plans
I want this to be the ultimate AI tool for dungeon masters. You say "You walk into a spooky room" and ChatGPT gives you a super detailed description of the room with the proper (and modular) context. You'll be able to feed it details about your setting in a separate box that it can reference when it generates its descriptions. You can use these generated descriptions to DM and read to your players for immersion and ideas. This description is then fed back into ChatGPT to create a Stable Diffusion version of the description so your players have a cool visual aid for the room their characters have walked into or the monster they're fighting.

## Example Usage
```
Input:
atlantis

Output:
Underwater city, ancient ruins, bioluminescent structures, schools of fish, merfolk inhabitants
```
