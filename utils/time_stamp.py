from django.db.models import (
    Model, 
    DateTimeField,
    Sum,
    Avg,
    Count,
)

from django.db.models.functions import (
    ExtractYear,
    ExtractQuarter,
    ExtractMonth,
    ExtractWeek,
    ExtractDay,
    ExtractHour,
)


class TimeStampModel(Model):
    created_datetime = DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class AggByDateTime:
    """
    Assignee : 김수빈
    Reviewer : -\n
    `column_name`은 집계하고자 하는 칼럼명\n
    `datetime_col`은 기준이 될 날짜/시간 칼럼명\n
    `annotate_func`는 "SUM", "AVG", "COUNT" 중에서 작성해야 함.\n
    `timeunit`은 "YEAR", "QUARTER", "MONTH", "WEEK", "DAY", "HOUR" 중에서 작성해야 함.
    """
    def __init__(
        self, 
        column_name: str,
        datetime_col: str,
        annotate_func: str, 
        timeunit: str,
        ):
        assert annotate_func.upper() in ["SUM", "AVG", "COUNT"]
        assert timeunit.upper() in ["YEAR", "QUARTER", "MONTH", "WEEK", "DAY", "HOUR"]
        self.aggregate_dict = self.set_annotate_dict(column_name)
        self.extract_time_dict = self.set_extract_dict(datetime_col)
        self.annotate_options = self.get_annotate_options(column_name, annotate_func, timeunit)
        self.cls_name = f'{column_name.lower()}_by_{timeunit.lower()}(agg: {annotate_func.lower()})'

    def __str__(self):
        return self.cls_name

    def set_extract_dict(self, datetime_column_name: str):
        extract_time_dict = {
            'YEAR': ExtractYear(datetime_column_name),
            'QUARTER': ExtractQuarter(datetime_column_name),
            'MONTH': ExtractMonth(datetime_column_name),
            'WEEK': ExtractWeek(datetime_column_name),
            'DAY': ExtractDay(datetime_column_name),
            'HOUR': ExtractHour(datetime_column_name),
        }
        return extract_time_dict

    def set_annotate_dict(self, target_column_name: str):
        aggregate_dict = {
            'SUM': Sum(target_column_name),
            'AVG': Avg(target_column_name),
            'COUNT': Count(target_column_name),
        }
        return aggregate_dict

    def get_annotate_options(self, target_column_name: str, annotate_func: str, timeunit: str):
        annotate_options = {
            f'{target_column_name.lower()}({annotate_func.lower()})': self.aggregate_dict.get(annotate_func.upper()),
            timeunit.lower(): self.extract_time_dict.get(timeunit.upper())
        }
        return annotate_options
