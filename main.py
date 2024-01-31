
import gradio as gr
from tools.discord import ui as discord_tab
from tools.msft import ui as msft_tab


if __name__ == '__main__':
    tabs = [discord_tab, msft_tab]
    names = [tab.title for tab in tabs]
    ui = gr.TabbedInterface(interface_list=tabs, tab_names=names)
    ui.launch()