# Code created by Mark Tjoluskin
from tkinter import *
from datetime import datetime
import create_db

# making it a class allows data to be passed easily between
# objects
class QuizGUI():

    def __init__(self, title, geometry):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.create_main_options()



    def create_main_options(self):
        self.clear_widgets()
        self.modules = create_db.Module.show_modules()
        Label(self.root, text="QUIZ APPLICATION").pack()
        Label(self.root, text="PLEASE SELECT FUNCTION:").pack()
        Button(self.root, text="Update Modules", command=self.update_modules).pack()
        Button(self.root, text="Update Questions", command=self.update_questions).pack()
        Button(self.root, text="Run Quiz", command=self.new_quiz).pack()
        Button(self.root, text="Result Statistics", command=self.result_statistics).pack()
        Button(self.root, text="QUIT", command=self.quit).pack()

    def quit(self):
        self.root.destroy()
        sys.exit()

    def update_modules(self):
        self.clear_widgets()
        #self.modules = create_db.Module.show_modules()
        Label(self.root, text="UPDATE MODULES").pack()
        Label(self.root, text="PLEASE SELECT FUNCTION:").pack()
        Button(self.root, text="Create Module", command=self.create_module).pack()
        Button(self.root, text="Update Module", command=self.update_module).pack()
        Button(self.root, text="Delete Module", command=self.delete_module).pack()
        Button(self.root, text="MAIN MENU", command=self.create_main_options).pack()

    def create_module(self):
        self.clear_widgets()
        Label(self.root, text="CREATE MODULE").pack()
        Label(self.root, text="Enter Module Code Number:").pack()
        self.module_code_widget = Entry(self.root, width=10)
        self.module_code_widget.pack()
        Label(self.root, text="Enter Module Label:").pack()
        self.module_label_widget = Entry(self.root, width=20)
        self.module_label_widget.pack()
        Button(self.root, text="Click to Create Module", command=self.create_module_button).pack()

    def create_module_button(self):
        module_label = self.module_label_widget.get().strip()
        module_code = self.module_code_widget.get()
        if module_label and module_code:
            m = create_db.Module(int(module_code), module_label)
        self.create_main_options()

    def update_module(self):
        self.clear_widgets()
        Label(self.root, text="UPDATE MODULE").pack()
        Label(self.root, text="Select Module to Update:").pack()
        self.select_module(command_function=self.update_module_selected)

    def update_module_selected(self, *arg):
        tuple_in_str_form = self.modules_list_object.get()
        parts = tuple_in_str_form.split(",")
        self.module_code = int(parts[0][1:])
        Label(self.root,
              text="Enter New Module Label for Module "+str(self.module_code)+":"
              ).pack()
        self.module_label_widget = Entry(self.root, width=20)
        self.module_label_widget.pack()
        Button(self.root, text="Click to Update Module", command=self.update_module_button).pack()

    def update_module_button(self):
        module_label = self.module_label_widget.get()
        if module_label:
            sql = "UPDATE modules SET module_name = '" + module_label + "' WHERE module_code = " + str(
                self.module_code)
            with create_db.qb_conn:
                result = create_db.qb_conn.execute(sql)
        self.create_main_options()

    def delete_module(self):
        self.clear_widgets()
        Label(self.root, text="DELETE MODULE").pack()
        Label(self.root, text="Select Module to Delete:").pack()
        self.select_module(command_function=self.delete_module_selected)

    def delete_module_selected(self, *arg):
        tuple_in_str_form = self.modules_list_object.get()
        parts = tuple_in_str_form.split(",")
        module_code = int(parts[0][1:])
        #print(module_code)
        sql = "DELETE FROM modules WHERE module_code = " + str(module_code)
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        self.create_main_options()

    # this is not the function to update a question
    # but the menu for deleting, creating and updating individual questions
    def update_questions(self):
        self.clear_widgets()
        Label(self.root, text="Select Module to Update Questions for:").pack()
        self.select_module(command_function=self.question_module_selected)

    def question_module_selected(self, *arg):
        tuple_in_str_form = self.modules_list_object.get()
        parts = tuple_in_str_form.split(",")
        self.question_module_code = int(parts[0][1:])
        self.update_questions_menu()

    def update_questions_menu(self):
        self.clear_widgets()
        # make this available:
        self.qb = create_db.QuestionBank()
        self.qb.question_list = self.qb.get_questions(self.question_module_code)
        Label(self.root,
              text="UPDATE QUESTIONS FOR MODULE "+str(self.question_module_code)).pack()
        Label(self.root, text="PLEASE SELECT FUNCTION:").pack()
        Button(self.root, text="Create Question", command=self.create_question).pack()
        Button(self.root, text="Update Question", command=self.update_question).pack()
        Button(self.root, text="Delete Question", command=self.delete_question).pack()
        Button(self.root, text="MAIN MENU", command=self.create_main_options).pack()

    def create_question(self):
        self.clear_widgets()
        Label(self.root, text="CREATE QUESTION").pack()
        Label(self.root, text="Enter Question Type:").pack()
        question_type_options = ["BestMatch","TF","MCQ"]
        self.question_type_list_object = StringVar()
        self.question_type_list_object.set(question_type_options[0])
        self.question_type_list_object.trace('w', self.question_type_selected)
        self.question_type_dropdown = OptionMenu(self.root,
                                           self.question_type_list_object,
                                           *question_type_options)
        self.question_type_dropdown.pack()



    def question_type_selected(self, *arg):
        self.question_type = self.question_type_list_object.get()
        # all question types need a question
        Label(self.root, text="Enter Question:").pack()
        self.question_entry = Entry(self.root, width=30)
        self.question_entry.pack()
        #print(self.question_type)
        # bestmatch and MCQ both have multiple answers
        if self.question_type == "BestMatch" or self.question_type == "MCQ":
            Label(self.root, text="Enter Possible Answers, separated by commas:").pack()
            self.answers_entry = Entry(self.root, width=30)
            self.answers_entry.pack()
            Label(self.root,
                  text="Enter Commentary for Each Answer, separated by commas:").pack()
            self.answers_commentaries = Entry(self.root, width=50)
            self.answers_commentaries.pack()
        elif self.question_type == "TF":
            Label(self.root, text="Is Question True or False (Enter T or F)?").pack()
            self.true_or_false_entry = Entry(self.root, width=5)
            self.true_or_false_entry.pack()
            Label(self.root,
                  text="Enter Commentary for Answer:").pack()
            self.answers_commentaries = Entry(self.root, width=50)
            self.answers_commentaries.pack()
        if self.question_type == "MCQ":
            Label(self.root, text="Which of the answers is correct?").pack()
            self.answer_that_is_correct = Entry(self.root, width=5)
            self.answer_that_is_correct.pack()
        Label(self.root,
              text="Enter Mark for a Correct Answer:").pack()
        self.answer_mark = Entry(self.root, width=5)
        self.answer_mark.pack()
        Button(self.root, text="Press to Save Question",
               command=self.save_question).pack()


    def save_question(self):
        try:
            self.qb.delete_question(self.question)
        except:
            print("Creating, not updating question")
        new_question = None
        if self.question_type == "BestMatch":
            if self.question_entry.get() and \
                self.answers_entry.get().split(",") and \
                self.answers_commentaries.get().split(",") and \
                self.answer_mark.get() and \
                self.question_module_code:
                new_question = create_db.Question(self.question_entry.get(),
                                        self.answers_entry.get().split(","),
                                        self.answers_commentaries.get().split(","),
                                        int(self.answer_mark.get()),
                                        int(self.question_module_code))
        elif self.question_type == "MCQ":

            answers = self.answers_entry.get().split(",")
            try:
                correct_index = answers.index(
                    self.answer_that_is_correct.get().lower())
            except ValueError:
                # means there's a mismatch between questions and answers
                # e.g. user has entered a "correct answer that isn't in questions.
                correct_index = "" # ensure it fails below test
            if self.question_entry.get() and \
                answers and \
                correct_index and \
                self.answers_commentaries.get().split(",") and \
                self.answer_mark.get():
                new_question = create_db.QuestionMCQ(self.question_entry.get(),
                                        answers,
                                        correct_index,
                                        self.answers_commentaries.get().split(","),
                                        int(self.answer_mark.get()),
                                        int(self.question_module_code))
        elif self.question_type == "TF":
            if self.question_entry.get() and \
                self.true_or_false_entry.get() and \
                [self.answers_commentaries.get()] and \
                self.answer_mark.get():
                new_question = create_db.QuestionTF(self.question_entry.get(),
                                                    self.true_or_false_entry.get().lower(),
                                                    [self.answers_commentaries.get()],
                                                    int(self.answer_mark.get()),
                                                    int(self.question_module_code))
        else:
            print("Couldn't find the question type in save_question(self)")
        if new_question:
            sql = new_question.convert_to_sql_insert()
            with create_db.qb_conn:
                result = create_db.qb_conn.execute(sql)
        else:
            print("Not a valid question")
        self.update_questions_menu()

    # this is for updating a specific question (as opposed to the
    # general menu: update_questions(self)
    def update_question(self):
        self.clear_widgets()
        Label(self.root, text="UPDATE QUESTIONS").pack()
        self.select_question(command_result=self.update_question_selected)

    # this is used in updating a single question - to populate entry
    # box with original values
    def insert_original_values(self, original_values, entry_box):
        current_values = [c for c in original_values if c != None]
        entry_box.insert(0, ",".join(current_values))

    # The only difference between this and create is that it
    # populates the box with the original versions
    # and forces the question type to stay the same
    def update_question_selected(self, *args):
        question_in_str_form = self.question_list_object.get()
        # self.qb.question_list contains all questions for current module
        q = [q for q in self.qb.question_list if q.question == question_in_str_form[:-1]][0]
        self.question = q
        self.question_type = q.self_type_as_string()
        Label(self.root, text="Enter Question:").pack()
        self.question_entry = Entry(self.root, width=30)
        current_question = q.question+"?"
        # must send as list
        self.insert_original_values([current_question], self.question_entry)
        self.question_entry.pack()
        if self.question_type == "BestMatch" or self.question_type == "MCQ":
            Label(self.root, text="Enter Possible Answers, separated by commas:").pack()
            self.answers_entry = Entry(self.root, width=30)
            current_answers = q.answers
            self.insert_original_values(current_answers, self.answers_entry)
            self.answers_entry.pack()
            Label(self.root,
                  text="Enter Commentary for Each Answer, separated by commas:").pack()
            self.answers_commentaries = Entry(self.root, width=50)
            current_commentaries = q.answer_commentaries
            self.insert_original_values(current_commentaries,
                                        self.answers_commentaries)
            self.answers_commentaries.pack()
        elif self.question_type == "TF":
            Label(self.root, text="Is Question True or False (Enter T or F)?").pack()
            self.true_or_false_entry = Entry(self.root, width=5)
            current_answer = q.answers
            self.insert_original_values(current_answer,
                                        self.true_or_false_entry)
            self.true_or_false_entry.pack()
            Label(self.root,
                  text="Enter Commentary for Answer:").pack()
            self.answers_commentaries = Entry(self.root, width=50)
            current_commentaries = q.answer_commentaries
            self.insert_original_values(current_commentaries,
                                        self.answers_commentaries)
            self.answers_commentaries.pack()
        if self.question_type == "MCQ":
            Label(self.root, text="Which of the answers is correct?").pack()
            self.answer_that_is_correct = Entry(self.root, width=5)
            current_correct_index = q.correct_answer_index
            # have to send as list
            # note, have to pull out actual answer, not index
            self.insert_original_values([str(q.answers[current_correct_index])],
                                        self.answer_that_is_correct)
            self.answer_that_is_correct.pack()

        Label(self.root,
              text="Enter Mark for a Correct Answer:").pack()
        self.answer_mark = Entry(self.root, width=5)
        current_mark = q.mark
        # have to send as list
        self.insert_original_values([str(current_mark)],
                                    self.answer_mark)
        self.answer_mark.pack()
        Button(self.root, text="Press to Save Updated Question",
               command=self.save_question).pack()


    def select_question(self, command_result=None):
        if command_result == None:
            command_result = self.delete_question_selected
        self.question_text_list = []
        for q in self.qb.question_list:
            self.question_text_list.append(q.question + "?")
        if self.question_text_list:
            Label(self.root, text="Select Question:").pack()
            self.question_list_object = StringVar()
            self.question_list_object.set(self.question_text_list[0])
            self.question_list_object.trace('w', command_result)
            self.question_delete_dropdown = OptionMenu(self.root,
                                                       self.question_list_object,
                                                       *self.question_text_list)
            self.question_delete_dropdown.pack()
        else:
            Button(self.root, text="No Questions in this Module - Press Here", command=self.create_main_options).pack()


    def delete_question(self):
        self.clear_widgets()
        Label(self.root, text="DELETE QUESTIONS").pack()
        self.select_question()

    def delete_question_selected(self, *args):
        question_in_str_form = self.question_list_object.get()
        # remove the ? with [:-1]
        # assumes that question_text defines a question uniquely.
        # May be a limit of this implementation.
        sql = "DELETE from questions where question_text = '" + question_in_str_form[:-1] + "'"
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        self.update_questions_menu()

    def result_statistics(self):
        self.clear_widgets()
        Label(self.root, text="RESULT STATISTICS").pack()
        self.select_module(command_function=self.results_module_selected)

    def results_module_selected(self, *args):
        tuple_in_str_form = self.modules_list_object.get()
        parts = tuple_in_str_form.split(",")
        self.results_module_code = int(parts[0][1:])
        # need to generate:
        # an achievements report that displays: the number of times a quiz was taken for that module, the
        # average score achieved, and the lowest and highest score achieved;
        # - a question statistics report that the displays the most 2 questions repeated in the quizzes taken.

        sql = "SELECT count(module_code) FROM results where module_code = '" + str(self.results_module_code) + "'"
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        r = [r for r in result][0][0]
        if r == None:
            r = 0
        r = r // 5  # Since there are 5 entries for each test
        Label(self.root,
              text="Number of tests done on Module "+str(self.results_module_code) + ": " + str(r)).pack()
        self.num_tests_done = str(r)
        sql = "SELECT AVG(score) FROM results where module_code="+str(self.results_module_code)
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        r = [r for r in result][0][0]
        if r == None:
            r = 0
        # don't need to divide by 5 since is an average
        Label(self.root,
              text="Average Score for tests on Module "+str(self.results_module_code) + ": " + str(r)).pack()
        self.av_score = str(r)
        sql = """SELECT question, COUNT(question) AS 'question_freq' FROM results 
                WHERE module_code = """ + str(self.results_module_code) + """
                GROUP BY question
                ORDER BY `question_freq` DESC
                LIMIT 2 """
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        r = [r[0]+"?" for r in result]
        r = "\n".join(r)
        self.two_most_freq = str(r)
        Label(self.root,
              text="Two Most frequently repeated questions:\n" + str(r)).pack()
        Button(self.root, text="Save Report to File", command=self.report_to_file).pack()
        Button(self.root, text="Press to Return to Main Menu", command=self.create_main_options).pack()

    def report_to_file(self): #&&&
        filename = "quiz_report_"+datetime.now().strftime("%d_%m_%Y")+".txt"
        with open(filename, "w") as f:
            f.write("Module "+str(self.results_module_code)+"\n")
            f.write("Number of tests done: " + self.num_tests_done +"\n")
            f.write("Average Score for tests: "+self.av_score +"\n")
            f.write("Two Most frequently repeated questions:\n" +
                    self.two_most_freq + "\n")
            Label(self.root, text="Report saved: "+filename).pack()

    def select_module(self, command_function=None):
        if command_function == None:
            command_function = self.after_module_selected
        # get from database
        #self.modules = m
        module_options = create_db.Module.show_modules()
        if module_options:
            self.modules_list_object = StringVar()
            self.modules_list_object.set(module_options[0])
            self.modules_list_object.trace('w', command_function)
            self.modules_dropdown = OptionMenu(self.root,
                                               self.modules_list_object,
                                               *module_options)
            self.modules_dropdown.pack()
        else:
            Button(self.root, text="No Modules - Press Here", command=self.create_main_options).pack()


    def after_module_selected(self, *arg):
        self.clear_widgets()
        Label(self.root, text="PLEASE ANSWER QUESTIONS:").pack()
        tuple_in_str_form = self.modules_list_object.get()
        parts = tuple_in_str_form.split(",")
        module_code = int(parts[0][1:])
        self.module_code = module_code
        qb = create_db.QuestionBank()
        self.g5q = qb.get_5_questions(module_code)
        if len(self.g5q) == 0:
            Button(self.root, text="No questions for module, press to Exit",
                   command=self.create_main_options).pack()
            return False
        self.BestMatch_widgets = []
        self.widgets_list = []
        self.question_widgets = []
        self.TF_answers = []
        self.MCQ_answers = []
        for q in self.g5q:
            if q.self_type_as_string() == "BestMatch":
                widget1 = Label(self.root, text=q.question + "?")
                widget2 = Entry(self.root, width=20)
                widget1.pack()
                widget2.pack()
                self.BestMatch_widgets.append(widget2)
            elif q.self_type_as_string() == "TF":
                widget1 = Label(self.root, text=q.question + " - True or False?")
                TF_options = ["True", "False"]
                TF_list_object = StringVar()
                widget2 = OptionMenu(self.root,
                                                TF_list_object,
                                                *TF_options,
                                                command=self.TF_has_been_clicked)
                widget1.pack()
                widget2.pack()
            elif q.self_type_as_string() == "MCQ":
                widget1 = Label(self.root, text=q.question + "? Select one:")
                MCQ_options = []
                #print("----")
                for a in q.answers:
                    MCQ_options.append(a)
                MCQ_list_object = StringVar()
                widget2 = OptionMenu(self.root,
                                                MCQ_list_object,
                                                *MCQ_options,
                                                command=self.MCQ_has_been_clicked)
                widget1.pack()
                widget2.pack()
        self.submit_button = Button(self.root, text="Submit Answers", command=self.score_results)
        self.submit_button.pack()


    def score_results(self):
        self.submit_button.destroy()
        score = 0
        max_score = 0
        for i, q in enumerate(self.g5q):
            max_score += q.mark
            if q.self_type_as_string() == "BestMatch":
                if len(self.BestMatch_widgets) > 0:
                    Entry_widget = self.BestMatch_widgets.pop(0)
                    user_answer = Entry_widget.get()
                    if user_answer.lower().strip() in q.answers:
                        score += q.mark
                        #print("Correct answer for question ",i)
            elif q.self_type_as_string() == "TF":
                if len(self.TF_answers) > 0:
                    user_answer = self.TF_answers.pop(0)
                    if user_answer.lower().strip()[0] in q.answers:
                        score += q.mark
                        #print("Correct answer for question ", i)
            elif q.self_type_as_string() == "MCQ":
                if len(self.MCQ_answers) > 0:
                    user_answer = self.MCQ_answers.pop(0)
                    if user_answer.lower().strip() == q.answers[q.correct_answer_index]:
                        score +=  q.mark
                        #print("Correct answer for question ", i)
        Label(self.root, text="Your score is "+str(score)+" out of "+str(max_score)).pack()
        self.send_score_to_database(score)
        Button(self.root, text="Press for Next Test", command=self.new_quiz).pack()
        Button(self.root, text="Press to Quit Testing", command=self.create_main_options).pack()

    def send_score_to_database(self, score):
        # need to store data for:
        # an achievements report that displays: the number of times a quiz was taken for that module, the
        # average score achieved, and the lowest and highest score achieved;
        # - a question statistics report that the displays the most 2 questions repeated in the quizzes taken.
        # So store:
        # (1) The module a quiz was done on
        # (2) the score
        sql = "SELECT MAX(test_index) FROM results"
        with create_db.qb_conn:
            result = create_db.qb_conn.execute(sql)
        r = [r for r in result][0][0]
        if r == None:
            next_index = 0
        else:
            next_index = int(r)+1
        for q in self.g5q:
            sql = "INSERT INTO results (test_index,date,question,score, module_code) values "
            sql += "(" + str(next_index) + ","
            sql += "'" + datetime.now().strftime("%d/%m/%Y") + "',"
            sql += "'" + q.question + "',"
            sql += str(score) + ", " + str(self.module_code) + ")"
            with create_db.qb_conn:
                result = create_db.qb_conn.execute(sql)
            next_index += 1

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # note this triggers a new quiz
    # it calls select_module but doesn't include a
    # parameter in the call for what commmand to call after
    # module selcted. This is because the default for
    # self.select_module() is after_module_selected() which
    # is the function for running a new quiz.
    def new_quiz(self):
        self.clear_widgets()
        Label(self.root, text="Select Module to Quiz on:").pack()
        self.select_module()

    def TF_has_been_clicked(self, selection):
        self.TF_answers.append(selection)

    def MCQ_has_been_clicked(self, selection):
        self.MCQ_answers.append(selection)


