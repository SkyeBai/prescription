This folder contains files necessary for comparing AWS Textract and Azure under different 
resolution of prescriptions. The result shows that AWS Textract is better under all situations.

File Explaination:
alterResolution.ipynb: Alters the resolution of images, scale from 1 to 100.
aws_try.py: Uses AWS Textract to extract information from the prescritions.
azure_try.py: Uses Azure to extract information from the prescritions.
AWSvsAzure.ipynb: Data analysis after getting the csv results from the above two .py files.
Note: The two .py files format the information extracted as a csv file for data analysis convenience.
OriginalScan, Quality25, Quality50 are the three levels of resolutions.
recorded_performance_aws2.csv and recorded_performance_azure2.csv are the extracted results.
PPTWK2: Presentation.

