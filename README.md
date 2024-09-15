# fashion-tryon

Anyone can now be a fashion model and walk the runway! *The future of how we dress, how we try on outfits before purchasing, and even how we find items online will be shaped by AI*.

## How it works

1. Start by uploading an image of yourself or a friend
2. Once you upload the image, the app will find 10 high fashion outfits that suit you well. [Mistral](https://mistral.ai/) generates descriptions of outfits based on who is in the photo, as determined by a caption using florence-2-large on [fal.ai](fal.ai). Then, we use Flux from [Black Forest Labs](https://blackforestlabs.ai/) to generate an image based on the outfit description. cat-vton is the model used to try on the outfit for the given user.
3. Select the outfits you like, then click "Start Show"
4. This will generate a video of you in those outfits walking the runway (Note: this step is currently using [Luma Dream Machine](https://lumalabs.ai/dream-machine) (to extend scene) and [Viggle](https://viggle.ai/home) (to generate walk)'s platforms since there's no publicly available API yet. Input the AI-generated images into the text/image to video models to get a "walk the runway" video. This will be updated to directly generate in the app once API's are released.)
5. Add AI-generated music from [Udio](https://www.udio.com/home) to go along with your walk if you wish!

## Setup

Add your own API keys in .env file for Fal.ai and Mistral

Run **streamlit run main.py**
