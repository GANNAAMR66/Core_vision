# main.py - OMR Main Script (Fast & Stable)
import cv2
import numpy as np
import utlis
import os

# ================= SETTINGS =================
heightImg, widthImg = 700, 700
questions, choices = 5, 5
ans = [1, 2, 0, 2, 4]
pathImage = r"C:\Users\DAR_MR\Desktop\Core Vision\Optical-Mark-Recognition-OPENCV-master\asset\2choices_no_answers.jpg"

# 🛠️ تخطي القائمة تلقائياً (غيّر لـ True/False لتفادي شاشة الاختيار)
FORCE_MODE = None  

# ================= MODE SELECTION =================
def selectMode():
    if FORCE_MODE is not None:
        return FORCE_MODE

    print("\n🖱️  CLICK on the window, then press [1] / [2] / [Q]")
    screen = np.ones((180, 500, 3), dtype=np.uint8) * 240
    cv2.putText(screen, "OMR MODE SELECTION", (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    cv2.putText(screen, "[1] Camera  [2] Image  [Q] Quit", (40, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,100,255), 2)
    cv2.putText(screen, ">>> Click window & press key <<<", (80, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,100,100), 1)

    cv2.namedWindow("OMR MODE", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("OMR MODE", screen)
    cv2.moveWindow("OMR MODE", 500, 300)
    cv2.waitKey(1)  # تأكيد رسم النافذة قبل الاستماع للكيبورد

    key = cv2.waitKey(0) & 0xFF  # يستنى ضغطتك مهما طال الوقت
    cv2.destroyWindow("OMR MODE")

    if key in [ord('1'), ord('c')]:
        print("✅ Camera Mode Selected")
        return True
    elif key in [ord('2'), ord('i')]:
        print("✅ Image Mode Selected")
        return False
    else:
        print("👋 Quitting...")
        return None

# ================= PROCESS ONE FRAME =================
def processOMR(img, imgBlank):
    try:
        img = cv2.resize(img, (widthImg, heightImg))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 70)
        
        contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rectCon = utlis.rectContour(contours)
        
        if len(rectCon) < 2:
            return img, {'img':img,'imgGray':imgGray,'imgCanny':imgCanny,
                         'imgContours':img.copy(),'imgBigContour':img.copy(),
                         'imgThresh':imgBlank.copy(),'imgWarpColored':imgBlank.copy()}
        
        biggestPoints = utlis.getCornerPoints(rectCon[0])
        gradePoints = utlis.getCornerPoints(rectCon[1])
        
        if biggestPoints is None or gradePoints is None:
            return img, None
        
        biggestPoints = utlis.reorder(biggestPoints)
        pts1 = np.float32(biggestPoints)
        pts2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        
        gradePoints = utlis.reorder(gradePoints)
        ptsG1 = np.float32(gradePoints)
        ptsG2 = np.float32([[0,0],[325,0],[0,150],[325,150]])
        matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)
        
        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
        boxes = utlis.splitBoxes(imgThresh, questions, choices)
        
        myPixelVal = np.zeros((questions, choices))
        countR = countC = 0
        for image in boxes:
            myPixelVal[countR][countC] = cv2.countNonZero(image)
            countC += 1
            if countC == choices:
                countC = 0
                countR += 1
        
        myIndex = [np.where(myPixelVal[x] == np.amax(myPixelVal[x]))[0][0] for x in range(questions)]
        grading = [1 if ans[x] == myIndex[x] else 0 for x in range(questions)]
        score = (sum(grading) / questions) * 100
        
        utlis.showAnswers(imgWarpColored, myIndex, grading, ans, questions, choices)
        utlis.drawGrid(imgWarpColored, questions, choices)
        
        imgRawDrawings = np.zeros_like(imgWarpColored)
        utlis.showAnswers(imgRawDrawings, myIndex, grading, ans, questions, choices)
        invMatrix = cv2.getPerspectiveTransform(pts2, pts1)
        imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))
        
        imgRawGrade = np.zeros((150, 325, 3), dtype=np.uint8)
        cv2.putText(imgRawGrade, f"{int(score)}%", (70, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
        invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1)
        imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))
        
        imgFinal = cv2.addWeighted(img.copy(), 1, imgInvWarp, 0.7, 0)
        imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)
        cv2.putText(imgFinal, f"Score: {int(score)}%", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
        
        return imgFinal, {'img':img,'imgGray':imgGray,'imgCanny':imgCanny,
                         'imgContours':img.copy(),'imgBigContour':img.copy(),
                         'imgThresh':imgThresh,'imgWarpColored':imgWarpColored,'imgFinal':imgFinal}
    
    except Exception as e:
        print(f"⚠️ Processing Error: {e}")
        return img.copy() if 'img' in locals() else np.zeros((heightImg, widthImg, 3), dtype=np.uint8), None

# ================= MAIN =================
def main():
    # تهيئة بيئة النوافذ لويندوز أحياناً محتاجة ده عشان الكيبورد يشتغل
    cv2.startWindowThread() if os.name == 'nt' else None

    webCamFeed = selectMode()
    if webCamFeed is None:
        cv2.destroyAllWindows()
        return
    
    cap = None
    try:
        if webCamFeed:
            cap = cv2.VideoCapture(0)
            cap.set(10, 160)
            if not cap.isOpened():
                print("❌ Camera failed. Try changing cv2.VideoCapture(0) to (1)")
                return
        else:
            if not os.path.exists(pathImage):
                print(f"❌ Image not found: {pathImage}")
                return
        
        imgBlank = np.zeros((heightImg, widthImg, 3), dtype=np.uint8)
        count = 0
        os.makedirs("Scanned", exist_ok=True)
        print("🎮 Controls: [S] Save | [Q/ESC] Quit | Click window to focus!")
        
        while True:
            if webCamFeed:
                success, img = cap.read()
                if not success: continue
            else:
                img = cv2.imread(pathImage)
                if img is None: break
                
            imgFinal, processed = processOMR(img.copy(), imgBlank)
            
            if processed:
                imageArray = ([processed['img'], processed['imgGray'], processed['imgCanny'], processed['imgContours']],
                             [processed['imgBigContour'], processed['imgThresh'], processed['imgWarpColored'], processed.get('imgFinal', imgBlank)])
            else:
                blank = np.zeros((heightImg, widthImg, 3), dtype=np.uint8) + 255
                imageArray = ([blank]*4, [blank]*4)
                
            labels = [["Original","Gray","Edges","Contours"],["BigContour","Threshold","Warped","Final"]]
            stackedImage = utlis.stackImages(imageArray, 0.5, labels)
            
            cv2.putText(stackedImage, "[S] Save  [Q] Quit", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(imgFinal, "[S] Save  [Q] Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # ترتيب النوافذ صحيح عشان الفوكس يشتغل
            cv2.imshow("Processing Steps", stackedImage)
            cv2.imshow("FINAL RESULT", imgFinal)
            cv2.moveWindow("Processing Steps", 50, 50)
            cv2.moveWindow("FINAL RESULT", 900, 50)
            
            # ⚠️ waitKey(1) للكيبورد + تحديث الشاشة | waitKey(0) للصورة عشان يستنى
            key = cv2.waitKey(1 if webCamFeed else 0) & 0xFF
            
            if key == ord('s'):
                fname = f"Scanned/omr_{count:03d}.jpg"
                cv2.imwrite(fname, imgFinal)
                print(f"💾 Saved: {fname}")
                count += 1
            elif key in [ord('q'), ord('Q'), 27]:
                print("👋 Closing...")
                break
    finally:
        if cap is not None: cap.release()
        cv2.destroyAllWindows()
        print("✅ Done.")

if __name__ == "__main__":
    main()