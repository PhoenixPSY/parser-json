# My Document Parser & Information Extraction Tool

Hey there! 👋 I've built this Python tool to help make sense of PDF and HTML documents. It basically reads through them, pulls out the important bits, and lets you search through everything using natural language queries. I'm using something called RAG (Retrieval-Augmented Generation) to make the searching work better.

**Quick note**: I got the best extraction results starting from line 415 in the JSON output file. After a bunch of trial and error with documents from both BID1 and BID2 folders, I think I've finally got the parsing working pretty well!

## What This Thing Can Do

- Grabs text from PDFs and HTML files without breaking a sweat
- Finds and pulls out the important stuff using some regex magic
- Uses some fancy embedding tech to let you search through everything naturally
- Saves everything in a nice, clean JSON file that's easy to work with

## Before You Start

You'll need:
- Python 3.6 or newer (I built it with Python 3.6 but newer versions should work fine)
- pip (to install all the packages we need)

## Setting Everything Up

1. **Getting Started**:
   - Make a new folder wherever you want to keep this project
   - Create a file called `main.py` and paste in the code I shared

2. **Installing the Good Stuff**: 
   Pop open your terminal, head to your project folder, and run this:
   ```
   pip install beautifulsoup4 pdfplumber sentence-transformers scikit-learn
   ```

3. **Getting Your Documents Ready**:
   Just make sure you've got your PDFs and HTML files somewhere accessible on your computer.

4. **Pointing to Your Files**:
   Open up `main.py` and look for the `document_paths` list. You'll need to update it with wherever your files are living.

   Here's where I keep mine (feel free to copy this structure or do your own thing):
   ```python
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
   ```

5. **Setting Up Where to Save Stuff**:
   The tool will save everything it finds in a JSON file. You can change where it saves by tweaking this line:
   ```python
   information_extractor.save_to_json(extracted_info, "your_output_file.json")
   ```

6. **Fire It Up!**:
   Just run:
   ```
   python main.py
   ```

## What's Going On Under the Hood

I've split everything into three main parts:
- `DocumentParser`: The workhorse that reads your files
- `InformationExtractor`: The smart bit that figures out what's important
- `RAGModel`: The fancy part that lets you search through everything
- And a main function that ties it all together

## If Something Goes Wrong

Don't worry! I've added error handling throughout the code, so if something breaks, you'll get a helpful message telling you what went wrong. Usually it's something simple like a file being in the wrong place or missing permissions.

---

Hope this helps get you started! Let me know if anything's unclear or if you run into any issues. I'm always tweaking and improving things, so feedback is super welcome! 🚀
