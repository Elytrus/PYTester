from collections import namedtuple

BeginEvent = namedtuple('BeginEvent', 'file_name case_cnt time_limit flags')
CaseTestedEvent = namedtuple('CaseTestedEvent', 'file_name results flags')
FinishEvent = namedtuple('FinishedEvent', 'file_name correct_count total_count meta flags')

VALID_EVENT_TYPES = (BeginEvent, CaseTestedEvent, FinishEvent)