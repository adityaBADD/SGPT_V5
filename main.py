from fastapi import FastAPI, Query, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

# Embedded data structured for FastAPI-friendly queries
directory = {
    "by_name": {
        "Guy Matthews": {
            "title": "Managing Partner, CEO",
            "reports_to": None,
            "subordinates": ["T. Temple", "R. Jocelyn", "E. Lanfear", "S. Ford", "J. Dave", "B. Langheim", "D. Berney"]
        },
        "T. Temple": {
            "title": "COO",
            "reports_to": "Guy Matthews",
            "subordinates": ["J. Paget", "V. Chandna"]
        },
        "J. Paget": {
            "title": "Head of Operations",
            "reports_to": "T. Temple",
            "subordinates": ["J. Cummins", "L. Presnell", "M. Bhandal", "P. Sarbutt"]
        },
        "J. Cummins": {
            "title": "Manager, Settlements",
            "reports_to": "J. Paget",
            "subordinates": []
        },
        "L. Presnell": {
            "title": "Supervisor, Corporate Actions & Governance",
            "reports_to": "J. Paget",
            "subordinates": []
        },
        "M. Bhandal": {
            "title": "Manager, Reconciliations",
            "reports_to": "J. Paget",
            "subordinates": []
        },
        "P. Sarbutt": {
            "title": "Manager, Fund Operations & Reconciliations",
            "reports_to": "J. Paget",
            "subordinates": []
        },
        "V. Chandna": {
            "title": "Head of Business Solutions",
            "reports_to": "T. Temple",
            "subordinates": ["G. Bains"]
        },
        "G. Bains": {
            "title": "Manager, Business Support",
            "reports_to": "V. Chandna",
            "subordinates": []
        },
        "R. Jocelyn": {
            "title": "Head of Compliance",
            "reports_to": "Guy Matthews",
            "subordinates": ["K. Malec", "J. Grech"]
        },
        "K. Malec": {
            "title": "Deputy MLRO",
            "reports_to": "R. Jocelyn",
            "subordinates": []
        },
        "J. Grech": {
            "title": "Manager, General Compliance",
            "reports_to": "R. Jocelyn",
            "subordinates": []
        },
        "E. Lanfear": {
            "title": "General Counsel",
            "reports_to": "Guy Matthews",
            "subordinates": []
        },
        "S. Ford": {
            "title": "Head of Finance",
            "reports_to": "Guy Matthews",
            "subordinates": []
        },
        "J. Dave": {
            "title": "Head of Human Resources",
            "reports_to": "Guy Matthews",
            "subordinates": []
        },
        "B. Langheim": {
            "title": "Head of Financial Planning, Analysis & Change",
            "reports_to": "Guy Matthews",
            "subordinates": []
        },
        "D. Berney": {
            "title": "Internal Audit",
            "reports_to": "Guy Matthews",
            "subordinates": []
        }
    },
    "by_title": {
        "Managing Partner, CEO": ["Guy Matthews"],
        "COO": ["T. Temple"],
        "Head of Operations": ["J. Paget"],
        "Manager, Settlements": ["J. Cummins"],
        "Supervisor, Corporate Actions & Governance": ["L. Presnell"],
        "Manager, Reconciliations": ["M. Bhandal"],
        "Manager, Fund Operations & Reconciliations": ["P. Sarbutt"],
        "Head of Business Solutions": ["V. Chandna"],
        "Manager, Business Support": ["G. Bains"],
        "Head of Compliance": ["R. Jocelyn"],
        "Deputy MLRO": ["K. Malec"],
        "Manager, General Compliance": ["J. Grech"],
        "General Counsel": ["E. Lanfear"],
        "Head of Finance": ["S. Ford"],
        "Head of Human Resources": ["J. Dave"],
        "Head of Financial Planning, Analysis & Change": ["B. Langheim"],
        "Internal Audit": ["D. Berney"]
    },
    "by_pdf_name":{
        "Sarasin Food & Agriculture Opportunities - A Acc":["GB00B2Q8L643.pdf"],
        "Sarasin Global Dividend - A Acc":["GB00BGDF8769.pdf"],
        "Sarasin Global Equity Real Return - A Acc":["GB00B13GW945.pdf"]
    }
}


app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/getProfile_name')
async def get_profile_by_name(name: str = Query(None)):
    # Check if the name exists in the directory
    profile = directory["by_name"].get(name)
    if profile:
        return profile
    else:
        return {"message": "No profile found for this name"}

@app.get('/getProfile_title')
async def get_profile_by_title(title: str = Query(None)):
    # Check if the title exists in the directory
    names = directory["by_title"].get(title)
    if names:
        # Return all profiles matching the title
        return {name: directory["by_name"][name] for name in names}
    else:
        return {"message": "No profiles found with this title"}

@app.get("/download-pdf/{pdf_name}")
async def download_pdf(pdf_name: str):
    file_path = f"static/pdfs/{pdf_name}"
    try:
        return FileResponse(path=file_path, filename=pdf_name, media_type='application/pdf')
    except FileNotFoundError:
        raise {"message": "No Files found"}

@app.get('/getPDF_by_name')
async def get_pdf_by_name(name: str = Query(None)):
    # Check if the PDF name exists in the directory
    name_pdf_list = directory["by_pdf_name"].get(name)

    if not name_pdf_list:
        raise {"message":"No PDF file found for this name"}

    # Assuming you want to serve the first PDF if there are multiple
    name_pdf = name_pdf_list[0]
    file_path = f"static/pdfs/{name_pdf}"

    try:
        return FileResponse(path=file_path, filename=name_pdf, media_type='application/pdf')
    except FileNotFoundError:
        raise {"message":"File Not Found"}
