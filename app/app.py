import dash
from dash import html, dcc, Output, Input, State
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd
import spacy
from PyPDF2 import PdfReader

# Load spaCy pipeline
spacy_load = spacy.load("./pipeline")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Upload(
        id="upload-pdf",
        children=html.Div(["Drag and drop or select a PDF file to upload."]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Button("Parse", id="parse-button"),
    html.Div(id="output-div"),
    html.Button("Download Excel", id="download-excel-button"),
    dcc.Download(id="download-excel"),
    dcc.Store(id="intermediate-data")  # Hidden store for intermediate data
])


# Function for text preprocessing
def preprocessing(sentence):
    stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)
    doc = spacy_load(sentence)
    clean_tokens = []
    
    for token in doc:
        if token.text not in stopwords and token.pos_ != 'PUNCT' and token.pos_ != 'SYM' and \
            token.pos_ != 'SPACE':
                clean_tokens.append(token.lemma_.lower().strip())
                
    return " ".join(clean_tokens)

# Function to extract information from PDF
def get_info(text):
    doc = spacy_load(text)
    skills = []
    education = []
    languages = []
    
    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skills.append(ent.text)
        elif ent.label_ == 'EDUCATION':
            education.append(ent.text)
        elif ent.label_ == 'LANGUAGES':
            languages.append(ent.text)    
 
    skills = list(set(skills))
    education = list(set(education))
    languages = list(set(languages))

    skills = ", ".join(skills)
    education = ", ".join(education)
    languages = ", ".join(languages)

    return [skills], [education], [languages]


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    pdf_reader = PdfReader(io.BytesIO(decoded))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    text = preprocessing(text)
    skills, education, languages = get_info(text)
    return skills, education, languages

@app.callback(
    Output("output-div", "children"),
    Output("intermediate-data", "data"),  # Store the data
    Input("parse-button", "n_clicks"),
    State("upload-pdf", "contents"),
    State("upload-pdf", "filename"),
    prevent_initial_call=True
)
def process_pdf(n_clicks, contents, filename):
    if n_clicks is None:
        raise PreventUpdate

    if contents is not None:
        skills, education, languages = parse_contents(contents, filename)
        df = pd.DataFrame({'Skills': skills, 'Education': education, 'Languages': languages})
        return (
            html.Div([
                html.H4("Extracted Information:"),
                html.P("Skills: {}".format(skills[0])),
                html.P("Education: {}".format(education[0])),
                html.P("Languages: {}".format(languages[0])),
            ]),
            df.to_json(date_format='iso', orient='split')  # Store data as JSON in a hidden div
        )
    else:
        return html.Div(["No file uploaded."]), None

@app.callback(
    Output("download-excel", "data"),
    Input("download-excel-button", "n_clicks"),
    State("intermediate-data", "data"),
    prevent_initial_call=True
)
def download_excel(n_clicks, jsonified_data):
    if n_clicks is None or jsonified_data is None:
        raise PreventUpdate

    df = pd.read_json(jsonified_data, orient='split')
    return dcc.send_data_frame(df.to_excel, "extracted_data.xlsx", index=False)

if __name__ == "__main__":
    app.run_server(debug=True)