from collections import Counter
from scipy.stats import spearmanr
import pandas as pd
from matplotlib import pyplot as plt

COURSE_LIST = pd.read_csv('..\\Data\\unique_courses.csv')['courses']
STUDENT_ID_LIST = pd.read_csv('..\\Data\\unique_student_ids.csv')['student_id']
GRADES_LIST = pd.read_csv('..\\Data\\id_term_course_grade.csv')
GRADES_LIST[['student_id', 'term_number']] = GRADES_LIST[['student_id', 'term_number']].apply(pd.to_numeric)
STUDENT_GRADE_LIST = pd.read_csv('data\\student_grade_list.csv')
COURSE_COMBINATIONS = pd.read_csv('..\\Data\\course_combinations.csv')
FINAL_FILE = 'results\\final_correlations.csv'
GRAPHS_FOLDER = 'results\\graphs\\'
GRADE_SCALE = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
ALPHA_VALUE = 0.05
NUM_FINAL_COMBINATIONS = 15953
MIN_SAMPLES = 20



def fill():
    """
    For each row in the course combinations table, get class 1 and class 2. Create a temporary dataframe with the 2 classes
    as column names. For each student, search through the student grade list for the class names. If a student has grade
    entries for both classes, add them to the temporary dataframe. Once all students have been iterated through, calculate
    the Spearman rank-order correlation coefficient.
    """
    counter = 0
    final = pd.DataFrame(columns=['class_1', 'class_2', 'rho', 'pval', 'n'])
    for (class_1, class1_row_series) in COURSE_COMBINATIONS.iterrows():
        took_both_count = 0
        class_2 = COURSE_COMBINATIONS['class 2'].values[class_1]
        class_1 = COURSE_COMBINATIONS['class 1'].values[class_1]
        df = pd.DataFrame(columns=[class_1, class_2])  # temp dataframe with class1 and class2 as column headers
        for (student_id, student_row_series) in STUDENT_GRADE_LIST.iterrows():
            grade_class_1 = STUDENT_GRADE_LIST[class_1].values[student_id]
            grade_class_2 = STUDENT_GRADE_LIST[class_2].values[student_id]
            if isinstance(grade_class_1, str) and isinstance(grade_class_2, str):
                took_both_count += 1
                temp_df = pd.DataFrame(
                    data={class_1: [grade_class_1.split(',')[1]], class_2: [grade_class_2.split(',')[1]]})
                df = df.append(temp_df, ignore_index=True)
        rho, pval = spearmanr(df[class_1].values, df[class_2].values)
        temp_df = pd.DataFrame(
            data={'class_1': [class_1], 'class_2': [class_2], 'rho': [rho], 'pval': [pval], 'n': [took_both_count]})
        final = final.append(temp_df, ignore_index=True)

        print(counter)
        if counter % 1000 == 0:
            final.to_csv(FINAL_FILE, index=False)
        counter += 1
    final.to_csv(FINAL_FILE, index=False)


def generate_graphs(max_p_value, min_n_value):
    """
    Generate a bubble scatter plot of student grades for each course that meets the given criteria. Must already have
    generated the final dataset with Pearson's Correlation Coefficients, p-values, and n-values. Scatter plot bubbles
    are sized based on the frequency of the grade combination for the two courses graphed.
    :param max_p_value: Each course combination must have a p-value less than or equal to the given max p-value, given
    in the calling statement is the Bonferroni adjusted p-value.
    :param min_n_value: Each course combination must have a sample size no less than the given number
    :return:
    """
    final_read = pd.read_csv(FINAL_FILE)
    # for each course combination that is in your final results
    for (class_1, class1_row_series) in final_read.iterrows():
        p_value = final_read['pval'].values[class_1]
        class_2 = final_read['class_2'].values[class_1]
        class_1 = final_read['class_1'].values[class_1]
        # p value for each course combination must be less than or equal than Bonferonni adjusted p value
        if p_value <= max_p_value:
            df = pd.DataFrame(columns=[class_1, class_2])
            # for each student id in our grades list
            for (student_id, student_row_series) in STUDENT_GRADE_LIST.iterrows():
                grade_class_1 = STUDENT_GRADE_LIST[class_1].values[student_id]
                grade_class_2 = STUDENT_GRADE_LIST[class_2].values[student_id]
                # if a student's grade in class_1 and class_2 exists
                if isinstance(grade_class_1, str) and isinstance(grade_class_2, str):
                    # get numerical value (for graphing) of grade
                    grade_class_1 = convert_grade(grade_class_1.split(',')[1])
                    grade_class_2 = convert_grade(grade_class_2.split(',')[1])
                    temp_df = pd.DataFrame(data={class_1: [grade_class_1], class_2: [grade_class_2]})
                    df = df.append(temp_df, ignore_index=True)
            if len(df) >= min_n_value:
                # getting the bubble size based on frequency in set
                c = Counter(zip(df[class_1].values, df[class_2].values))
                s = [10 * c[(xx, yy)] for xx, yy in
                     zip(df[class_1].values, df[class_2].values)]  # https://stackoverflow.com/a/46700817
                plt.close()
                # force plot to have A-F axis labels
                plt.xlim(left=-0.5, right=10.5)
                plt.ylim(bottom=-0.5, top=10.5)
                plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                           ['F', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A'])
                plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                           ['F', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A'])
                plt.scatter(df[class_1].values, df[class_2].values, s=s)
                plt.xlabel(class_1)
                plt.ylabel(class_2)
                # save graph with a proper filename
                plt.savefig(
                    GRAPHS_FOLDER + "".join([c for c in class_1 if c.isalpha() or c.isdigit() or c == ' ']).rstrip() +
                    '_' + "".join([c for c in class_2 if
                                   c.isalpha() or c.isdigit() or c == ' ']).rstrip())  # https://stackoverflow.com/a/7406369


def convert_grade(string_grade):
    """
    Convert the letter grade to an arbitrary value between 0-10 inclusive in order to plot evenly. Encoded values are
    evenly spaced for graphing purposes only, these values should not be directly correlated to each grade in any other
    way.
    :param string_grade: the grade to encode
    :return: the encoded value for each grade
    """
# convert the letter grade to an arbitrary value between 0-10 inclusive in order to plot evenly.
def convert_grade(string_grade):
    if string_grade == 'A':
        return 10
    elif string_grade == 'A-':
        return 9
    elif string_grade == 'B+':
        return 8
    elif string_grade == 'B':
        return 7
    elif string_grade == 'B-':
        return 6
    elif string_grade == 'C+':
        return 5
    elif string_grade == 'C':
        return 4
    elif string_grade == 'C-':
        return 3
    elif string_grade == 'D+':
        return 2
    elif string_grade == 'D':
        return 1
    elif string_grade == 'F':
        return 0


if __name__ == "__main__":
    generate_graphs(ALPHA_VALUE / NUM_FINAL_COMBINATIONS, MIN_SAMPLES)
