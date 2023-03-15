import openai
import toml
import streamlit as st
import re

openai.api_key = st.secrets["api_key"]

@st.cache_data(show_spinner=False)
def generate_outline(topic):
    prompt = [{"role": "system", "content": "You are a helpful assistant that creates an outline for learning a given topic."},
              {"role": "user", "content": f"Create an outline for learning the topic: {topic}. Each topic should be on a new line, with a bullet point infront of each topic, nothing else. Please omit any headings with title such as Introduction to ..."}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return completion.choices[0].message.content


@st.cache_data
def parse_content(content):
    sections = re.split(r'\n{1,}', content)
    return [section.strip("- ").strip() for section in sections]


@st.cache_data(show_spinner = False)
def generate_module_content(topic, module):
   prompt = [{"role": "system", "content": "You are a helpful assistant that provides explanations for modules in a learning topic."},
              {"role": "user", "content": f"Explain the {module} module for learning the topic: {topic} in great detail with examples if needed."}]
   completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
   return completion.choices[0].message.content


st.header("What do you want to learn?")
user_topic = st.text_input("Enter a topic")


if user_topic:
    outline = generate_outline(user_topic)
    sections = parse_content(outline)
    
    if sections:
        selected_module = st.selectbox("Select a module:", sections)
        module_content = generate_module_content(user_topic, selected_module)
        st.markdown(f"## {selected_module}")
        st.markdown(module_content)
    else:
        st.write("No content available for given topic.")

# st.write(message_history)