# OMR Auto Grading System using OpenCV

An intelligent Optical Mark Recognition (OMR) system built with Python and OpenCV that automatically detects, analyzes, and grades multiple-choice answer sheets with high accuracy and efficiency.

## Project Description

This automated grading system eliminates the time-consuming process of manual answer sheet correction by leveraging advanced computer vision techniques. The system can process answer sheets from various angles, automatically detect marked responses, compare them against answer keys, and generate comprehensive results in Excel format.

## Key Features

- **Automatic Sheet Detection**: Identifies answer sheet boundaries regardless of rotation or perspective
- **Perspective Correction**: Warps skewed images to top-down view for accurate analysis
- **Real-time Processing**: Fast and efficient image processing pipeline
- **Multi-format Support**: Handles JPG, JPEG, PNG, and BMP image formats
- **Intelligent Grading**: Detects correct, wrong, empty, and multi-selection responses
- **Visual Feedback**: Color-coded results with green (correct), red (wrong), and yellow (multi-selection) indicators
- **Excel Export**: Automatic generation of detailed results in spreadsheet format
- **Graphical User Interface**: User-friendly Tkinter-based interface for easy operation
- **Dynamic Thresholding**: Adaptive pixel-based detection for accurate response identification

## Technical Overview

The system employs a sophisticated image processing pipeline:

1. **Image Preprocessing**: Converts input images to grayscale and applies Gaussian blur to reduce noise
2. **Edge Detection**: Utilizes Canny edge detection to identify sheet boundaries
3. **Contour Analysis**: Detects the largest quadrilateral contour representing the answer sheet
4. **Perspective Transformation**: Applies warp perspective to correct sheet orientation
5. **Grid Segmentation**: Divides the corrected sheet into individual answer cells
6. **Pixel Analysis**: Counts non-zero pixels in each cell to detect marked responses
7. **Grading Logic**: Compares detected responses against the answer key
8. **Result Visualization**: Overlays colored circles on detected answers
9. **Data Export**: Generates comprehensive Excel reports with question-wise analysis

## Image Processing Pipeline

### Stage 1: Grayscale Conversion
Transforms the input image from BGR color space to grayscale, simplifying subsequent processing operations while preserving essential structural information.

### Stage 2: Gaussian Blurring
Applies a 5x5 Gaussian kernel to smooth the image and reduce high-frequency noise, improving the accuracy of edge detection.

### Stage 3: Canny Edge Detection
Implements the Canny algorithm with thresholds of 10 and 50 to detect sharp intensity transitions, highlighting the boundaries of the answer sheet and marked regions.

### Stage 4: Contour Detection
Identifies all external contours in the edge-detected image and filters them based on area and polygonal approximation to locate the answer sheet boundary.

### Stage 5: Perspective Correction
Reorders the detected corner points and applies perspective transformation to generate a top-down, undistorted view of the answer sheet with dimensions 700x700 pixels.

### Stage 6: Thresholding
Applies binary inverse thresholding with a value of 170 to isolate marked regions, converting them to white pixels against a black background.

### Stage 7: Grid Extraction
Splits the thresholded image into a 5x5 grid (5 questions, 5 choices each) using vertical and horizontal splitting operations.

### Stage 8: Response Detection
Counts non-zero pixels in each grid cell and applies a threshold of 5000 pixels to determine whether a choice has been marked.

### Stage 9: Grading and Visualization
Compares detected responses with the answer key [B, C, A, B, E], calculates the score, and overlays colored circles indicating correctness.

## System Requirements

### Core Dependencies
- Python 3.7 or higher
- OpenCV (cv2) version 4.5 or higher
- NumPy for numerical operations
- Pandas for Excel export
- Pillow (PIL) for image handling in GUI
- Tkinter for graphical user interface

### Installation

1. Clone or download the project repository

2. Install required packages:
```bash
pip install opencv-python numpy pandas pillow
```

3. Ensure Tkinter is installed (usually included with Python installation)

## Project Structure

```
OMR-Auto-Grading-System/
│
├── OMR_Main.py                 # Main application file with GUI and core logic
├── utlis.py                    # Utility functions for image processing
├── README.md                   # Project documentation
├── Final_Result_Project.xlsx   # Output results file (auto-generated)
│
├── assets/
│   ├── original.jpg           # Sample input images
│   ├── original2.jpg
│   ├── original3.jpg
│   ├── gray.jpg               # Grayscale conversion example
│   ├── edges.jpg              # Edge detection result
│   ├── contours.jpg           # Contour detection visualization
│   ├── warped.jpg             # Perspective-corrected image
│   ├── final.jpg              # Final graded result
│   └── demo.gif               # System demonstration
│
└── Scanned/
    └── [Answer sheet images]
```

## Usage Instructions

### Method 1: Graphical User Interface

1. Run the main application:
```bash
python OMR_Main.py
```

2. Click the "Browse" button to select an answer sheet image

3. Click the "Grade" button to process the image

4. View the score displayed in the GUI

5. Check the generated Excel file "Final_Result_Project.xlsx" for detailed results

6. The corrected image with visual feedback is displayed in the application window

