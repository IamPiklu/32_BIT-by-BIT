from pdf2image import convert_from_path
import base64
import requests
import io
from PIL import Image
from openai import OpenAI
import PyPDF2
import time

# OpenAI API Key
api_key = ""
client = OpenAI(api_key=api_key)


# Function to encode the image
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def get_image_text(base64_image):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "the image is of a answer script , i want you to transcribe it and dont add anything of your own message just transcribe whatever you can and maintain numbering",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()["choices"][0]["message"]["content"]


def handwriting_to_text(pdf_path):
    # Convert the PDF to images
    images = convert_from_path(pdf_path)

    # Initialize an empty string to hold the text
    all_text = ""

    # Loop through the images and get the text
    for i, image in enumerate(images):
        base64_image = encode_image(image)
        text = get_image_text(base64_image)

        # Append the text to the all_text variable
        all_text += text + "\n"
    return all_text


def guide_to_txt(pdf_path):
    # Open the PDF file in binary mode
    with open(pdf_path, "rb") as pdf_file:
        # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to hold the text
        text = ""

        # Loop through each page in the PDF and extract the text
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


def wait_for_assistant(thread, run):
    """
    Function to periodically check run status of AI assistant and print run time
    """

    # wait for assistant process prompt
    t0 = time.time()
    while run.status != "completed":

        # retreive status of run (this might take a few seconds or more)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # wait 0.5 seconds
        time.sleep(0.25)
    dt = time.time() - t0
    print("Elapsed time: " + str(dt) + " seconds")

    return run


def compare(prompt):
    # create thread (i.e. object that handles conversations between user and assistant)
    thread = client.beta.threads.create()

    # # generate user message
    # user_message = "Great content, thank you!"

    # add a user message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=prompt
    )

    # send message to assistant to generate a response
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_5gZUXFofdL0rWKhkAVVDPuVA",
    )
    run = wait_for_assistant(thread, run)
    # view messages added to thread

    messages = client.beta.threads.messages.list(thread_id=run.thread_id)

    return messages.data[0].content[0].text.value


# if __name__ == "__main__":
#     # ocr
#     pdf_path = "C:\\Desktop\\hack\\hackfest\\esp\\my\\ESP_2.pdf"  # replace with your actual PDF path
#     answers_text = handwriting_to_text(pdf_path)

#     # guide to txt

#     # Path to your PDF file
#     pdf_path = r"C:\Desktop\hack\hackfest\esp\tg.pdf"
#     # Convert the PDF to text
#     guide_text = guide_to_txt(pdf_path)

#     prompt = (
#         "below is the teachers guide\n\n"
#         + guide_text
#         + "\n\n\n\n\nbelow is the transcription of a students answer script \n\n"
#         + answers_text
#         + "\n\n\n\n\nI want you to evaluate the students answer script based on teacher's guide. Teachers guide contains the bare minimum points or keywords that the teacher is looking for in the answer.\nRules for evaluation:-\n1)ignore spelling and grammar mistake\n2)marking allotted for each answers is mentioned in teachers guide\n3)give full marks if all the points from the teachers guide are present in the students answers\n4)if points are missing then give marks accordingly or partially\nreturn the total marks obtained by the student at the last"
#     )
#     review = compare(prompt)
#     print(review)
