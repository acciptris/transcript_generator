import csv
import os
from datetime import datetime

from fpdf import FPDF


def get_grade_point(grade):
    grade_point_dict = {
        "AA": 10,
        "AB": 9,
        "BB": 8,
        "BC": 7,
        "CC": 6,
        "CD": 5,
        "DD": 4,
        "F": 0,
        "I": 0,
    }
    grade = grade.strip()
    if grade[-1] == "*":
        grade = grade[:-1]
    point = grade_point_dict[grade]
    return point


def get_year_of_admission(roll):
    short_year = roll[:2]
    long_year = "20" + short_year
    return long_year


def get_programme(roll):
    decider = roll[2:4]
    if decider == "01":
        return "Bachelor of Technology"
    elif decider == "11":
        return "Master of Technology"
    elif decider == "12":
        return "Master of Science"
    elif decider == "21":
        return "Doctor of Philosophy"


def get_course(roll):
    decider = roll[4:6]
    dict = {
        "CS": "Computer Science and Technology",
        "EE": "Electrical and Electronics Engineering",
        "ME": "Mechanical Engineering",
        "CE": "Civil Engineering",
    }
    return dict[decider]


def get_cpi(spi, credits_taken):
    cpi = 0
    total_credits = 0
    for sem in spi:
        cpi += spi[sem] * credits_taken[sem]
        total_credits += credits_taken[sem]
    cpi /= total_credits
    return cpi


