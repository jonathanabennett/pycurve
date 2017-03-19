from statistics import mean
import csv

class Student:

    def __init__(self, name, section, raw):
        self.name = name
        self.section = section
        self.raw = raw
        self.curved = {}

    def get_curve(self, scale, boost):
        self.curved[int(scale * 100)] = scale * self.raw + boost


class Assessment:

    def __init__(self, name, students=[]):
        self.name = name
        self.students = students
        self.analyze()

    def analyze(self):
        if self.students:
            self.raw_avg = mean([student.raw for student in self.students])
            self.raw_low = min([student.raw for student in self.students])
            self.raw_high = max([student.raw for student in self.students])

            self.curved_avg = mean([student.curved.get(55,0) for student in self.students])
            self.curved_low = min([student.curved.get(55,0) for student in self.students])
            self.curved_high = max([student.curved.get(55,0) for student in self.students])
        else:
            self.raw_avg = 0
            self.raw_low = 0
            self.raw_high = 88

    def curve(self, scale=0.55, max_curve=98):
        if self.raw_high > max_curve: max_curve = self.raw_high

        boost = max_curve - scale * self.raw_high
        for student in self.students:
            student.get_curve(scale, boost)
        self.analyze()

    def add_student(self, student_name, student_section, student_raw):
        self.students.append(Student(student_name, student_section,
                                     student_raw))
        self.analyze()
        self.curve()

    def save(self, dialect='csv'):
        with open("%s.csv" % (self.name), 'w', newline='') as csvfile:
            assess_writer = csv.writer(csvfile, dialect='excel')
            assess_writer.writerow(["Name", "Class", "Raw Score",
                                    "Curved Score"])
            for student in self.students:
                assess_writer.writerow([student.name, student.section,
                                        student.raw, student.curved.get(55,0)])


def assessment_loader(self, data_file, dialect='csv'):
    if dialect == 'csv':
        with open(data_file, 'r', newline='') as csvfile:
            name = data_file.split('.')[0]
            assessment = Assessment(name)
            filereader = csv.reader(csvfile, dialect='excel')
            next(filereader) #Throw away the header row
            for row in filereader:
                assessment.add_student(row[0], row[1], int(row[2]))

def tui():
    while True:
        print("""Welcome to the test curver. Please enter the following data
              about your test.""")
        name = input("What would you like to call it? ")
        assessment = Assessment(str(name))
        print("""Now, let's add your students. Enter student information
              below.""")
        cont = True
        while cont:
            name = input("Student's name: ")
            section = input("Class/Period: ")
            raw = input("What is their raw score (percent) ")
            assessment.add_student(name, section, int(raw))
            ret = input("Add another student? Y/n ")
            if ret in ("Nn"): cont = False
        print("Here are the statistics for your test:")
        assessment.analyze()
        print("Lowest raw/curved score: %s / %s" % (assessment.raw_low,
                                                    assessment.curved_low))
        print("Highest raw/curved score: %s / %s" % (assessment.raw_high,
                                                     assessment.curved_high))
        print("Raw / Curved Average score: %s / %s" % (assessment.raw_avg,
                                                       assessment.curved_avg))
        print("And here are the statistics by student: ")
        print("Name\t\tSection\tRaw\tCurved")
        for student in assessment.students:
            print("%s\t%s\t%s\t%s" % (student.name, student.section,
                                      student.raw, student.curved.get(55,0)))
        assessment.save()
        break

if __name__ == "__main__":
    tui()
