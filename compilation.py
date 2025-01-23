import os

def read_file_contents(filename):
    """Read and return contents of a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"File {filename} not found"

def get_style_for_type(file_type):
    """Return appropriate environment name based on file type."""
    if file_type == 'r':
        return 'definition'
    elif file_type == 'g':
        return 'statement'
    elif file_type == 'b':
        return 'problem'
    elif file_type == 'y':
        return 'solution'
    return 'plain'

def create_mathematics_tex(order_file, output_tex):
    """Create LaTeX document based on order file."""
    # Read order sequence
    with open(order_file, 'r') as f:
        sequence = [x.strip() for x in f.read().split(',')]
    
    # LaTeX document header
    latex_content = [
        r'\documentclass[12pt]{article}',
        r'\usepackage[utf8]{inputenc}',
        r'\usepackage[margin=1in]{geometry}',
        r'\usepackage{amsthm}',
        r'\usepackage{mdframed}',
        r'\usepackage{parskip}',
        '',
        # Define custom environments
        r'\newmdtheoremenv{definition}{Definition}',
        r'\newmdtheoremenv{statement}{Statement}',
        r'\newmdtheoremenv{problem}{Problem}',
        r'\newmdtheoremenv{solution}{Solution}',
        '',
        # Customize spacing
        r'\setlength{\parindent}{0pt}',
        r'\setlength{\parskip}{1em}',
        '',
        r'\begin{document}',
        ''
    ]

    # Process each file in sequence
    for item in sequence:
        file_type = item[0]  # 'r', 'g', 'b', or 'y'
        filename = f"{item}.txt"
        
        # Read content
        content = read_file_contents(filename)
        env_name = get_style_for_type(file_type)
        
        # Create framed environment with content
        latex_content.extend([
            r'\begin{' + env_name + '}',
            content.replace('_', r'\_').replace('%', r'\%').replace('#', r'\#').replace('&', r'\&'),
            r'\end{' + env_name + '}',
            ''
        ])

    # Close document
    latex_content.append(r'\end{document}')
    
    # Write LaTeX file
    with open(output_tex, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))

def compile_latex(tex_file):
    """Compile LaTeX document to PDF."""
    os.system(f'pdflatex {tex_file}')
    
    # Clean up auxiliary files
    base_name = tex_file[:-4]
    for ext in ['.aux', '.log']:
        if os.path.exists(base_name + ext):
            os.remove(base_name + ext)

def main():
    tex_file = 'mathematics_1.tex'
    create_mathematics_tex('order.txt', tex_file)
    compile_latex(tex_file)

if __name__ == "__main__":
    main()