def generate_transcript(
    grades_file_path="input/grades.csv",
    subjects_file_path="input/subjects_master.csv",
    names_file_path="input/names-roll.csv",
    input_roll_numbers=[],
    seal_dir="",
    sign_dir="",
):
    grades_data = {}
    # Nested dictionary to stores grades of students
    # First key: roll number, Second key: semester number
    # The value is a list of grade details of the subjects
    # enrolled by the student in that particular semester
    with open(grades_file_path) as grades_file:
        for grade in csv.DictReader(grades_file):
            roll = grade["Roll"]
            sem = int(grade["Sem"])

            if roll not in grades_data:
                grades_data[roll] = {}
            if sem not in grades_data[roll]:
                grades_data[roll][sem] = []

            grades_data[roll][sem].append(grade)

    subjects_data = {}
    # Dictionary with subject codes as keys and subject names as values
    with open(subjects_file_path) as subjects_file:
        for subject in csv.DictReader(subjects_file):
            subjects_data[subject["subno"]] = subject

    names_data = {}
    # Dictionary with roll number as keys and student names as values
    with open(names_file_path) as names_file:
        for name in csv.DictReader(names_file):
            names_data[name["Roll"]] = name["Name"]

    try:
        os.mkdir("./transcripts")
    except FileExistsError:
        pass
    except:
        print("Error making './transcripts' directory.\nTerminating function")
        return

    invalid_roll_numbers = []
    valid_roll_numbers = []
    if len(input_roll_numbers) != 0:
        for roll in input_roll_numbers:
            if roll in grades_data:
                valid_roll_numbers.append(roll)
            else:
                invalid_roll_numbers.append(roll)
    else:
        # valid_roll_numbers = ["0501CS16"]
        valid_roll_numbers = list(grades_data.keys())

    x = []
    for roll in valid_roll_numbers:
        gap = 2
        logo_size = 40
        details_margin = 80

        pdf = FPDF(orientation="landscape", format="A3")
        pdf.add_page()
        pdf.set_font("helvetica", size=10)
        line_height = pdf.font_size * 1.25
        subtable_width = pdf.epw / 3
        pdf.b_margin = pdf.t_margin
        pdf.r_margin = pdf.l_margin - gap
        pdf.rect(x=pdf.l_margin, y=pdf.t_margin, w=pdf.epw, h=pdf.eph)

        # Transcript Header
        pdf.image(
            "logo.jpg",
            x=pdf.l_margin + gap,
            y=pdf.t_margin + gap,
            w=logo_size,
            h=logo_size,
        )
        pdf.set_xy(
            pdf.l_margin + gap, pdf.t_margin + logo_size + 2 * gap,
        )
        pdf.cell(
            logo_size, txt="--**INTERIM TRANSCRIPT**--", align="C", markdown=True,
        )
        pdf.image(
            "logo.jpg",
            x=pdf.l_margin + pdf.epw - logo_size - gap,
            y=pdf.t_margin + gap,
            w=logo_size,
            h=logo_size,
        )
        pdf.set_xy(
            pdf.l_margin + pdf.epw - logo_size - gap,
            pdf.t_margin + logo_size + 2 * gap,
        )
        pdf.image(
            "heading.png",
            x=pdf.l_margin + logo_size + 3 * gap + pdf.line_width,
            y=pdf.t_margin + gap,
            w=pdf.epw - 2 * (logo_size + 3 * gap + pdf.line_width),
            h=logo_size,
        )
        pdf.cell(
            logo_size, txt="--**INTERIM TRANSCRIPT**--", align="C", markdown=True,
        )
        pdf.line(
            pdf.l_margin,
            pdf.t_margin + logo_size + 3 * gap + pdf.font_size,
            pdf.l_margin + pdf.epw,
            pdf.t_margin + logo_size + 3 * gap + pdf.font_size,
        )
        pdf.line(
            pdf.l_margin + logo_size + 2 * gap,
            pdf.t_margin,
            pdf.l_margin + logo_size + 2 * gap,
            pdf.t_margin + logo_size + 3 * gap + pdf.font_size,
        )
        pdf.line(
            pdf.l_margin + pdf.epw - (logo_size + 2 * gap),
            pdf.t_margin,
            pdf.l_margin + pdf.epw - (logo_size + 2 * gap),
            pdf.t_margin + logo_size + 3 * gap + pdf.font_size,
        )

        # Students details
        pdf.set_xy(
            details_margin,
            pdf.t_margin + logo_size + 4 * gap + pdf.font_size + pdf.line_width,
        )
        col_width = (pdf.epw - 2 * details_margin) / 3
        pdf.multi_cell(
            col_width,
            line_height,
            f"**Roll No**: {roll}",
            align="L",
            markdown=True,
            ln=3,
        )
        pdf.multi_cell(
            col_width,
            line_height,
            f"**Name**: {names_data[roll]}",
            align="L",
            markdown=True,
            ln=3,
        )
        pdf.multi_cell(
            col_width,
            line_height,
            f"**Year of Admission**: {get_year_of_admission(roll)}",
            align="L",
            markdown=True,
            ln=3,
        )
        pdf.ln(line_height)
        pdf.set_x(details_margin)
        pdf.multi_cell(
            col_width,
            line_height,
            f"**Programme**: {get_programme(roll)}",
            align="L",
            markdown=True,
            ln=3,
        )
        pdf.multi_cell(
            col_width * 2,
            line_height,
            f"**Course**: {get_course(roll)}",
            align="L",
            markdown=True,
            ln=3,
        )
        pdf.rect(
            details_margin,
            pdf.t_margin + logo_size + 4 * gap + pdf.font_size + pdf.line_width,
            pdf.epw - 2 * details_margin,
            2 * line_height,
        )

        y_max = (
            pdf.t_margin
            + logo_size
            + 4 * gap
            + pdf.font_size
            + pdf.line_width
            + 2 * line_height
        )
        y_max_new = y_max

        # Dictionaries to store credit and spi with semester number as keys
        credits_taken = {}
        credits_cleared = {}
        spi = {}

        for nsem, sem in enumerate(sorted(grades_data[roll])):
            pdf.set_font(style="BU")
            pdf.set_xy(pdf.l_margin + (nsem % 3) * subtable_width + gap, y_max + gap)
            pdf.cell(txt=f"Semester {sem}")
            pdf.ln(line_height)
            pdf.set_x(pdf.l_margin + (nsem % 3) * subtable_width + gap)
            pdf.set_font("helvetica", size=9)
            subtable_heading = ["Sub. Code", "Subject Name", "L-T-P", "CRD", "GRD"]
            subtable_column_widths = [0.149, 0.601, 0.09, 0.08, 0.08]
            pdf.set_font(style="B")
            for ih, heading in enumerate(subtable_heading):
                pdf.multi_cell(
                    (subtable_width - gap) * subtable_column_widths[ih],
                    line_height,
                    heading,
                    align="C",
                    ln=3,
                    border=1,
                )
            pdf.ln(line_height)
            pdf.set_x(pdf.l_margin + (nsem % 3) * subtable_width + gap)

            credits_taken[sem] = 0
            credits_cleared[sem] = 0
            spi[sem] = 0

            for i, grade_dict in enumerate(
                sorted(grades_data[roll][sem], key=lambda d: d["SubCode"]), 1
            ):
                data_line = []
                subno = grade_dict["SubCode"]
                credit = int(grade_dict["Credit"])

                data_line.append(subno)
                data_line.append(subjects_data[subno]["subname"])
                data_line.append(subjects_data[subno]["ltp"])
                data_line.append(credit)
                data_line.append(grade_dict["Grade"])

                pdf.set_font("helvetica", size=9)
                for id, data in enumerate(data_line):
                    pdf.multi_cell(
                        (subtable_width - gap) * subtable_column_widths[id],
                        line_height,
                        str(data),
                        align="C",
                        ln=3,
                        border=1,
                        max_line_height=2 * pdf.font_size,
                    )
                pdf.ln(line_height)
                pdf.set_x(pdf.l_margin + (nsem % 3) * subtable_width + gap)

                credits_taken[sem] += credit
                spi[sem] += credit * get_grade_point(grade_dict["Grade"])
                if get_grade_point(grade_dict["Grade"]) != 0:
                    credits_cleared[sem] += credit
            spi[sem] /= credits_taken[sem]
            cpi = get_cpi(spi, credits_taken)
            pdf.set_font(style="B")
            pdf.set_xy(pdf.get_x(), pdf.get_y() + gap)
            pdf.multi_cell(
                (subtable_width - gap) * 0.9,
                line_height * 1.25,
                txt=f"Credits Taken: {credits_taken[sem]}        Credits Cleared: {credits_cleared[sem]}        SPI: {spi[sem]:.2f}        CPI: {cpi:.2f}",
                border=1,
                align="L",
            )

            y_max_new = max(y_max_new, pdf.get_y()) + gap / 2
            if nsem % 3 == 2 or nsem == len(sorted(grades_data[roll])) - 1:
                y_max = y_max_new
                pdf.line(
                    pdf.l_margin, y_max, pdf.l_margin + pdf.epw, y_max,
                )

        curr_time = datetime.now().strftime("%d %b %Y, %H:%M")
        pdf.set_font(style="B")
        pdf.set_xy(pdf.l_margin + gap, pdf.eph - 2 * gap - pdf.font_size)
        pdf.cell(txt=f"Date Generated: {curr_time}")

        pdf.line(
            pdf.l_margin + pdf.epw - 50,
            pdf.eph - 2 * gap - pdf.font_size,
            pdf.l_margin + pdf.epw - 5 * gap,
            pdf.eph - 2 * gap - pdf.font_size,
        )
        pdf.set_xy(pdf.l_margin + pdf.epw - 50, pdf.eph - gap - pdf.font_size)
        pdf.cell(
            50 - 5 * gap, txt="Assistant Registrar (Academic)", align="C",
        )
        if len(sign_dir) != 0:
            pdf.image(
                sign_dir,
                x=pdf.l_margin + pdf.epw - 50,
                y=pdf.eph - 4 * gap - pdf.font_size - logo_size * 0.3,
                w=logo_size * 0.8,
            )

        if len(seal_dir) != 0:
            pdf.image(
                seal_dir,
                x=(pdf.l_margin + pdf.epw) / 2,
                y=pdf.eph - logo_size * 0.6,
                w=logo_size * 0.6,
            )

        pdf.output("transcripts/" + roll + ".pdf")

    invalid_roll_numbers.sort()
    return invalid_roll_numbers
