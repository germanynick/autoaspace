import gradio as gr
import time
from .service import run, tooggle_running

import random
import time


def toggle():
    running = tooggle_running()
    label = "Stop" if running else "Start"
    return gr.update(value=label)


with gr.Blocks(title="Discord") as ui:
    with gr.Row():
        with gr.Column() as main:
            token =  gr.Textbox(label="Discord Token", type="password")
            bot_name = gr.Textbox(label="Bot Name")
            channel = gr.Textbox(label="Channel ID")
            ids = gr.Textbox(label="User IDs")

            start_btn = gr.Button("Start", variant="primary")

        with gr.Column() as output:
            chat = gr.Chatbot(value=[["Welcome to the chatbot!", None]])

            start_btn.click(toggle, outputs=start_btn).then(run, inputs=[token, channel, bot_name, ids, chat], outputs=chat)
            
       