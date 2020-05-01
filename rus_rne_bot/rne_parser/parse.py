from .form import form
import requests
from bs4 import BeautifulSoup
from .problem import Problem

url = 'https://rus-ege.sdamgia.ru/'
s = requests.session()


def get_options(p, acc=[]):
    f = p.find('p')
    option = p.contents[0].strip()
    if option == '': 
        return get_options(p.find_all('p')[1])
    if f is not None:
        return get_options(f, acc + [option])
    return acc + [option]

def parse_problem(problem_id):
    try:
        r = s.get(url + 'problem?id={}'.format(problem_id))
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

def parse():
    s.get(url)
    r = s.post(url + 'test?a=generate', data=form)
    html = BeautifulSoup(r.text, 'html.parser')
    ids = list(map(lambda x: int(x.find('a')['href'].split('=')[-1]), html.find_all('span', attrs={'class': 'prob_nums'})))
    count = 0
    res = []
    for i in ids:
        problem = parse_problem(i)
        if problem is None:
            continue
        count += 1
        res.append(problem)
        if count == 30:
            break
    return res
