# fashion-tryon

Anyone can now be a fashion model and walk the runway! *The future of how we dress, how we try on outfits before purchasing, and even how we find items online will be shaped by AI*.

## How it works

1. Start by uploading an image of yourself or a friend
2. Once you upload the image, the app will find 5 high fashion outfits that suit you well. [Mistral](https://mistral.ai/) generates descriptions of outfits based on who is in the photo, as determined by a caption using florence-2-large on [fal.ai](fal.ai). Then, we use Flux from [Black Forest Labs](https://blackforestlabs.ai/) to generate an image based on the outfit description. cat-vton is the model used to try on the outfit for the given user.

** The other option here is to use a Flux LoRA which you can train [here](https://fal.ai/models/fal-ai/flux-lora-general-training/playground). Input the lora file into the input field and the virtual try-on images will look more like you.
4. Select the outfits you like, then click "Start Show"
5. This will generate a video of you in those outfits walking the runway. We use [Luma Dream Machine](https://lumalabs.ai/dream-machine) because they recently released their API. You can also use [Viggle](https://viggle.ai/home) for some fun effects on their playground. Input the AI-generated images into the text/image to video models to get a "walk the runway" video. 
6. Add AI-generated music from [Udio](https://www.udio.com/home) to go along with your walk if you wish!
7. Run [Browserbase](https://www.browserbase.com/) web agent script to find a similar online and add it to your shopping cart for your review before you purchase.

## Setup

Add your own API keys in .env file for Fal.ai, Mistral, and Browserbase

Run **streamlit run main.py**

amazonSearch.js contains the web agent script. Either run it in the browserbase playground to modify it for your own taste or run it locally.

## Future Directions

Improve web agent shopping feature - certain actions are blocked (Amazon uses sophisticated systems to detect non-human behavior). Integrating with more shopping sites without bot detection can increase scope and help find a more similar outfit. Doing a similarity search between images and not just captions will also result in better results, as will adding filters for price / brand / material / etc. 

Longer runway videos are currently still expensive and object persistence needs improvement
