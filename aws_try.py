import json
import boto3
import csv

bucket = "bucket4genv"
docs = ["OriginalScan_.jpg", 'Quality50.jpg', 'Quality25.jpg']
service = 'AWSTextract'

for doc in docs:

    # upload file to resources
    s3 = boto3.resource('s3')
    data = open(doc, 'rb')
    s3.Bucket(bucket).put_object(Key=doc, Body=data)

    # Textract client
    textract = boto3.client('textract')

    # call for OCR
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': doc
            }
        }
    )
    
    # Assign resolution type
    if doc == "OriginalScan_.jpg":
        resolution = '3'
    elif doc == "Quality50.jpg":
        resolution = '2'
    elif doc == "Quality25.jpg":
        resolution = '1'

    # Detect columns and print lines
    columns = []
    lines = []

    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            column_found = False
            for index, column in enumerate(columns):
                bbox_left = item["Geometry"]["BoundingBox"]["Left"]
                bbox_right = item["Geometry"]["BoundingBox"]["Left"] + \
                    item["Geometry"]["BoundingBox"]["Width"]
                bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + \
                    item["Geometry"]["BoundingBox"]["Width"] / 2
                column_centre = column['left'] + column['right'] / 2

                if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                    # Bbox appears inside the column
                    lines.append((item["Text"], item['Confidence'], item['TextType'], resolution, service))
                    column_found = True
                    break
            if not column_found:
                columns.append({'left': item["Geometry"]["BoundingBox"]["Left"], 'right': item["Geometry"]
                                ["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
                lines.append((item["Text"], item['Confidence'], item['TextType'], resolution, service))

    #lines.sort(key=lambda x: x[0])
    print(lines)

    print('========')

    with open("recorded_performance_aws2.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines)