# -*- coding: utf-8 -*-
import re
from pysbd.abbreviation_replacer import AbbreviationReplacer
from pysbd.between_punctuation import BetweenPunctuation
from pysbd.lang.common import Common, Standard
from pysbd.processor import Processor
from pysbd.utils import Text
from pysbd.punctuation_replacer import replace_punctuation
from pysbd.lists_item_replacer import ListItemReplacer


class Croatian(Common, Standard):

    iso_code = 'hr'

    class ListItemReplacer(ListItemReplacer):

        def add_line_break(self):
            # We've found alphabetical lists are causing a lot of problems with abbreviations
            # with multiple periods and spaces, such as 'Company name s. r. o.'. Disabling
            # alphabetical list parsing seems like a reasonable tradeoff.

            # self.format_alphabetical_lists()
            self.format_roman_numeral_lists()
            self.format_numbered_list_with_periods()
            self.format_numbered_list_with_parens()
            return self.text

    class Processor(Processor):

        def __init__(self, text, lang, char_span=False):
            super().__init__(text, lang, char_span)

        def process(self):
            if not self.text:
                return self.text
            self.text = self.text.replace('\n', '\r')

            # Here we use language specific ListItemReplacer:
            li = self.lang.ListItemReplacer(self.text)
            self.text = li.add_line_break()

            self.replace_abbreviations()
            self.replace_numbers()
            self.replace_continuous_punctuation()
            self.replace_periods_before_numeric_references()
            self.text = Text(self.text).apply(
                self.lang.Abbreviation.WithMultiplePeriodsAndEmailRule,
                self.lang.GeoLocationRule, self.lang.FileFormatRule)
            postprocessed_sents = self.split_into_segments()
            return postprocessed_sents

        def replace_numbers(self):
            self.text = Text(self.text).apply(*self.lang.Numbers.All)
            self.replace_period_in_slovak_dates()
            self.replace_period_in_ordinal_numerals()
            self.replace_period_in_roman_numerals()
            return self.text

        def replace_period_in_ordinal_numerals(self):
            # Rubular: https://rubular.com/r/0HkmvzMGTqgWs6
            self.text = re.sub(r'(?<=\d)\.(?=\s*[a-z]+)', '∯', self.text)

        def replace_period_in_roman_numerals(self):
            # Rubular: https://rubular.com/r/XlzTIi7aBRThSl
            self.text = re.sub(r'((\s+[VXI]+)|(^[VXI]+))(\.)(?=\s+)', r'\1∯', self.text, re.IGNORECASE)

        def replace_period_in_slovak_dates(self):
            MONTHS = [
                'Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj', 'Lipanj', 'Srpanj',
                'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac',
                'Siječnja', 'Veljače', 'Ožujka', 'Travnja', 'Svibnja', 'Lipnja', 'Srpnja',
            ]
            for month in MONTHS:
                # Rubular: https://rubular.com/r/dGLZqsbjcdJvCd
                self.text = re.sub(r'(?<=\d)\.(?=\s*{month})'.format(month=month), '∯', self.text)
