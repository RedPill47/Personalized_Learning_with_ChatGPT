from langchain.tools import tool
import os
import subprocess

@tool("Store Output")
def store_output(content: str, file_path: str) -> str:
    """Store the provided content into a file specified by file_path."""
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    full_path = os.path.join(output_dir, file_path)
    
    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return f"Output successfully written to {full_path}"
    except Exception as e:
        return f"Failed to write output to {full_path}: {e}"

@tool("LaTeX Compiler")
def compile_latex(file_path: str, output_file: str) -> str:
    """Compiles LaTeX content from a specified file and saves the resulting PDF to the specified output file."""
    try:
        # Construct the full path to the file in the output_files directory
        full_file_path = os.path.join('output_files', file_path)
        with open(full_file_path, "r") as tex_file:
            full_latex_content = tex_file.read()

        tex_filename = "compiled_materials.tex"
        pdf_filename = os.path.join('output_files', output_file)
        log_filename = os.path.join('output_files', "compiled_materials.log")


        with open(tex_filename, "w") as tex_file:
            tex_file.write(full_latex_content)
        
        try:
            # Compile the LaTeX file and redirect output to log file
            subprocess.run(
                ["pdflatex", "-output-directory=output_files", tex_filename],
                check=True,
                capture_output=True,
                text=True
            )
            # Ensure the PDF was created
            if not os.path.exists(pdf_filename):
                raise Exception("PDF compilation failed.")
            return f"PDF successfully compiled and saved to {pdf_filename}"
        except subprocess.CalledProcessError as e:
            # Capture the LaTeX error log
            with open(log_filename, "r") as log_file:
                log_content = log_file.read()
            return f"An error occurred during LaTeX compilation: {e}\nLog Output:\n{log_content}"
        finally:
            # Clean up intermediate files
            for file in [tex_filename, log_filename, os.path.join('output_files', "compiled_materials.aux"), 
                         os.path.join('output_files', "compiled_materials.toc"), 
                         os.path.join('output_files', "compiled_materials.out"), 
                         os.path.join('output_files', "compiled_materials.tex")]:
                if os.path.exists(file):
                    os.remove(file)
    except Exception as e:
        return f"Failed to read LaTeX file: {e}"
