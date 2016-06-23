import json
import difflib

SUBJECT_ARR = ["Arts and Humanities",
               "Mathematics",
               "Biology and Life Sciences",
               "Physical Science",
               "Social Science",
               "Business",
               "Engineering",
               "Computer Science",
               "Data Science",
               "Education & Teaching",
               "Personal Development",
               "Language Learning"]

TOPICS_ARR = [
               ["History", "Music and Visual Arts", "Philosophy and Ethics", "Design & Creativity", "Literature", "Religion & Culture", "Film & Theatre", "Digital Media & Video Games"],
               ["Math", "Logic"],
               ["Animals and Veterinary Science", "Bioinformatics", "Biology", "Medicine & Healthcare", "Nutrition", "Clinical Science"],
               ["Environmental Science and Sustainability", "Physics and Astronomy", "Research Methods", "Energy & Earth Sciences", "Chemistry"],
               ["Politics", "Governance and Society", "Law", "Psychology"],
               ["Leadership and Management", "Economics and Finance", "Marketing", "Entrepreneurship", "Business Essentials", "Business Strategy"],
               ["Architecture", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Materials Science & Engineering"],
               ["Software Development", "Mobile and Web Development", "Algorithms", "Computer Security and Networks", "Design and Product", "Artificial Intelligence"],
               ["Data Analysis", "Machine Learning", "Probability and Statistics"],
               ["K12", "STEM", "Higher Education", "Teacher Development", "Classroom Development", "Online Education", "Test Prep"],
               ["Communication", "Sport & Leisure"],
               ["Learning English", "Other Languages"]
             ]

