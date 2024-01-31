import gradio as gr
from .service import run

ui = gr.Interface(fn=run, title="Discord",  inputs=[gr.Textbox(label="Name")], outputs=[gr.Text(label="Greeting")])
