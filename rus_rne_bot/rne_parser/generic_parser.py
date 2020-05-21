import requests
from .helper import baseurl
from .form import form
from bs4 import BeautifulSoup


class GenParser:
    form_key = "prob"

    def __init__(self):
        self.session = requests.session()
        self.session.get(baseurl)

    def parse_problem(self, problem_id):
        return None
    
    def parse(self, quantity):
        if quantity > 25:
            raise ParserException("cant parse more than 25 problems")

        rform = form.copy()
        rform[self.form_key] = str(quantity * 4)
        r = self.session.post(baseurl + 'test?a=generate', data=rform)
        html = BeautifulSoup(r.text, 'html.parser')
        ids = list(map(lambda x: int(x.find('a')['href'].split('=')[-1]), html.find_all('span', attrs={'class': 'prob_nums'})))
        count = 0
        res = []

        for i in ids:
            problem = self.parse_problem(i)
            if problem is None:
                continue
            count += 1
            res.append(problem)
            if count == quantity:
                break
        
        return res
    