# Diffusion and Dragons
## About
This is in early testing. As of now, all it does is take a simple natural language prompt and make a more detailed one, either as descriptive paragraphs or intricate image prompts. You need to manually put your [openAI API key](https://platform.openai.com/account/api-keys) into [main.py](https://github.com/hunter-meloche/sd-diffusion-dragons/blob/fd7337df5107b2626ce4e703f7fc8089a8483665/scripts/main.py#L9). I'll be adding a button through the UI that takes care of this for you later on. Shoutout to [controlnet](https://github.com/Mikubill/sd-webui-controlnet) and [text2prompt](https://github.com/toshiaki1729/stable-diffusion-webui-text2prompt) because I frankensteined your code together to make this.

![image](https://user-images.githubusercontent.com/123516285/226503708-4c0cc703-023d-4e57-960a-1bd6efafaac7.png)

## Plans
I want this to be the ultimate AI tool for dungeon masters. You say your players walk into "a spooky room" and ChatGPT gives you a super detailed description of the room with the proper (and modular) context. You'll be able to feed it details about your setting in a separate box that it can reference when it generates its descriptions. You can use these generated descriptions to DM and read to your players for immersion and ideas. This description is then fed back into ChatGPT to create a Stable Diffusion version of the description so your players have a cool visual aid for the room their characters have walked into or the monster they're fighting.

## Example Usage
**You can generate detailed paragraphs about creature's and places from just a few words.**
```
Input:
a wizard's bedroom

Description Output:
The wizard's bedroom exudes an air of mystique and enchantment. Cobwebs cling to the corners of the room, adding to the otherworldly atmosphere. A bookshelf lines the wall, filled to the brim with ancient tomes and spell books, their spines cracked and faded with age. The bed in the center of the room is adorned with velvet sheets, the colors of midnight and amethyst. A towering headboard looms over the bed, intricately carved with symbols and runes. Two ornate nightstands flank the bed, each holding a flickering candle, casting a warm glow over the room. The floor is covered in a plush red rug, making each step feel like you're walking on clouds. As your eyes adjust to the dim lighting, you see a desk in the corner of the room, covered in various magical artifacts and parchment. The walls themselves seem to pulse with an otherworldly energy, giving you a sense of awe and reverence. It's clear that this is the sleeping quarters of a powerful wizard, and you can't help but feel a sense of reverence for the magic that permeates the room.
```
**You can also generate detailed image prompts the same way**
```
Input:
an armored warrior

Image Prompt Output:
Armored warrior, male, muscular, tall, long hair, wielding sword, full plate armor, battle-worn, standing on rocky terrain, facing towards the viewer, intense gaze
```
Before:

![image](https://user-images.githubusercontent.com/123516285/226486704-1c7e8ac7-b0a5-42c4-96af-ce64dd661717.png)


After:

![image](https://user-images.githubusercontent.com/123516285/226486552-ed34542f-330b-43ae-af64-2d92e34e6d38.png)
