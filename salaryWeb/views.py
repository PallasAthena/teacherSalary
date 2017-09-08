# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:02:54 2017

@author: biqiao
"""

from teacherSalary import salary

from django.shortcuts import render
from teacherSalary import settings
import os

CSV_FILE = os.path.join(settings.BASE_DIR, "teacherSalary", "out", "salary.csv")
HTML_FILE = os.path.join(settings.BASE_DIR, "teacherSalary", "out", "salary_table.html")


# Create your views here.
def index(request):
    return render(request, "index.html")


def count_salary(request):
    if request.method == 'POST':
        # form = forms.NameForm(request.POST)
        # if form.is_valid():
        #     dateFrom = form.clean_data["date_from"]
        #     dateTo = form.clean_data["date_to"]
        dateFrom = request.POST["date_from"] + ' 00:00:00'
        dateTo = request.POST["date_to"] + ' 00:00:00'
        salary.salary_sheet(dateFrom, dateTo, CSV_FILE, HTML_FILE)
        context = {'html_table': HTML_FILE}
        return render(request, "result.html", context)

