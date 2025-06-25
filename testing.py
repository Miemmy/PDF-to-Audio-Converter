import os
pdf_path="C:\\Users\\hp\\Documents\\ALX#DoHardThings\\Copy of Week 3 Milestone Worksheet - Professional Foundations.docx"
bb=os.path.basename(pdf_path)
print(bb)
print(os.path.splitext(pdf_path)[1])
print(bb.split(".")[0])