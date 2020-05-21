from .helper import *
from . import Problem
from . import GenParser
from bs4 import BeautifulSoup


class Rus4(GenParser):
    form_key = "prob4"

    def parse_problem(self, problem_id):
        try:
            r = self.session.get(baseurl + 'problem?id={}'.format(problem_id))
            html = BeautifulSoup(r.text, 'html.parser')
            blocks = html.find('div', attrs={'class': 'prob_maindiv'}).find_all('div')
            # print(blocks[1])
            question_ps = blocks[1].find('p').find_all('p')
            # print(question_ps)
            question = blocks[1].find('p').contents[0].strip()
            # print(question)
            options = get_options(question_ps[-5])
            # print(options)
            answer = html.find('div', attrs={'class': 'answer'}).find('span').get_text().split(':')[-1].strip()
            # print(answer)
            answer_id = list(map(lambda x: x.lower().split()[0], options)).index(answer)
            return Problem(question, options, answer_id)
        except (BaseException):
            return None
    