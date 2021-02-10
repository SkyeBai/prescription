from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import csv

####### CHANGE YOUR CLIENT HERE #######
client = FormRecognizerClient("https://recognizeforms.cognitiveservices.azure.com/", AzureKeyCredential("yourCredential"))

# images to recognise:
docs = ["OriginalScan_.jpg", 'Quality50.jpg', 'Quality25.jpg']
service = 'Azure'
for doc in docs:

    # Assign resolution type
    if doc == "OriginalScan_.jpg":
        resolution = '3'
    elif doc == "Quality50.jpg":
        resolution = '2'
    elif doc == "Quality25.jpg":
        resolution = '1'

    output = []

    def format_bounding_box(bounding_box):
        if not bounding_box:
            return "N/A"
        return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])



    with open(doc, 'rb') as f:
        poller = client.begin_recognize_content(form=f)
    form_pages = poller.result()

    for idx, content in enumerate(form_pages):
        #print("----Recognizing content from page #{}----".format(idx+1))
        #print("Page has width: {} and height: {}, measured with unit: {}".format(
        #    content.width,
        #    content.height,
        #    content.unit
        #))
        for table_idx, table in enumerate(content.tables):
            #print("Table # {} has {} rows and {} columns".format(table_idx, table.row_count, table.column_count))
            #print("Table # {} location on page: {}".format(table_idx, format_bounding_box(table.bounding_box)))
            for cell in table.cells:
                print("...Cell[{}][{}] has text '{}' within bounding box '{}'".format(
                    cell.row_index,
                    cell.column_index,
                    cell.text,
                    format_bounding_box(cell.bounding_box)
                ))

        for line_idx, line in enumerate(content.lines):
            print("Line # {} has word count '{}' and text '{}' within bounding box '{}'".format(
                line_idx,
                len(line.words),
                line.text,
                format_bounding_box(line.bounding_box)
            ))
            for word in line.words:
                print("...Word '{}' has a confidence of {}".format(word.text, word.confidence))
                
                # Store output
                output.append((word.text, word.confidence, 'None', resolution, service))

        """for selection_mark in content.selection_marks:
            print("Selection mark is '{}' within bounding box '{}' and has a confidence of {}".format(
                selection_mark.state,
                format_bounding_box(selection_mark.bounding_box),
                selection_mark.confidence
            ))"""
        print("----------------------------------------")

        with open("recorded_performance_azure2.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(output)
