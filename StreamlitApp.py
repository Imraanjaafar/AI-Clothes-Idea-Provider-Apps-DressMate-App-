import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import requests

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Confirm Button
def clothes_idea_provider(msg):
    idea_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an AI Clothes Idea Provider,
                                Your goal is to suggest the perfect outfit based on the user's choice."""
            },
            {
                "role": "user",
                "content": f'{msg}'
            }
        ],
        max_tokens=500,
        temperature=1.3
    )

    return idea_response.choices[0].message.content

def clothes_idea_image(msg):
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=f"Clothing idea for {msg} in pixar style",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return image_response.data[0].url


def clothes_design_ai(msg):
    design_response_generate = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an AI Clothes Idea Provider.
                    Generate a detailed image prompt for the suggested clothing based on the user's choice.
                    """
            },
            {
                "role": "user",
                "content": f'{msg}'
            }
        ],
        max_tokens=400,
        temperature=1.3
    )

    return design_response_generate.choices[0].message.content

# Generate Input button
def clothes_idea_provider_generate(msg_generate):
    idea_response_generate = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an AI Clothes Idea Provider,
                                Your goal is to suggest the perfect outfit based on the user's description."""
            },
            {
                "role": "user",
                "content": f'{msg_generate}'
            }
        ],
        max_tokens=500,
        temperature=1.3
    )

    return idea_response_generate.choices[0].message.content

def generate_clothes_idea_image_generate(msg_generate):
    image_response_generate = client.images.generate(
        model="dall-e-3",
        prompt=f"Clothing idea for {msg_generate} in pixar style",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return image_response_generate.data[0].url

def design_ai_generate(msg_generate):
    design_response_generate = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an AI Clothes Idea Provider.
                    Generate a detailed image prompt for the suggested clothing based on the user's description.
                    The prompt should include relevant style or colour, suitable for the given context."""
            },
            {
                "role": "user",
                "content": f'{msg_generate}'
            }
        ],
        max_tokens=400,
        temperature=1.3
    )

    return design_response_generate.choices[0].message.content

# Streamlit App
st.title("👗 DressMate")
st.write("AI Clothes Idea Provider App 🤖")

# Homepage options
option = st.selectbox("Choose an option to get started:", ["Any", "Choices", "Text Input"])

if option == "Any":
    st.markdown("## Welcome to DressMate - Dress to Impress!👔")
    st.markdown("""

DressMate is an innovative app designed to help you discover the perfect outfit for any occasion effortlessly. Whether you prefer making choices or providing a text description, DressMate leverages the power of AI to generate personalized clothing suggestions and designs just for you.

### Options:

- Choices: Customize your wardrobe by selecting your gender, age, clothing types, and more.
- Text Input: Describe your desired outfit, and DressMate will generate a personalized suggestion based on your input.

### How it Works:

##### 1. Choices Page:
- Select your gender, age, and preferences for top and bottom, shoe types, and occasions.
- Click "Confirm" to generate a detailed clothing suggestion, complete with a design and image.

##### 2. Text Input Page:
- Describe the occasion and style you have in mind using the text area.
- Click "Generate Input" to receive a unique clothing suggestion, along with a detailed design and image.

### Get Started:
- Choose an option from the dropdown menu.
- Follow the prompts and selections for a personalized clothing experience.
- Enjoy DressMate's AI-generated outfit suggestions tailored just for you!

## Get ready to elevate your style with DressMate! 🚀

""")

elif option == "Choices":
    st.markdown("## Choices Page 👚👖")

    gender = st.selectbox("Gender:", options=['Any', 'Men', 'Women'])
    age = st.selectbox("Categories:", options=['Any', 'Kids', 'Teen', 'Adult', 'Elderly'])
    tops = st.selectbox("Top:", options=['Any', 'T-Shirts', 'Shirts', 'Blouses(Women)', 'Hoodies', 'Sweaters', 'Jackets', 'Coats', 'Dresses'])
    low = st.selectbox("Bottom:", options=['Any', 'Jeans', 'Trousers', 'Shorts', 'Skirts(Women)', 'Joggers', 'Cargo Pants', 'Palazzo Pants', 'Chinos', 'Sweatpants', 'Dresses'])
    shoe_type = st.selectbox("Type of Shoe:", options=['Any', 'Athletic Shoes', 'Sneakers', 'Flats', 'Heels(women)', 'Sandals', 'Boots', 'Loafers', 'Hiking Boots'])
    dress_reason = st.selectbox("Occasion/Reason/Type of Events:", options=['Any', 'Formal', 'Casual', 'Work', 'Sports', 'Special Celebrations', 'Travel'])
    confirm_button = st.button("Confirm 👍")

    if confirm_button:
        msg = f"Gender: {gender}, Age: {age}, Tops: {tops}, Lowers: {low}, Shoe Type: {shoe_type}, Occasion: {dress_reason}"
        with st.spinner("Generating your clothes..."):
            clothing_suggestion = clothes_idea_provider(msg)
            clothes_design = clothes_design_ai(clothing_suggestion)
            clothes_image = clothes_idea_image(clothing_suggestion)

            # Display results
            st.header("Your clothes idea image 🌟")
            cl_image = Image.open(requests.get(clothes_image, stream=True).raw)
            st.image(cl_image, caption="The Clothes Idea")

            st.header("Clothing Suggestion:")
            st.write(clothing_suggestion)

            st.header("Clothing Design:")
            st.write(clothes_design)

elif option == "Text Input":
    st.markdown("## Text Input Page ✍️")

    user_input = st.text_area("Describe the occasion and style you want:", height=100)
    generate_button = st.button("Generate Input 🔄")

    if generate_button:
        with st.spinner("Generating your clothes..."):
            # Modify the msg based on what you want for the generate button
            clothes_suggestion_generate = clothes_idea_provider_generate(user_input)
            clothes_design_generate = design_ai_generate(clothes_suggestion_generate)
            clothes_image_generate = generate_clothes_idea_image_generate(clothes_design_generate)

            # Display Results
            st.header("Your clothes idea image 🌟")
            cl_image = Image.open(requests.get(clothes_image_generate, stream=True).raw)
            st.image(cl_image, caption="The Clothes Idea")

            st.header("Clothing Suggestion:")
            st.write(clothes_suggestion_generate)

            st.header("Clothing Design:")
            st.write(clothes_design_generate)
