from collections import defaultdict
import xmltodict
from rich import print, inspect
from shiny import App, render_text, ui, render_ui

from models import RuleSet, Action, AppPropertyTidy
import json


# ------------------------------------------------------------------------------
# START UP
# ------------------------------------------------------------------------------
# Get test data
with open("../example-rules/example1.xml") as xml_file:
    GMAIL_XML_RAW = xml_file.read()
    GMAIL_XML_DICT = xmltodict.parse(GMAIL_XML_RAW)

# Save to disk
with open("example.json", "w") as f:
    GMAIL_XML_JSON = json.dumps(GMAIL_XML_DICT, indent=4)
    f.write(GMAIL_XML_JSON)


# ------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------
app_ui = ui.page_fluid(
    ui.h1("Gmail rule creator"),
    ui.p("A nicer UI for creating Gmail rules!"),
    ui.input_slider("n", "N", 0, 100, 40),
    ui.output_text_verbatim("txt"),

    # Handle raw json
    ui.input_text_area("raw_xml", label="Raw JSON", value=GMAIL_XML_RAW, width="100%"),

    # Rules summary
    ui.h3("Rules Summary"),
    ui.output_ui("summary_rules"),
    # Raw rules
    ui.h3("Raw Rules"),
    ui.output_ui("raw_rules"),


)

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------
def parse_gmail_xml(xml_str: str) -> RuleSet:
    dict_data = xmltodict.parse(xml_str)
    return RuleSet(**dict_data)

def summarize_rules_by_label(rule_set: RuleSet):
    print("hello")


# ------------------------------------------------------------------------------
# SERVER
# ------------------------------------------------------------------------------
def server(input, output, session):

    @output()
    @render_text()
    def txt():
        return f"The value of n*2 is {input.n() * 2}"
    

    @output()
    @render_ui()
    def summary_rules():
        rule_set = parse_gmail_xml(input.raw_xml())
        entries = [i for i in rule_set.feed.entry]

        # Loop through each entry and identify the unique labels.
        print(entries[0].dict())
        labels = []
        label_rules = defaultdict(list)
        for entry in entries:
            for app_property in entry.apps_property:
                if app_property.name == "label":
                    labels.append(app_property.value)
        print(labels)

        
        ui_out = []
        for entry in entries:
            rule_id = ui.h5(entry.id)
            ui_out.append(rule_id)
            for app_property in entry.apps_property:
                ui_out.append(ui.p(f"{app_property.name}: {app_property.value}"))
        
        return ui_out
    
    
    @output()
    @render_ui()
    def raw_rules():
        rule_set = parse_gmail_xml(input.raw_xml())
        entries = [i for i in rule_set.feed.entry]
        
        ui_out = []
        for entry in entries:
            rule_id = ui.h5(entry.id)
            ui_out.append(rule_id)
            for app_property in entry.apps_property:
                ui_out.append(ui.p(f"{app_property.name}: {app_property.value}"))
        
        return ui_out


# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server)
