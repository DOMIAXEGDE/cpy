import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def create_pdf(data, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_styles = {
        "title": ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=12
        ),
        "body": ParagraphStyle(
            'BodyText',
            parent=styles['BodyText'],
            fontSize=12,
            spaceAfter=12,
            leading=15
        ),
        "subtitle": ParagraphStyle(
            'Subtitle',
            parent=styles['Title'],
            fontSize=18,
            spaceAfter=6
        )
    }

    story = []

    for structure_id, details in data.items():
        story.append(Paragraph(structure_id, custom_styles['title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Timestamp: {details['timestamp']}", custom_styles['subtitle']))
        story.append(Spacer(1, 12))
        
        properties = details["properties"]
        for key, value in properties.items():
            # Handle multi-line property values by replacing newlines with <br/> tags
            if isinstance(value, str):
                value = value.replace('\n', '<br/>')
            story.append(Paragraph(f"{key}: {value}", custom_styles['body']))
            story.append(Spacer(1, 12))

        story.append(PageBreak())

    doc.build(story)

if __name__ == "__main__":
    input_filename = input("Enter input filename.json (With extension): ")
    json_data = read_json_file(input_filename)
    
    # Print JSON data to verify structure
    print(json.dumps(json_data, indent=4))
    
    create_pdf(json_data, 'output.pdf')
