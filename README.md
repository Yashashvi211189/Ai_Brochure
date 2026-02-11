# AI-Powered Brochure Generator

A web application that creates professional marketing brochures from **HTML files, images, or text ideas**. Generate tailored brochures for customers, investors, and partners with beautiful gradient backgrounds.

The focus is on:
- Clean, readable Python
- Simple, linear architecture
- Modern web interface with tabs
- Multiple input types (HTML, Image, Text)
- Automatic background image generation
- Local processing (no external API calls needed)

## How it works

### Input Processing

1. **HTML Files** (`scraper.py`)
   - Loads a local HTML file from disk
   - Parses it with BeautifulSoup
   - Strips noise (scripts, styles, navbars, footers, cookie banners)
   - Extracts content blocks (headings and paragraphs)

2. **Images** (`image_analyzer.py`)
   - Analyzes uploaded images
   - Extracts metadata and visual characteristics
   - Infers business information from image properties

3. **Text/Ideas** (`text_analyzer.py`)
   - Parses raw text input
   - Intelligently identifies headings and paragraphs
   - Structures the content for processing

### Analysis & Generation

4. **Business Analysis** (`analyzer.py`)
   - Processes content blocks into a structured business profile
   - Identifies: positioning, offerings, audience, value props, brand tone
   - Uses offline heuristics (stubbed for demo)

5. **Brochure Generation** (`generator.py`)
   - Creates three tailored brochures (customers, investors, partners)
   - Formats content for each audience type

6. **Background Images** (`image_generator.py`)
   - Generates beautiful gradient backgrounds for each brochure
   - Uses color schemes based on audience type

### Web Interface

7. **Flask App** (`app.py`)
   - Provides web interface with tabs for different input types
   - Handles file uploads and form submissions
   - Returns JSON with generated brochures and images

## Requirements

- Python 3.9+
- An OpenAI-compatible API key available as `OPENAI_API_KEY` in your environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your API key (example for PowerShell on Windows):

```powershell
$env:OPENAI_API_KEY="sk-..."   # replace with your key
```

## Running the Application

### Option 1: Web Interface (Recommended)

Start the Flask web server:

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

You'll see a beautiful web interface where you can:
- Upload an HTML file
- Generate brochures with one click
- View all three brochures with generated background images
- See results instantly in your browser

### Option 2: Command Line Interface

Basic usage (defaults to `data/company.html`):

```bash
python main.py
```

Specify a custom input HTML and output directory:

```bash
python main.py --html .\data\my_company.html --output .\output
```

After running, check the `output` directory for:

- `brochure_customers.md`
- `brochure_investors.md`
- `brochure_partners.md`

Each file contains a marketing-ready brochure tailored to that audience.

## Features

- **Web Interface**: Modern, responsive UI with tabbed input options
- **Multiple Input Types**:
  - 📄 **HTML Files**: Upload company website HTML
  - 🖼️ **Images**: Upload logos, screenshots, or any business image
  - 💡 **Text/Ideas**: Type your company description or idea
- **Image Generation**: Automatically generates beautiful gradient backgrounds for each brochure
- **Three Audience Types**: Customers, Investors, and Partners
- **Local Processing**: Everything runs locally, no external API calls needed (stubbed version)
- **Clean Architecture**: Modular Python code that's easy to understand and extend

## Deployment

This app can be deployed online for free using Render.com, Railway, or PythonAnywhere.

**Quick Deploy to Render.com:**
1. Push code to GitHub (already done ✅)
2. Go to https://render.com
3. Connect your GitHub repo
4. Create new Web Service
5. Use build command: `pip install -r requirements.txt`
6. Use start command: `gunicorn app:app`
7. Deploy!

See `DEPLOYMENT.md` for detailed instructions.

**Live Demo URL:** (After deployment)
```
https://your-app-name.onrender.com
```

## Notes

- Input source is strictly **local HTML**. There is no URL fetching.
- The current version uses offline/stubbed LLM calls for demo purposes.
- Comments are deliberately short and practical, aimed at another engineer reading this codebase.