RESET_TABLES = True
if RESET_TABLES:
    create_db.delete_tables()
    create_db.create_tables()

# TEST MODULES
m = create_db.Module(1765, 'COMP-1765')
m2 = create_db.Module(1811, 'COMP-1811')

# TEST QUESTIONS
qb = create_db.QuestionBank()
x1 = create_db.Question("What is 2+2?", ["4", "four"], ["numeric version best answer", "word is fine"],mark=5,module_code=1811)
x2 = create_db.QuestionMCQ("What is 2+2 equal to?", ["5", "2", "3", "4"], 3, ['too big',
                                                           'way too small',
                                                           'too small',
                                                           'just right!'], mark=4, module_code=1811)
x3 = create_db.QuestionTF("2+2 = 4", "t", mark=5, module_code=1811)
x4 = create_db.Question("What is 3+3?", ["6", "six"], ["numeric version best answer", "word is fine"],mark=6,module_code=1811)
x5 = create_db.QuestionMCQ("What is 3+3 equal to?", ["5", "2", "6", "4"], 2, ['too smallish',
                                                           'way too small',
                                                           'just right!',
                                                            'too small'], mark=7, module_code=1811)
x6 = create_db.QuestionTF("3*3 = 9", "f", mark=8, module_code=1811)
x7 = create_db.Question("What is 3+3?", ["6", "six"], ["numeric version best answer", "word is fine"],mark=6,module_code=1765)
x8 = create_db.QuestionMCQ("What is 3+3 equal to?", ["5", "2", "6", "4"], 2, ['too smallish',
                                                           'way too small',
                                                           'just right!',
                                                            'too small'], mark=7, module_code=1765)
x9 = create_db.QuestionTF("3+3 = 5", "f", mark=8, module_code=1765)
qb.add_question(x1)
qb.add_question(x2)
qb.add_question(x3)
qb.add_question(x4)
qb.add_question(x5)
qb.add_question(x6)
qb.add_question(x7)
qb.add_question(x8)
qb.add_question(x9)

quiz = QuizGUI("Quiz","500x400")
quiz.root.mainloop()