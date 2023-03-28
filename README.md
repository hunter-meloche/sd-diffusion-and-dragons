# Diffusion and Dragons (DnD)
## About
DnD is a tool for game masters to add visual and literary color to their sessions. DnD generates detailed image prompts and text descriptions meant to be read to player based on simple phrases as input, like 'a dog' or 'a dungeon room'. When players go off the rails of your campaign, DnD is here to help you

You need to input your [openAI API key](https://platform.openai.com/account/api-keys) the first time you use DnD.

![image](https://user-images.githubusercontent.com/123516285/228127446-a500fe96-325d-4143-ac12-c4bdd61adc24.png)

## Plans
I'll be adding a long term memory solution that keeps track of the world, objects, and NPCs. This way you can have accurate dialogue with recurring characters and randomly generated characters will persist. This will make the game world become more alive than ever before. If anyone knows of a smart way to do this, please let me know. Right now, I'm thinking of keeping a prompt log locally that appends to a Redis embedding store that launches with DnD every time sd-web-ui starts.

## Example Usage
**You can generate detailed paragraphs about creature's and places from just a few words.**
```
Input:
a wizard's bedroom

Description Output:
The wizard's bedroom exudes an air of mystique and enchantment. 
Cobwebs cling to the corners of the room, adding to the otherworldly atmosphere. 
bookshelf lines the wall, filled to the brim with ancient tomes and spell books, their spines cracked and faded with age. 
The bed in the center of the room is adorned with velvet sheets, the colors of midnight and amethyst. 
A towering headboard looms over the bed, intricately carved with symbols and runes. 
Two ornate nightstands flank the bed, each holding a flickering candle, casting a warm glow over the room. 
The floor is covered in a plush red rug, making each step feel like you're walking on clouds. 
As your eyes adjust to the dim lighting, you see a desk in the corner of the room, covered in various magical artifacts and parchment. 
The walls themselves seem to pulse with an otherworldly energy, giving you a sense of awe and reverence. 
It's clear that this is the sleeping quarters of a powerful wizard, and you can't help but feel a sense of reverence for the magic that permeates the room.
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
