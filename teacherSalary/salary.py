#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:02:54 2017

@author: biqiao
"""


from .db import DB
from .countSalary import TeacherInfo, SalarySheet, AnswerSalary


       

def get_answers(date_from, date_to):

    get_answer_sql = '''
        SELECT 
        a.teacher_id, 
        a.teacher_rating, 
        g.grade_id, 
        a.FIXED_ANSWER_TIME, 
        a.answer_type 
        FROM 
        ozing_answer a, 
        ozing_grade g 
        WHERE 
        a.grade_id = g.grade_id 
        AND a.PREAPPOINTMENT_ID IS NULL 
        AND a.begin_time < a.end_time 
        AND (a.answer_time >= 30 
        OR a.fixed_answer_time >= 30) 
        AND a.teacher_rating > 2 
        AND a.date_added > "{}" 
        AND a.date_added < "{}" 
        AND a.TEACHER_ID IN (SELECT 
        teacher_id 
        FROM 
        ozing_teacher) 
        and (a.answer_type = 'free' or a.answer_type = 'charge')  limit 10
    '''.format(date_from, date_to)


    result = DB().select(get_answer_sql.replace('\n', ''))
    if result:
        answers = [list(item) for item in result]
        return answers
        

    
def salary_sheet(date_from, date_to, csv_file, html_file):
    answers = get_answers(date_from, date_to)
    answerSalary = AnswerSalary(answers)
    answerSalary.charged_answers_salary()
    answerSalary.free_answers_salary()
    all_answer_salary = answerSalary.charge_answers + answerSalary.free_answers
    
    teacher_ids = ','.join('{}'.format(item[0]) for item in answers)
    teacher_infos = TeacherInfo(teacher_ids).get_teacher_info()
    
    SalarySheet(all_answer_salary, teacher_infos, csv_file, html_file).salary_sheet()

    


        
       



