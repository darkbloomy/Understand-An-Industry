#!/usr/bin/env python3
"""
Extract CV information from PDF and generate LinkedIn-style HTML profile
"""

import sys
from pathlib import Path

# Try different PDF libraries
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using available library"""
    text = ""
    
    if HAS_PDFPLUMBER:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif HAS_PYPDF:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        raise ImportError("No PDF library available. Install pdfplumber or pypdf")
    
    return text


def parse_cv_content(text):
    """Parse CV text and extract key sections"""
    lines = text.split('\n')
    
    data = {
        'name': '',
        'title': '',
        'contact': {},
        'summary': '',
        'experience': [],
        'education': [],
        'skills': [],
        'languages': []
    }
    
    # Extract name (usually first non-empty line)
    for line in lines:
        if line.strip() and len(line.strip()) < 100:
            data['name'] = line.strip()
            break
    
    # Extract content based on keywords
    current_section = None
    current_item = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Section detection
        if any(keyword in line.upper() for keyword in ['EXPERIENCE', 'EMPLOYMENT', 'WORK']):
            current_section = 'experience'
            continue
        elif any(keyword in line.upper() for keyword in ['EDUCATION', 'DEGREE']):
            current_section = 'education'
            continue
        elif any(keyword in line.upper() for keyword in ['SKILL', 'COMPETENCE']):
            current_section = 'skills'
            continue
        elif any(keyword in line.upper() for keyword in ['LANGUAGE', 'LINGUISTIC']):
            current_section = 'languages'
            continue
        elif any(keyword in line.upper() for keyword in ['SUMMARY', 'PROFILE', 'ABOUT']):
            current_section = 'summary'
            continue
        
        # Extract content by section
        if current_section == 'summary':
            data['summary'] += line + ' '
        elif current_section == 'skills':
            if line and not line.startswith('•'):
                data['skills'].append(line)
        elif current_section == 'languages':
            if line:
                data['languages'].append(line)
        elif current_section == 'experience':
            data['experience'].append(line)
        elif current_section == 'education':
            data['education'].append(line)
    
    # Clean up contact info from text
    for line in lines:
        if '@' in line or '+' in line or 'linkedin' in line.lower():
            data['contact']['email'] = line if '@' in line else data['contact'].get('email', '')
            data['contact']['phone'] = line if '+' in line or '(' in line else data['contact'].get('phone', '')
    
    return data


def generate_linkedin_html(cv_data):
    """Generate LinkedIn-style HTML profile"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cv_data['name']} - Professional Profile</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f3f2ef;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0077b5 0%, #004182 100%);
            color: white;
            padding: 60px 40px 40px;
            text-align: center;
        }}
        
        .profile-image {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            border: 4px solid white;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 5px;
            font-weight: 700;
        }}
        
        .header .title {{
            font-size: 18px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 15px;
        }}
        
        .contact-info {{
            font-size: 14px;
            opacity: 0.9;
            margin-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.2);
            padding-top: 15px;
        }}
        
        .contact-info a {{
            color: white;
            text-decoration: none;
            margin: 0 15px;
        }}
        
        .contact-info a:hover {{
            text-decoration: underline;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            color: #0077b5;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e8e7e3;
        }}
        
        .summary {{
            background: #f3f2ef;
            padding: 20px;
            border-radius: 4px;
            font-size: 15px;
            line-height: 1.7;
        }}
        
        .experience-item, .education-item {{
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 1px solid #e8e7e3;
        }}
        
        .experience-item:last-child, .education-item:last-child {{
            border-bottom: none;
        }}
        
        .position-title {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .company {{
            font-size: 14px;
            color: #0077b5;
            font-weight: 500;
            margin-bottom: 3px;
        }}
        
        .duration {{
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .description {{
            font-size: 14px;
            color: #555;
            line-height: 1.6;
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .skill-tag {{
            background: #e8e7e3;
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 14px;
            text-align: center;
            border: 1px solid #d0ccc8;
        }}
        
        .languages-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .language-item {{
            background: #f3f2ef;
            padding: 12px 15px;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        .footer {{
            background: #f3f2ef;
            padding: 20px 40px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #e8e7e3;
        }}
        
        @media (max-width: 600px) {{
            .header {{
                padding: 40px 20px 30px;
            }}
            
            .header h1 {{
                font-size: 24px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .skills-grid, .languages-list {{
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="profile-image">👤</div>
            <h1>{cv_data['name']}</h1>
            <div class="title">{cv_data['title'] or 'Professional'}</div>
            <div class="contact-info">
                {f'<a href="mailto:{cv_data["contact"].get("email", "")}">📧 Email</a>' if cv_data['contact'].get('email') else ''}
                {f'<a href="tel:{cv_data["contact"].get("phone", "")}">📞 Phone</a>' if cv_data['contact'].get('phone') else ''}
            </div>
        </div>
        
        <div class="content">
"""
    
    # Summary section
    if cv_data['summary'].strip():
        html += f"""
            <div class="section">
                <h2 class="section-title">About</h2>
                <div class="summary">{cv_data['summary'].strip()}</div>
            </div>
"""
    
    # Experience section
    if cv_data['experience']:
        html += """
            <div class="section">
                <h2 class="section-title">Experience</h2>
"""
        for exp in cv_data['experience'][:10]:  # Limit to 10 items
            if exp.strip():
                html += f"""
                <div class="experience-item">
                    <div class="position-title">{exp[:50]}...</div>
                    <div class="description">{exp}</div>
                </div>
"""
        html += "            </div>\n"
    
    # Education section
    if cv_data['education']:
        html += """
            <div class="section">
                <h2 class="section-title">Education</h2>
"""
        for edu in cv_data['education'][:5]:  # Limit to 5 items
            if edu.strip():
                html += f"""
                <div class="education-item">
                    <div class="position-title">{edu}</div>
                </div>
"""
        html += "            </div>\n"
    
    # Skills section
    if cv_data['skills']:
        html += """
            <div class="section">
                <h2 class="section-title">Skills</h2>
                <div class="skills-grid">
"""
        for skill in cv_data['skills'][:15]:  # Limit to 15 skills
            if skill.strip():
                html += f'                    <div class="skill-tag">{skill[:30]}</div>\n'
        html += "                </div>\n            </div>\n"
    
    # Languages section
    if cv_data['languages']:
        html += """
            <div class="section">
                <h2 class="section-title">Languages</h2>
                <div class="languages-list">
"""
        for lang in cv_data['languages'][:8]:  # Limit to 8 languages
            if lang.strip():
                html += f'                    <div class="language-item">{lang}</div>\n'
        html += "                </div>\n            </div>\n"
    
    html += """
        </div>
        
        <div class="footer">
            <p>Generated Professional Profile | LinkedIn Style</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    pdf_path = Path(__file__).parent / '.github' / 'assets' / 'Yameng_CV_202306.pdf'
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)
    
    print(f"Extracting content from: {pdf_path}")
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        print(f"Successfully extracted {len(text)} characters from PDF")
        
        # Parse CV content
        cv_data = parse_cv_content(text)
        print(f"Parsed CV data: name={cv_data['name']}")
        
        # Generate HTML
        html_content = generate_linkedin_html(cv_data)
        
        # Save HTML file
        output_path = Path(__file__).parent / 'Yameng_CV_Profile.html'
        output_path.write_text(html_content, encoding='utf-8')
        
        print(f"\n✅ Successfully generated: {output_path}")
        print(f"   File size: {len(html_content)} bytes")
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install required dependencies:")
        print("  pip install pdfplumber pypdf")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
