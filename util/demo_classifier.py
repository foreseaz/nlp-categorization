"""
======================================================
Demo Mapping of Courses into Subjects and Topics
using simple character similarity
======================================================
"""
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

def export_course(courses):
  with open('demo_courses.json', 'w') as f:
    f.write(json.dumps(courses))
  print "DONE: Write Demo courses to demo_courses.json \n      Total course: %d" %len(courses)

def has_categories(course):
  has = True
  categories = course.get('categories')
  if not categories:
    has = False
  return has
  
with open('./classify_langs/en_courses.json') as json_data:
  courses = json.load(json_data)
  json_data.close()
   
  sm = difflib.SequenceMatcher(None)
  cate_courses = [c for (c) in courses if has_categories(c)]
  result_courses_arr = []
  for course in cate_courses:
    categories = "".join(course.get("categories"))
    sm.set_seq1(categories)

    subj_id = 0
    topic_id = 0
    ratio = 0
    for sid, s in enumerate(TOPICS_ARR):
      for tid, t in enumerate(s):
        sm.set_seq2(t)
        loop_ratio = sm.ratio()
        if loop_ratio > ratio:
          ratio = loop_ratio
          subj_id = sid
          topic_id = tid
    course['subject'] = SUBJECT_ARR[subj_id]
    course['topic'] = TOPICS_ARR[subj_id][topic_id]

    print course.get('title')
    print course.get('subject')
    print course.get('topic')
    print '\n'
    result_courses_arr.append(course)
  
  export_course(result_courses_arr)
