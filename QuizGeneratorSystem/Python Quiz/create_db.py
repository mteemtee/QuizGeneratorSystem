# Code created by Mark Tjoluskin
from quiz import *
import sqlite3 as sl
qb_conn = sl.connect('question_bank.db')
from copy import copy #for testing
import random


#prints result of self.db(), one line per row, and ignoring "Nones"
def simple_print(result):
    for r in result:
        none_cleaned = [x for x in r if x is not None]
        print(none_cleaned)



class Module:
    def __init__(self, module_code, module_name):
        self.module_code = module_code
        self.module_name = module_name
        self.sql = "INSERT INTO modules (module_code, module_name) values "
        self.sql += "(" + str(self.module_code) + ", '" + str(self.module_name) + "')"
        self.db()

    def db(self, show=False):
        with qb_conn:
            if show:
                print(self.sql)
            result = qb_conn.execute(self.sql)
            return [r for r in result]

    @classmethod
    def show_modules(self):
        sql = "SELECT * FROM modules"
        with qb_conn:
            result = qb_conn.execute(sql)
            return [r for r in result]

    def update_module(self, new_module_name):
        self.module_name = new_module_name
        self.sql = "UPDATE modules SET module_name = '"+ self.module_name + "' WHERE module_code = " + str(self.module_code)
        return self.db() + self.show_modules() #returns the new set of rows. Python goes left to right

    def delete_module(self):
        self.sql = "DELETE FROM modules WHERE module_code = " + str(self.module_code)
        self.module_name = "DELETED_MODULE"
        return self.db() + self.show_modules()  #returns the new set of rows


class QuestionBank:
    def __init__(self):
        self.question_list = []
        self.sql = ""

    def db(self, show=False):
        with qb_conn:
            if show:
                print(self.sql)
            result = qb_conn.execute(self.sql)
            return [r for r in result]

    def add_question(self, question):
        """# question must be of type question
        question_type = question.self_type_as_string()"""
        self.question_list.append(question)
        self.sql = question.convert_to_sql_insert()
        return self.db() #+ self.get_questions()

    # a question is considered unique if it has the same question text
    # and question type.
    def delete_question(self, question):
        self.question_list.pop(self.question_list.index(question))
        self.sql = "DELETE from questions where question_text = '" + question.question + "' AND question_type = '" + question.self_type_as_string() + "'"
        return self.db()  # + self.get_questions()  #returns the new set of rows

    def get_questions(self, module_code=0, show=False):
        self.sql = "SELECT * from questions WHERE module_code=" + str(module_code)
        #return self.db(show = show)
        query_results = self.db(show=show)
        questions = []
        for qr in query_results:
            # convert row to a question object
            if qr[2] == "BestMatch":
                question = Question()
            elif qr[2] == "TF":
                question = QuestionTF()
            elif qr[2] == "MCQ":
                question = QuestionMCQ()
            else:
                print("No such Question Type!")
            questions.append(question.init_from_query_result(qr))
        return questions


    def get_5_questions(self, module_code):
        module_questions = self.get_questions(module_code=module_code)
        random.shuffle(module_questions)
        if len(module_questions) > 5:
            module_questions = module_questions[:5]
        # if it is a MCQ, shuffle the answers
        # but keep track of right answer
        resulting_questions = []
        for question in module_questions:
            if question.self_type_as_string() == "MCQ":
                # this will become a shuffled version of question
                new_question = copy(question)
                # get correct answer choice text
                correct_answer = new_question.answers[new_question.correct_answer_index]
                # shuffle answer choices list
                random.shuffle(new_question.answers)
                # set answer index to point at new index of correct answer choice
                # (assumes all answers are different)
                new_question.correct_answer_index = new_question.answers.index(correct_answer)
                question = new_question
            resulting_questions.append(question)
        return resulting_questions


def create_tables():
    # in case anything goes wrong, this context thing will clean up
    # afterwards
    with qb_conn:
        # can only execute one command at a time
        sql = """CREATE TABLE modules
                (module_code INTEGER NOT NULL PRIMARY KEY,
                module_name TEXT);
                """
        try:
            qb_conn.execute(sql)
        except sl.OperationalError:
            print("Couldn't create modules")  #table already there

        sql = """CREATE TABLE questions 
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                question_type TEXT,
                question_answer1 TEXT,
                question_answer2 TEXT,
                question_answer3 TEXT,
                question_answer4 TEXT,
                question_answer5 TEXT,
                question_correct1 TEXT,
                question_correct2 TEXT,
                question_correct3 TEXT,
                question_correct4 TEXT,
                question_correct5 TEXT,
                answer_commentary1 TEXT,
                answer_commentary2 TEXT,
                answer_commentary3 TEXT,
                answer_commentary4 TEXT,
                answer_commentary5 TEXT,
                mark INTEGER,
                module_code INTEGER,
                FOREIGN KEY(module_code) REFERENCES modules(module_code));"""
        try:
            qb_conn.execute(sql)
        except sl.OperationalError:
            print("Couldn't create questions") # table already there
        # can only execute one command at a time
        sql = """CREATE TABLE results
                (test_index INTEGER NOT NULL PRIMARY KEY,
                date TEXT,
                question TEXT,
                score INTEGER,
                module_code INTEGER,
                FOREIGN KEY(module_code) REFERENCES modules(module_code));"""
        try:
            qb_conn.execute(sql)
        except sl.OperationalError:
            print("Couldn't create results")  #table already there

def delete_tables():
    # in case anything goes wrong, this context thingy will clean up
    # afterwards
    with qb_conn:
        # can only execute one command at a time
        sql = "DROP TABLE modules"
        try:
            qb_conn.execute(sql)
        except:
            print("Couldn't execute ",sql)
        sql= "DROP TABLE questions"
        try:
            qb_conn.execute(sql)
        except:
            print("Couldn't execute ",sql)
        sql = "DROP TABLE results"
        try:
            qb_conn.execute(sql)
        except:
            print("Couldn't execute ", sql)

def display_table(table_name):
    with qb_conn:
        rows = qb_conn.execute("SELECT * FROM "+table_name)
        for row in rows:
            print(row)

