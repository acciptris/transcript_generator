# GUI-based Transcript Generator

GUI-based transcript generator for generating interim academic transcripts from student grades data. Project made as a part of CS384 (Python Programming) course at IIT Patna.


## Requirements
The following packages have been used:
*   `fpdf2` for PDF document generation
*   `PyQt6` for GUI

These packages can be installed using the following command.
```
pip install fpdf2 PyQt6
```


## Usage

1. Clone this repo and change directory to `./transcript_generator`.
2. Run `python app.py`. GUI interface will open.
3. Images for seal and signature can be chosen in the interface.
4. If required, enter roll number range of required transcripts and click "Generate for roll no. range". Otherwise, click "Generate all Transcripts".
5. Required transcripts will be generated in `./transcripts` directory.

The students and grades data used for generation are stored in `./input` directory.
* `grades.csv`: Data containing roll number, semester number, course code, number of credits, grade obtained, subject type for each course taken by each student.
* `names-roll.csv`: Data containing name and roll number of each student.
* `subjects_masters.csv`: Data containing course code, course name and course credit details.


<!-- ## Features -->


<!-- ## Screenshots -->
