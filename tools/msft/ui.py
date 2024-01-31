import gradio as gr
from .service import run

inputs=[
    gr.Number(label="Amount"),
    gr.Dropdown(label="Webdriver", choices=["Firefox", "Chrome"], value="Firefox"),
    gr.Text(label="Signup link", value="https://signup.live.com/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1605407946&rver=7.0.6738.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252F%253Frefp%253Dsignedout-index&lc=1033&id=292666&lw=1&fl=easi2&mkt=en-US")
]

ui = gr.Interface(fn=run, title="MSFT", inputs=inputs , outputs=[gr.Text(label="Output")])
