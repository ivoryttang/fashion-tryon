# fashion-tryon

Anyone can now be a fashion model and walk the runway! The future of how we dress and try on outfits before purchase will be shaped by AI.

## How it works

1. Start by uploading an image of yourself (or a friend)
2. Once you upload the image, the app will find 10 high fashion outfits that suit you well (Mistral-generated based on who is in the photo)
3. Select the outfits you like, then click "Start Show"
4. This will generate a video of you in those outfits walking the runway (note: this is currently using Luma AI (to extend scene) and Viggle (to generate walk)'s platforms since there's no publicly available API yet)
5. Add AI-generated music from Udio to go along with your walk if you wish!

## Setup

Add your own API keys in .env file for Fal.ai and Mistral

Run streamlit run main.py
