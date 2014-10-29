#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of election-orchestra.
# Copyright (C) 2013  Eduardo Robles Elvira <edulix AT wadobo DOT com>

# election-orchestra is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# election-orchestra  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with election-orchestra.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import argparse
from frestq.fscheduler import FScheduler
from frestq.app import *
from frestq.utils import (list_messages, list_tasks, task_tree, show_task,
                    show_message, show_external_task, finish_task, get_tasks, get_external_task)
from frestq.models import Task

from prettytable import PrettyTable
import json

def print_task_list(tasks):
    table = PrettyTable(['small id', 'label', 'election', 'sender_url', 'created_date'])

    for task in tasks:
          election = task.input_data['Title']
          question = ''

          table.add_row([str(task.id)[:8], task.label, election, task.sender_url, task.created_date])

    print table

def print_task(task):
    table = PrettyTable(header=False)
    election = task.input_data['Title']
    if 'Question data' in task.input_data:
        question_data =  task.input_data['Question data']
        questions = ''
        for q in question_data:
            questions = questions + q['question'] + " "

    table.add_row(["small id", str(task.id)[:8]])
    table.add_row(["election", election])
    table.add_row(["label", task.label])

    if len(questions) > 0:
        table.add_row(["questions", questions.strip()])
    table.add_row(["sender_url",  task.sender_url])
    table.add_row(["created_date", task.created_date])

    print table

app.configure_app(config_object=__name__)

target_parser = argparse.ArgumentParser()
target_parser.add_argument("--tasks", help="list last tasks",
                    action="store_true")
target_parser.add_argument("--filters", nargs='+',
    help="filter items, with \"key=value\" ", default=[])
target_parser.add_argument("--tree",
                    help="prints the tree of related tasks")
target_parser.add_argument("--show-task", help="prints a task in detail")
target_parser.add_argument("--show-message", help="prints a task in detail")
target_parser.add_argument("--show-external", help="prints an external task details")
target_parser.add_argument("--finish", help="finish an external task",
                    nargs=2, default=None)
target_parser.add_argument("--with-parents",
                    help="show in the tree parent tasks too",
                    action="store_true")
target_parser.add_argument("-n", "--limit", help="limit number of results",
                    type=int, default=20)

# local parser
parser = argparse.ArgumentParser()
parser.add_argument("--list", help="list last tasks",
                    action="store_true")
parser.add_argument("--show", help="show task")
parser.add_argument("--show-full", help="show task detail")
parser.add_argument("--accept", help="accept task")
parser.add_argument("--reject", help="reject task")
pargs = parser.parse_args()

if pargs.list:
    target_pargs = target_parser.parse_args(["--tasks", "--filters", "task_type=external", "status=executing"])
    tasks = get_tasks(target_pargs)
    print_task_list(tasks)
elif pargs.show:
    target_pargs = target_parser.parse_args(["--show-external", pargs.show])
    tasks = get_external_task(target_pargs)
    if not tasks:
        print "task %s not found" % pargs.show
    else:
        task = tasks[0]
        print_task(task)
elif pargs.show_full:
    target_pargs = target_parser.parse_args(["--show-external", pargs.show_full])
    tasks = get_external_task(target_pargs)
    if not tasks:
        print "task %s not found" % pargs.show
    else:
        task = tasks[0]
        print(json.dumps(tasks[0].input_data, indent=4))
elif pargs.accept:
    target_pargs = target_parser.parse_args(["--finish", pargs.accept, '{"status": "accepted"}'])
    finish_task(target_pargs)
elif pargs.reject:
    target_pargs = target_parser.parse_args(["--finish", pargs.reject, '{"status": "denied"}'])
    finish_task(target_pargs)
else:
    parser.print_help()
