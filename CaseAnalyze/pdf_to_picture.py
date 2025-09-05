import datetime
import os
import fitz  # fitz就是pip install PyMuPDF

def pdf2png(pdfPath, baseImagePath):
    imagePath=os.path.join(baseImagePath,os.path.basename(pdfPath).split('.')[0])
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    print("imagePath=" + imagePath)
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    pdfDoc = fitz.open(pdfPath)
    #totalPage=pdfDoc.pageCount
    totalPage=pdfDoc.page_count
    for pg in range(totalPage):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        print(f'正在保存{pdfPath}的第{pg+1}页，共{totalPage}页')
        pix.save(imagePath + '/' + f'images_{pg+1}.png')
    endTime_pdf2img = datetime.datetime.now()
    print(f'{pdfDoc}-pdf2img-花费时间={(endTime_pdf2img - startTime_pdf2img).seconds}秒')

if __name__ == "__main__":
    pdfPath = r'./小牛模拟案卷.pdf'
    baseImagePath = './imgs'
    pdf2png(pdfPath, baseImagePath)
