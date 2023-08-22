from bs4 import BeautifulSoup
import requests
import markdownify
import re
import os
import sys
import logging

def parseSource(source):
    if source.find('problemset') == -1:
        contest_id_regex = r'[0-9]+'
        match = re.search(contest_id_regex, source)
        contest_id = source[match.start():match.end()]

        problem_regex = r'\/[a-zA-Z][0-9]*\b'
        problem_match = re.search(problem_regex, source)
        problem = source[problem_match.start() + 1: problem_match.end()]
        
        problem_source_link = "https://codeforces.com/problemset/problem/" + contest_id + "/" + problem
        return problem_source_link
    else:
        return source

def Main():
    source = str(sys.argv[1])

    source = parseSource(source)

    cf_source = requests.get(source).text
    # cf_source.encode('utf-16')
    soup = BeautifulSoup(cf_source, 'lxml')

    problem_id = re.search(r'/\d*/[A-Z]\d?$', source)
    problem_id = str(problem_id.group())
    problem_id = re.sub(r'/', '', problem_id)
    title = soup.find('div', class_='title').text
    title = re.sub(r'^[^\.]*\.\s', '', title)
    problem_name = (problem_id + ' ' + title)

    _path = os.path.join(os.getcwd(), problem_name)
    if not os.path.exists(_path):
        os.mkdir(_path)
        logging.info(f'Directory {problem_name} Created at {_path}')

    readme_path = os.path.join(_path, 'README.md')
    problem_path = os.path.join(_path, problem_name.lower().replace(' ', '_') + '.cpp')
    
    open(problem_path, 'w+')
    write_to_readme(readme_path, soup)


    
def write_to_readme(path, problem_soup):
    sourceFile = open(path, 'w+', encoding='utf-8')
    html = problem_soup.prettify()

    header_block = str(problem_soup.find('div', class_= 'header'))
    header_soup = BeautifulSoup(header_block, 'lxml')

    title = header_soup.find('div', class_='title').text
    print('#', title, file=sourceFile)

    time_limit = header_soup.find('div', class_='time-limit').find('div', class_='property-title').next_sibling.text
    memory_limit = header_soup.find('div', class_='memory-limit').find('div', class_='property-title').next_sibling.text
    rating = problem_soup.find('span', {'title':'Difficulty'})
    print('**Time Limit**: ', time_limit,'\\', file=sourceFile)
    print('**Memory Limit**: ', memory_limit, '\\', file=sourceFile)
    if rating:
        print('```', rating.text.strip()[1:], '```\n', file=sourceFile)
    else:
        print("", file=sourceFile)

    problem_statement = problem_soup.find('div', class_ = 'problem-statement')
    
    statement = list()
    for element in problem_statement:
        statement.append(element)

    problem = statement[1].find_all('p')    
    for child in problem:
        child_text = re.sub(r'\${3,}', r'$', child.text)
        print(child_text, '\n', file=sourceFile)

    print('### Input', file=sourceFile)
    
    input = statement[2].find_all('p')
    for idx, child in enumerate(input):
        child_text = re.sub(r'\${3,}', r'$', child.text)
        if idx != len(input) - 1:
            print(child_text, '\\', file=sourceFile)
        else:
            print(child_text, file=sourceFile)

    print('### Output', file=sourceFile)
    output = statement[3].find_all('p')
    for idx, child in enumerate(output):
        child_text = re.sub(r'\${3,}', r'$', child.text)
        if idx != len(output) - 1:
            print(child_text, '\\', file=sourceFile)
        else:
            print(child_text, file=sourceFile)


    print('### Sample Tests', file=sourceFile)
    for idx, samples in enumerate(problem_soup.find('div', class_ = 'sample-test').children):
        if idx % 2 == 0:
            print('#### Input', file=sourceFile)
            print('```', file=sourceFile)
            for lines in samples.find('pre'):
                print(lines.text, file=sourceFile)
            print('```', file=sourceFile)
        else:
            print('#### Output', file=sourceFile)
            print('```', file=sourceFile)
            for lines in samples.find('pre'):
                print(lines.text.strip(), file=sourceFile)
            print('```', file=sourceFile)

    print('### Note', file=sourceFile)
    note = problem_soup.find('div', class_='note').find_all('p')
    for child in note:
        child_text = re.sub(r'\${3,}', r'$', child.text)
        print(child_text, '\n', file=sourceFile)

    sourceFile.close()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    Main()