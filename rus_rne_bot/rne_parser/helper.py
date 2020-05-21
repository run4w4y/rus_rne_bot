baseurl = 'https://rus-ege.sdamgia.ru/'

def get_options(p, acc=[]):
    f = p.find('p')
    option = p.contents[0].strip()
    if option == '': 
        return get_options(p.find_all('p')[1])
    if f is not None:
        return get_options(f, acc + [option])
    return acc + [option]