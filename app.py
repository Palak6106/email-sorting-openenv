
import gradio as gr
from inference import *   # assuming your logic is here

def run_app(input_text):
    # modify this based on your function
    return "Output: " + input_text

demo = gr.Interface(
    fn=run_app,
    inputs=gr.Textbox(label="Enter Email/Text"),
    outputs=gr.Textbox(label="Result"),
    title="Email Sorting System"
)

demo.launch()