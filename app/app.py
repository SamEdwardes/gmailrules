import xmltodict
from rich import print
from shiny import App, render_text, ui

from .models import RuleSet

# Get test data
with open("example-rules/example1.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

print(data_dict)
rule_set = RuleSet(**data_dict)
print(rule_set)



app_ui = ui.page_fluid(
    ui.input_slider("n", "N", 0, 100, 40),
    ui.output_text_verbatim("txt"),
)

def server(input, output, session):
    @output()
    @render_text()
    def txt():
        return f"The value of n*2 is {input.n() * 2}"

# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server)
