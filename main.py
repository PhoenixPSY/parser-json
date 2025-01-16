import os
import json
from typing import Dict, List, Tuple
import re
import pdfplumber
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentParser:
    def __init__(self):
        # For now just handling PDF and HTML - might add more formats later if needed
        self.supported_formats = ['.pdf', '.html']

    def parse_document(self, file_path: str) -> str:
        """
        Figures out what kind of document we're dealing with and extracts the text.
        I'm keeping it simple for now - just checking the file extension.

        Args:
            file_path: Where to find the document

        Returns:
            The text content pulled from the document
        """
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.pdf':
            return self._parse_pdf(file_path)
        elif ext.lower() == '.html':
            return self._parse_html(file_path)
        return ""  # Nothing we can do with unsupported files

    def _parse_pdf(self, file_path: str) -> str:
        """
        Gets text out of PDFs using pdfplumber. Been pretty reliable so far.
        
        Args:
            file_path: PDF file location
        
        Returns:
            All the text we managed to extract
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages).strip()
        except Exception as e:
            print(f"Ugh, PDF parsing failed for {file_path}: {str(e)}")
            return ""

    def _parse_html(self, file_path: str) -> str:
        """
        Pulls text from HTML files. BeautifulSoup makes this pretty straightforward.
        Strips out scripts and styling - we just want the content.
        
        Args:
            file_path: HTML file location
        
        Returns:
            The cleaned up text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                # Get rid of the stuff we don't want
                for script in soup(["script", "style"]):
                    script.decompose()
                return soup.get_text(separator='\n').strip()
        except Exception as e:
            print(f"HTML parsing broke for {file_path}: {str(e)}")
            return ""

class InformationExtractor:
    def extract_information(self, text: str) -> Dict[str, str]:
        """
        Tries to make sense of the text by finding patterns like "key: value".
        Not perfect but works well enough for our needs.
        
        Args:
            text: The raw text to process
        
        Returns:
            Dictionary of the stuff we found
        """
        results = {}

        # Look for obvious key-value pairs first
        lines = text.splitlines()
        for line in lines:
            # This regex catches most key-value formats I've seen
            match = re.search(r'(.+?):\s*(.*)', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                results[key] = value

        # Backup plan: save any non-empty lines we haven't caught yet
        for line in lines:
            if line and line not in results:
                results[line] = ""

        return results

    def save_to_json(self, data: List[Dict[str, str]], output_file: str):
        """
        Dumps everything we found into a JSON file.
        Makes it easy to check what we extracted.
        
        Args:
            data: All the info we extracted
            output_file: Where to save it
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

class RAGModel:
    def __init__(self):
        # Using this model because it's fast and works well enough
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.document_embeddings = {}
        self.documents = {}

    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Processes documents and gets them ready for searching.
        Combines all the key-value pairs into one string per document.
        
        Args:
            documents: List of extracted document content
        """
        for index, content in enumerate(documents):
            # Smush all the content together for embedding
            text = ' '.join(f"{k}: {v}" for k, v in content.items() if v)
            embedding = self.model.encode([text])[0]
            self.document_embeddings[index] = embedding
            self.documents[index] = content

    def query(self, question: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        Finds the documents most relevant to the question.
        Uses cosine similarity - simple but effective.
        
        Args:
            question: What we're looking for
            top_k: How many results to return (default 3 seems to work well)
        
        Returns:
            The most relevant documents we found
        """
        question_embedding = self.model.encode([question])[0]

        similarities = {}
        for index, doc_embedding in self.document_embeddings.items():
            similarity = cosine_similarity(
                [question_embedding], 
                [doc_embedding]
            )[0][0]
            similarities[index] = similarity

        sorted_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        results = []
        for index, _ in sorted_docs[:top_k]:
            results.append(self.documents[index])

        return results

def main():
    """
    Puts everything together. Pretty straightforward process:
    1. Parse the documents
    2. Extract the information
    3. Save it
    4. Set up the RAG model
    """
    document_parser = DocumentParser()
    information_extractor = InformationExtractor()
    rag_model = RAGModel()

    # All the documents we need to process
    document_paths = [
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid2\\Contract_Affidavit.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid2\\Dell Laptops w_Extended Warranty - Bid Information - {3} _ BidNet Direct.html",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid2\\Dell_Laptop_Specs.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid2\\Mercury_Affidavit.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid2\\PORFP_-_Dell_Laptop_Final.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid1\\Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid1\\Addendum 2 RFP JA-207652 Student and Staff Computing Devices.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid1\\JA-207652 Student and Staff Computing Devices FINAL.pdf",
        "C:\\Users\\npran\\OneDrive\\Desktop\\PARSER JSON\\Documents\\Bid1\\Student and Staff Computing Devices __SOURCING #168884__ - Bid Information - {3} _ BidNet Direct.html"
    ]

    try:
        print("Starting to parse the documents...")
        parsed_docs = [document_parser.parse_document(path) for path in document_paths]
        
        print("Extracting all the useful bits...")
        extracted_info = [information_extractor.extract_information(content) for content in parsed_docs]

        print("Saving everything to extracted_information.json")
        information_extractor.save_to_json(extracted_info, "extracted_information.json")

        print("Loading everything into the RAG model...")
        rag_model.add_documents(extracted_info)

    except Exception as e:
        print(f"Something went wrong: {str(e)}")

if __name__ == "__main__":
    main()