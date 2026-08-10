# Student Management System
class Student:
    def __init__(self, name: str, age: int, grade: str):
        self.name = name
        self.age = age
        self.grade = grade

    def __str__(self):
        return f"Student Name: {self.name}, Age: {self.age}, Grade: {self.grade}"

    def update_student_info(self, name: str = None, age: int = None, grade: str = None):
        if name:
            self.name = name
        if age:
            self.age = age
        if grade:
            self.grade = grade
        return 'Student information updated successfully.'

    def delete_student_info(self):
        self.name = ""
        self.age = 0
        self.grade = ""
        return 'Student information deleted successfully.'

    def attendance(self, status: str):
        if status.lower().strip() == 'present':
            return f'{self.name} is present today.'
        if status.lower().strip() == 'absent':
            return f'{self.name} is absent today.'
        return 'Invalid attendance status. Please enter "present" or "absent".'

    def progress_report(self, subject: str, marks: int):
        if marks >= 90:
            grade = 'A'
        elif marks >= 80:
            grade = 'B'
        elif marks >= 70:
            grade = 'C'
        elif marks >= 60:
            grade = 'D'
        else:
            grade = 'F'
        return f'{self.name} scored {marks} in {subject}, and received a grade of {grade}.'


print('Welcome to the Student Management System!')

while True:
    try:
        name = input('Enter student name: ').strip()
        age = int(input('Enter student age: '))
        grade = input('Enter student grade: ').strip()
        student1 = Student(name, age, grade)
        break
    except ValueError:
        print("❌ Invalid input! Age must be a number. Please try again.")

while True:
    print('\nMenu:')
    print('1. Display Student Information')
    print('2. Update Student Information')
    print('3. Delete Student Information')
    print('4. Mark Attendance')
    print('5. Generate Progress Report')
    print('6. Exit')

    choice = input('Enter your choice (1-6): ').strip()

    if choice == '1':
        print(student1)

    elif choice == '2':
        new_name = input('Enter new name (Leave blank to keep current): ').strip()
        new_age = input('Enter new age (Leave blank to keep current): ').strip()
        new_grade = input('Enter new grade (Leave blank to keep current): ').strip()

        student1.update_student_info(
            name=new_name if new_name else None,
            age=int(new_age) if new_age.isdigit() else None,
            grade=new_grade if new_grade else None
        )
        print('Student information updated successfully.')

    elif choice == '3':
        confirmation = input('Are you sure you want to delete the student information? (yes/no): ')
        if confirmation.lower().strip() == 'yes':
            print(student1.delete_student_info())
            del student1
            break
        else:
            print('Deletion cancelled.')

    elif choice == '4':
        attendance_status = input('Enter attendance status (present/absent): ')
        print(student1.attendance(attendance_status))

    elif choice == '5':
        try:
            subject = input('Enter subject name: ').strip()
            marks = int(input('Enter marks obtained: '))
            print(student1.progress_report(subject, marks))
        except ValueError:
            print("❌ Invalid input! Marks must be a valid number.")

    elif choice == '6':
        print('Exiting the Student Management System. Goodbye!')
        break

    else:
        print('Invalid choice. Please try again.')
