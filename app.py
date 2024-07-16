import streamlit as st
import openai
import os
from dotenv import load_dotenv
import random
import time

# Load environment variables
load_dotenv()

# Function to get API key
def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    else:
        return st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else None

# Set your OpenAI API key
api_key = "sk-None-QyMVE66IlLxu49ZfRo6KT3BlbkFJUZp6EvCaTfdbrViZuKml"

if api_key:
    openai.api_key = api_key
else:
    st.error("No API key found. Please set your OpenAI API key.")
    st.stop()

# Create a Streamlit app
st.title("AI Image Generator")
st.write("Enter a prompt to generate an image:")

# Create a text input field for the prompt
prompt = st.text_input("Prompt:", value="A cute baby sea otter")

# Create a dropdown menu to select the image size
size_options = ["1024x1024", "1024x1792", "1792x1024"]
size = st.selectbox("Image Size:", size_options, index=0)

# Create a dropdown menu to select the quality
quality_options = ["standard", "hd"]
quality = st.selectbox("Image Quality:", quality_options, index=0)

# Create a checkbox to toggle between mock and real API
use_mock_api = st.checkbox("Use Mock API (for testing)", value=False)

# Create a button to generate the image
generate_button = st.button("Generate Image")

# Function to generate image using OpenAI API
def generate_image_openai(prompt, size, quality):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=size,
            quality=quality
        )
        image_url = response.data[0].url
        return image_url
    except openai.error.OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Mock image generation function
def mock_generate_image(prompt, size, quality):
    placeholder_images = [
        "https://picsum.photos/1024/1024",
        "https://picsum.photos/1024/1792",
        "https://picsum.photos/1792/1024"
    ]
    time.sleep(2)  # Simulate API delay
    return random.choice(placeholder_images)

# Generate the image when the button is clicked
if generate_button:
    if not api_key and not use_mock_api:
        st.error("API key is not set. Please set your OpenAI API key to use this feature.")
    else:
        with st.spinner("Generating image..."):
            if use_mock_api:
                image_url = mock_generate_image(prompt, size, quality)
                if image_url:
                    st.write("Generated Image (Mock):")
                    st.image(image_url, use_column_width=True)
            else:
                image_url = generate_image_openai(prompt, size, quality)
                if image_url:
                    st.write("Generated Image:")
                    st.image(image_url, use_column_width=True)

# Add a footer with a disclaimer and usage warning
st.markdown("---")
st.write("Disclaimer: This app uses OpenAI's DALL-E 3 model. Please ensure you comply with OpenAI's usage policies.")
st.warning("Note: This app uses the OpenAI API, which has usage limits. If image generation fails, you may have reached your limit.")

# Display current settings
st.sidebar.header("Current Settings")
st.sidebar.write(f"API Mode: {'Mock' if use_mock_api else 'Real'}")
st.sidebar.write(f"Size: {size}")
st.sidebar.write(f"Quality: {quality}")