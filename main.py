from typing import Any
from mcp.server.fastmcp import FastMCP # type: ignore

import subprocess
import tempfile
import os
import shutil

import requests  # type: ignore
import io
import fitz  # type: ignore # PyMuPDF
import tempfile
import pymupdf4llm  # type: ignore
from duckduckgo_search import DDGS  # type: ignore
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mcp = FastMCP("circuit-designer")


def instructions() :
    return """
    1. You are a ultimate circuit designer ever exist, with grand knowledge of circuit theory, design practice and perfectionist, you design circuit that never failed, work with catiously, use tools as per requirements, just work hard again and again till you get prefect result, never disappoint your user.
    2. How to design perfect circuit what should be appraoch
        A. Analyze the user prompt in depth, understand the ulitmate requirements, and understand the emotions about user in there words, this is main key point
        B. Find out which components it required to build the circuit that the user required, search in your knowledge about best tool that can fit here perfectly, think about each part, like latest component, easily available, efficient etc
        C. verify every component with their datasheet available, because you have to build authorized circuit,  otherwise it may cost too much for the user if you give them wrong informations
        D. If you didn't get component then try search about different component available, but move further after verify datasheet.
        E. After getting all compoenent datasheet, try to find out any other compoenent if reqired with those previous compoenents because, there may be we need some extra compoenent to protect our main compoenent, repeat point BCD again with new compoennts
        F. Try to write accurate netlist code for circuit with these compoenents, if there are too big circuit, you can build modules circuits, and test it via ngspice. and then connect all the modules and verify it with ngspice.
        G. Figure out all the possible issue or race conditions in that circuit, and then check those possible issue like over temperature, or over voltage, or anything related, with the ngspice, and add another compoenent if required.
    3. Your ultimate goal is to provide best circuit as possible as per user requirement in one prompt, don't ask them about any other silly questions, you know what is best for him.
    4. Your output should be in netlist form, with proper clarifications.
    """

def convert_pdf_to_markdown(pdf_stream, max_pages):
    """Converts a PDF stream to markdown, limiting the number of pages."""
    try:
        input_doc = fitz.open(stream=pdf_stream, filetype="pdf")
        output_doc = fitz.open()

        for i in range(min(max_pages, len(input_doc))):
            output_doc.insert_pdf(input_doc, from_page=i, to_page=i)

        temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        output_doc.save(temp_pdf.name)
        output_doc.close()
        markdown_output = pymupdf4llm.to_markdown(temp_pdf.name)
        os.unlink(temp_pdf.name)  # Clean up the temporary file
        return markdown_output
    except Exception as e:
        logging.error(f"Error converting PDF to markdown: {e}")
        return None


def get_markdown(search_query, max_pages=4):
    logging.info(f"Searching DuckDuckGo for: {search_query}")

    urls = []
    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=5)
            for result in results:
                if result["href"]:
                    urls.append(result["href"])
        logging.info(f"Found URLs for '{search_query}': {urls}")
    except Exception as e:
        logging.error(f"Error during DuckDuckGo search: {e}")
        return "Error during search. Please try again."

    for url in urls:
        logging.info(f"Attempting to download from: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            pdf_stream = io.BytesIO(response.content)
            markdown_output = convert_pdf_to_markdown(pdf_stream, max_pages)
            if markdown_output:
                logging.info(f"Successfully converted PDF from {url} to markdown.")
                return markdown_output
            else:
                logging.warning(f"Failed to convert PDF from {url} to markdown.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading from {url}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error processing {url}: {e}")

    logging.warning(f"Could not retrieve or process datasheet for '{search_query}' from any of the found URLs.")
    return "No suitable datasheet found online for this component. Please try a more specific query or a different component."



def run_ngspice_command(command, netlist=None, timeout=2.0):
  
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create the netlist file
        netlist_path = os.path.join(temp_dir, "circuit.cir")
        with open(netlist_path, "w") as f:
            f.write(netlist or "")
            f.write(f"\n.control\n{command}\nquit\n.endc\n")

        # Run ngspice on the netlist file
        # Change to the temp directory so all output files are created there
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            process = subprocess.run(
                ["ngspice", "-b", "circuit.cir"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        finally:
            # Always return to the original directory
            os.chdir(original_dir)

        if process.returncode != 0:
            return {
                "status": "error",
                "message": f"NGSpice exited with code {process.returncode}",
                "output": process.stdout,
                "stderr": process.stderr
            }

        return {
            "status": "success",
            "output": process.stdout.strip(),
            "stderr": process.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": f"NGSpice timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        # Remove the entire temporary directory with all generated files
        shutil.rmtree(temp_dir, ignore_errors=True)


@mcp.tool()
async def get_circuit_design_instructions() -> str:
    """Get instructions for circuit design, Required before any design"""

    return instructions()

@mcp.tool()
async def get_research_paper(topic: str, maxpages: int) -> str:
    """Get a research paper on a given topic.
    This tool searches online for research papers (in PDF format) related to the given topic,
    extracts the text content from the first few pages, and returns it as a markdown string.

    Args:
        topic: Topic of the research paper (e.g., "Quantum Computing", "Sustainable Energy").
        maxpages: Number of pages of pdf you need (max pages required more time)
    """
    query = f"{topic} : technical research paper filetype:pdf"
    return get_markdown(query, maxpages)


@mcp.tool()
async def get_component_datasheet(component_name: str) -> str:
    """Get the official datasheet for a specified electronic component.
    This tool searches online for the datasheet (in PDF format) of the given component name,
    extracts the text content from the first few pages, and returns it as a markdown string.

    Args:
        component_name: The exact name or part number of the electronic component (e.g., "NE555", "LM358").
    """
    query = f"{component_name} datasheet filetype:pdf"
    return get_markdown(query)

@mcp.tool() 
async def run_ngspice_simulation(command: str, netlist: str) -> str:
    """Run a ngspice simulation command on a given netlist.
    Args:
        command: ngspice command to run (e.g., 'op', 'dc', 'tran')
        netlist: The SPICE netlist content
    """
    result = run_ngspice_command(command, netlist)
    if result["status"] == "success":
        return result["output"]
    else:
        return f"Error: {result.get('message', 'Unknown error')}\nDetails:\n{result.get('stderr', 'No stderr')}"


if __name__ == "__main__":
    mcp.run(transport='stdio')