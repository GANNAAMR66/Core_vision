# Core_vision
OMR Auto Grading System using OpenCV that detects, analyzes, and grades MCQ answer sheets in real-time with high accuracy
# 🎯 OMR MCQ Auto Grading System with OpenCV

![Demo](demo.mp4)

---

## 📌 Overview

An intelligent **OMR (Optical Mark Recognition) system** built with Python and OpenCV that automatically detects and grades MCQ answer sheets in real-time using computer vision techniques.

---

## 📸 Demo

### 📝 Input Sheet

![Original](Optical-Mark-Recognition-OPENCV-master/asset/original.jpg)
![Original2](original2.jpg)
![Original3](original3.jpg)
![Test Sheet](2choices_no_answers.jpg)

---

## 🔍 Image Processing Pipeline

### 1️⃣ Grayscale Conversion

Convert image to grayscale for easier processing.

### 2️⃣ Gaussian Blur

Reduce noise for better edge detection.

### 3️⃣ Edge Detection (Canny)

Detect object boundaries in the image.

### 4️⃣ Contour Detection

Identify the answer sheet using the largest contour.

---

## 📸 Processing Steps

### Grayscale

![Gray](asset/gray.jpg)

### Edge Detection

![Edges](Edges.jpg)

### Contours

![Contours](contours.jpg)
### threshold

![threshold](threshold.jpg)

---

## 📐 Perspective Transformation

The sheet is warped to a top-down view for accurate analysis.

![Warped](wraped.jpg)

---

## ✅ Final Result

![Result](final.jpg)

---

## 🚀 Features

* 📷 Real-time webcam scanning
* 🖼️ Image-based processing
* 🔍 Automatic answer detection
* 📐 Perspective correction
* 🧠 Pixel-based grading
* 📊 Score visualization

---

## 🛠️ Technologies Used

* Python
* OpenCV
* NumPy

---

## ⚙️ How It Works

The system follows a full image processing pipeline: preprocessing → contour detection → perspective transform → pixel analysis → grading.

---

## 📂 Project Structure

```bash
OMR-Auto-Grading-System/
│── main.py
│── utlis.py
│── README.md
│
├── assets/
│   │── original.jpg
│   │── original2.jpg
│   │── original3.jpg
│   │── 2choices_no_answers.jpg
│   │── gray.jpg
│   │── edges.jpg
│   │── contours.jpg
│   │── warped.jpg
│   │── final.jpg
│   │── demo.gif
│
└── Scanned/
```

---

## ▶️ How to Run

```bash
pip install opencv-python numpy
python main.py
```

---

## 🎮 Controls

* Press **'s'** → Save result
* Press **ESC** → Exit

---

## 👩‍💻 Team

* **Ganna Amr Emad Eldin** — Team Leader
* Habiba Saad Mohamed
* Haneen Mahmoud Abdel Fattah
* Rana Basyouni Askar
* Maryam Teama
* Hana Radwan

---

## ⭐ Acknowledgment

This project was developed as part of a Computer Vision and Image Processing course.

---

## 📌 License

For educational purposes only.

---

⭐ If you like this project, give it a star!

