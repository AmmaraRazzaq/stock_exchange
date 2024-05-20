import time 
import streamlit as st
from io import BytesIO
from PIL import Image
from openai import OpenAI
client = OpenAI(api_key="sk-proj-9HFr86mSr3umkWtNNkVHT3BlbkFJjvt6xmESlrbFIsTLh5U3")
ASSISTANT_ID = "asst_OMhIPr3WGKc4rkbdo71frQba"

query = st.text_input("Type your query?")
# query = "Give me the complete historic trend of Saudi Arabia Refineries Co."

if query:
    # create a thread with a message 
    thread = client.beta.threads.create(
        messages=[
            {
                "role":"user",
                "content":f"{query}"
            }
        ]
    )

    # submit the thread to the assistant (as a new run)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    ) 
    print(f"run created: {run.id}")

    # wait for run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"run status: {run.status}")
        time.sleep(1)
    else:
        print("Run Completed")


    # Get the latest message from the thread 
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data 

    # print the latest message 
    latest_message = messages[0]
    for message_content in latest_message.content:
        if hasattr(message_content, "image_file"):
            file_id = message_content.image_file.file_id
            resp = client.files.with_raw_response.content(file_id)
            if resp.status_code == 200:
                image_data = BytesIO(resp.content)
                image = Image.open(image_data)
                # image.save("openai_image.png")
                st.image(image)
            else:
                st.write("Error in retrieving the image")
        
        elif hasattr(message_content, "text"):
            st.write(message_content.text.value)
                   
    # print(f"latest_message: {latest_message.content[0].text.value}")
    # st.write(latest_message.content[0].text.value)

