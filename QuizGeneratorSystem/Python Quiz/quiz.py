# Code created by Mark Tjoluskin
# base class is a basic text question with text answers
# this is essentially the BestFit type question
class Question:
    def __init__(self, question="?", answers=[], answer_commentaries=[], mark=0, module_code=0):
        # need to remove all commas, because they are used in GUI
        self.question = question.replace(","," ")
        # remove question mark to save space. Is added back later.
        self.strip_question_mark()
        self.answers = answers
        self.answer_commentaries = answer_commentaries
        self.module_code = module_code
        self.mark = mark
        if not self.answer_commentaries: # same as == []
            # creates an empty commentary list so
            # no error later
            self.answer_commentaries = [""]*len(self.answers)


    def strip_question_mark(self):
        # get rid of question mark to save space in db
        if self.question[-1] == "?":
            self.question = self.question[:-1]


    def self_type_as_string(self):
        if isinstance(self, QuestionMCQ):
            return "MCQ"
        if isinstance(self, QuestionTF):
            return "TF"
        return "BestMatch"

    @staticmethod
    def build_sql_list(sql1, sql2, list_to_add, table_column_stem):
        for i, list_item in enumerate(list_to_add):
            # note in objects things are numbered from 0
            # in db columns are numbered from 1, hence i+1
            sql1 += ", " + table_column_stem + str(i+1)
            sql2 += ", '" + list_item + "'"
        return sql1, sql2

    def sql_tail(self, sql1, sql2):
        sql1 += ", mark, module_code) "
        sql2 += ", " + str(self.mark) + ", " + str(self.module_code) + ")"
        sql = sql1 + sql2
        return sql

    def sql_top(self, top="INSERT INTO"):
        # base question
        sql1 = top + " questions (question_text, question_type"
        sql2 = "values ('" + self.question + "', '" + self.self_type_as_string() + "'"
        return sql1, sql2

    def convert_to_sql_insert(self):
        # base question
        sql1, sql2 = self.sql_top()
        # now things are done based on number of possible answers
        sql1, sql2 = self.build_sql_list(sql1, sql2,
                                         self.answers, "question_answer")
        sql1, sql2 = self.build_sql_list(sql1, sql2,
                                         self.answer_commentaries,
                                         "answer_commentary")
        return self.sql_tail(sql1, sql2)

    # receives a tuple which is a query result
    def init_from_query_result(self, query_result):
        self.module_code = query_result[19]
        self.mark = query_result[18]
        self.question = query_result[1]
        question_type = query_result[2]
        question_answers = query_result[3:8]
        question_corrects = query_result[8:13]
        question_commentaries = query_result[13:18]
        self.answers = []
        for qa in question_answers:
            if qa not in ["", None]:
                self.answers.append(qa)
        # only for MCQ
        if question_type == "MCQ":
            correct_index = 0
            for qcorrs in question_corrects:
                if qcorrs == "y":
                    self.correct_answer_index = correct_index
                    break
                correct_index += 1
        self.answer_commentaries = []
        for qcomms in question_commentaries:
            if qcomms not in ["", None]:
                self.answer_commentaries.append(qcomms)
        return self


    def __str__(self):
        ret_str = f"Text Question: {self.question}\nAnswers: {self.answers}\n"
        ret_str += f"Commentary: {self.answer_commentaries}\nMark: {self.mark}\n"
        ret_str += f"Module code: {self.module_code}"
        return ret_str


# inherits Question base class
# multiple choice question
class QuestionMCQ(Question):
    def __init__(self, question="?", answers=[], correct_answer_index=-1, answer_commentaries=[], mark=0, module_code=0):
        super().__init__(question, answers, answer_commentaries, mark, module_code)
        # answers is an array, and one has the correct answer
        # note this only asks one answer MC questions
        # but could be extended to answer multiple by
        # making correct_answer_index a list.
        self.correct_answer_index = correct_answer_index
        """if not self.answer_commentaries: # same as == []
            # creates an empty commentary list so
            # no error later
            self.answer_commentaries = [""]*len(self.answers)"""

    def convert_to_sql_insert(self):
        # override question
        sql1, sql2 = self.sql_top()
        # now things are done based on number of possible answers
        sql1, sql2 = self.build_sql_list(sql1, sql2,
                                         self.answers, "question_answer")
        # build a list that a 'y'for correct question
        # and a 'n for incorrect
        question_correct = ["n"]*len(self.answers)
        question_correct[self.correct_answer_index] = "y"
        sql1, sql2 = self.build_sql_list(sql1, sql2,
                                         question_correct, "question_correct")
        sql1, sql2 = self.build_sql_list(sql1, sql2,
                                         self.answer_commentaries,
                                         "answer_commentary")
        return self.sql_tail(sql1, sql2)

    def __str__(self):
        return f"MC Question: {self.question}\nChoices: {self.answers}\nCorrect answer index: {self.correct_answer_index}\nAnswer Commentaries: {self.answer_commentaries}\nMark: {self.mark}\nModule code: {self.module_code}"

# inherits Question base class
class QuestionTF(Question):
    def __init__(self, question="?", answers=["t"], answer_commentaries=[], mark=0, module_code=0):
        super().__init__(question, answers, answer_commentaries, mark, module_code)
        # just one answer in TF
        self.answer = answers[0] # only store t or f
        if self.answer.strip().lower() not in ["t", "f"]:
            raise ValueError("QuestionTF: Answer must be T or F")

    def __str__(self):
        return f"TF Question: {self.question}\nAnswer: {self.answer}\nAnswer Commentaries: {self.answer_commentaries}\nMark: {self.mark}\nModule code: {self.module_code}"
