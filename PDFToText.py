######################################################################
# @ 임포트.
######################################################################
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter # pip install pdfminer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys
import io
import os


######################################################################
# @ PDF로부터 텍스트 추출.
######################################################################
def ExtractTextFromPDF(path) -> bool:
	if not os.path.isfile(path):
		return ""

	rsrcmgr = PDFResourceManager()
	retstr = io.StringIO()
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, laparams=laparams)

	file = open(path, "rb")
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	pagenos = set()

	for page in PDFPage.get_pages(
		file,
		pagenos,
		maxpages=0,
		password="",
		caching=True,
		check_extractable=True):
		interpreter.process_page(page)

	text = retstr.getvalue()
	file.close()
	device.close()
	retstr.close()
	return text


######################################################################
# @ 진입점.
######################################################################
def OnMain(arguments : list):

	pdfFileFullName = arguments[1]
	pdfText = ExtractTextFromPDF(pdfFileFullName)

	# 전체경로가 포함된 파일이름과 확장자 구분.
	pdfFileFullNameAndExtension = os.path.splitext(pdfFileFullName)
	textFileFullName = f"{pdfFileFullNameAndExtension[0]}.txt"
	
	# PDF파일에서 추출된 텍스트를 저장.
	with open(textFileFullName, "w") as file
		file.write(pdfText)
		file.close()

	exit(0)


######################################################################
# @ 진입점.
######################################################################
if __name__ == "__main__":
	OnMain(sys.argv)