# Diffusion and Dragons
[stable-diffusion-web-ui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension that generates detailed prompts with ChatGPT

## About
This is in early testing. As of now, all it does is take a simple natural language prompt and make a more detailed one that's formatted as an image generation prompt. You need to manually put your [openAI API key](https://platform.openai.com/account/api-keys) into [main.py](https://github.com/hunter-meloche/sd-diffusion-dragons/blob/fd7337df5107b2626ce4e703f7fc8089a8483665/scripts/main.py#L9). I'll be adding a button through the UI that takes care of this for you later on. Shoutout to [controlnet](https://github.com/Mikubill/sd-webui-controlnet) and [text2prompt](https://github.com/toshiaki1729/stable-diffusion-webui-text2prompt) because I frankensteined your code together to make this.

## Plans
I want this to be the ultimate AI tool for dungeon masters. You say "You walk into a spooky room" and ChatGPT gives you a super detailed description of the room with the proper (and modular) context. You'll be able to feed it details about your setting in a separate box that it can reference when it generates its descriptions. You can use these generated descriptions to DM and read to your players for immersion and ideas. This description is then fed back into ChatGPT to create a Stable Diffusion version of the description so your players have a cool visual aid for the room their characters have walked into or the monster they're fighting.

## Example Usage
```
Input:
fantasy tavern

Output:
tavern, fantasy, dimly-lit, cozy atmosphere, wooden bar, stained glass windows, fireplace, hanging lanterns, kegs of ale, bar stools, dusty tapestries, wandering minstrel, patrons enjoying drinks, mysterious hooded figure in the corner
```
Before:

![image](https://user-images.githubusercontent.com/123516285/226485681-d0357f69-8a87-4c34-ba2c-7d09701aca47.png)


After:

![image](https://user-images.githubusercontent.com/123516285/226485787-e9bcfd1e-cf2c-48ea-b950-2648fb259427.png)

```
Input:
an armored warrior

Output:
Armored warrior, male, muscular, tall, long hair, wielding sword, full plate armor, battle-worn, standing on rocky terrain, facing towards the viewer, intense gaze
```

Before:

![image](https://user-images.githubusercontent.com/123516285/226486704-1c7e8ac7-b0a5-42c4-96af-ce64dd661717.png)


After:

![image](https://user-images.githubusercontent.com/123516285/226486552-ed34542f-330b-43ae-af64-2d92e34e6d38.png)