### Method 2: Command Line (if implemented)

```bash
python OMR_Main.py --image path/to/answer_sheet.jpg
```

### Input Specifications

- **Image Format**: JPG, JPEG, PNG, or BMP
- **Sheet Layout**: 5 questions with 5 choices each (A, B, C, D, E)
- **Marking Method**: Fully shaded/filled circles
- **Image Quality**: Minimum resolution of 640x480 recommended
- **Sheet Orientation**: Any angle (system auto-corrects perspective)

### Output Specifications

- **Excel Report**: Contains question-wise status, individual grades, and total score
- **Visual Result**: Annotated image with colored circles indicating:
  - Green: Correct answer
  - Red: Wrong answer (with small green circle showing correct choice)
  - Yellow: Multiple selections (invalid)
  - No mark: Empty/unanswered

## Configuration

The system can be customized by modifying the settings in `OMR_Main.py`:

```python
widthImg  = 700          # Output image width
heightImg = 700          # Output image height
questions = 5            # Number of questions
choices   = 5            # Number of choices per question
ans       = [1, 2, 0, 1, 4]   # Answer key (0=A, 1=B, 2=C, 3=D, 4=E)
threshold_val = 5000     # Pixel threshold for detecting marked answers
```

## Algorithm Details

### Perspective Transformation

The system uses a four-point perspective transform to correct sheet orientation:

1. Detect the largest quadrilateral contour
2. Order points consistently (top-left, top-right, bottom-left, bottom-right)
3. Calculate transformation matrix using `cv2.getPerspectiveTransform()`
4. Apply warp to generate top-down view

### Response Detection Logic

For each question row:
- Count non-zero pixels in each choice cell
- If pixels > 5000: Choice is marked
- If multiple choices marked: Invalid (Multi-Selection)
- If one choice marked: Compare with answer key
- If no choices marked: Empty

### Grading Formula

```
Score = (Number of Correct Answers / Total Questions) × 100
```

## Error Handling

The system includes robust error handling for:

- **File Not Found**: Displays error message if image path is invalid
- **Sheet Detection Failure**: Warns user if answer sheet boundary cannot be detected
- **Empty Image Path**: Prompts user to select an image before grading
- **Low Quality Images**: Threshold filtering helps handle varying image qualities

## Performance Metrics

- **Processing Time**: Typically 1-3 seconds per image
- **Accuracy**: High accuracy with properly shaded answers
- **Robustness**: Handles rotated, skewed, and varying lighting conditions
- **Scalability**: Can be extended to handle more questions and choices

## Advantages Over Manual Grading

1. **Speed**: Processes sheets in seconds versus minutes manually
2. **Accuracy**: Eliminates human error in counting and marking
3. **Consistency**: Applies uniform grading criteria
4. **Objectivity**: Removes grader bias
5. **Efficiency**: Handles large volumes effortlessly
6. **Record Keeping**: Automatic Excel export for data management
7. **Visual Verification**: Colored overlays allow quick result verification

## Limitations and Considerations

- Requires clearly visible answer sheet boundaries
- Marked circles should be sufficiently filled (not just checked)
- Extreme lighting conditions may affect detection accuracy
- Current implementation supports 5×5 grid (customizable)
- Image resolution should be adequate for contour detection

## Future Enhancements

1. Support for variable numbers of questions and choices
2. QR code or barcode integration for student identification
3. Batch processing of multiple sheets
4. Cloud-based storage and result management
5. Mobile application for on-the-go grading
6. Support for different answer sheet templates
7. Machine learning-based adaptive thresholding
8. Integration with learning management systems (LMS)
9. Optical character recognition (OCR) for student names
10. Statistical analysis and performance reporting

## Development Team

**Team Leader**: Ganna Amr Emad Eldin

**Team Members**:
- Habiba Saad Mohamed
- Haneen Mahmoud Abdel Fattah
- Rana Basyouni Askar
- Maryam Teama
- Hana Radwan

## Academic Supervision

**Course Instructor**: Dr. Marwa Elsedik

**Engineering Supervisor**: Eng. Abdelraouf Hawash

## Acknowledgments

This project was developed as part of the Computer Vision and Image Processing course at the Faculty of Artificial Intelligence, Kafrelsheikh University.

We extend our gratitude to Dr. Marwa Elsedik for her invaluable guidance and support throughout the development of this system.

## Educational Purpose

This project is developed solely for educational and academic purposes. It demonstrates the practical application of computer vision techniques in solving real-world problems.

## License

This project is created for educational purposes. The code and documentation are intended for learning and academic use.

## References and Technologies Used

- **OpenCV**: Open Source Computer Vision Library
- **NumPy**: Numerical computing with Python
- **Pandas**: Data manipulation and analysis
- **Pillow**: Python Imaging Library
- **Tkinter**: Python standard GUI framework

## Contact

For questions, suggestions, or collaboration, please contact the development team through the Faculty of Artificial Intelligence, Kafrelsheikh University.

---

**Faculty of Artificial Intelligence**  
**Kafrelsheikh University**  
**Academic Year 2025-2026**
