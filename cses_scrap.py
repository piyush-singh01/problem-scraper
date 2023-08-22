from bs4 import BeautifulSoup
import requests
import markdownify
import re
import sys
import os
import logging

def PrintCorrectUsage():
    print("Correct Usage:")
    print('python cses_scrap.py -d <Task Section>')
    print('python cses_scrap.py <Problem Link>')

def FetchProblem():
    if len(sys.argv) < 1:
        logging.info("Invalid Arguments Passed")
        PrintCorrectUsage()
        return
    
    problem_link = str(sys.argv[1])

    path = os.getcwd()

    problem_src = requests.get(problem_link).text
    problem_soup = BeautifulSoup(problem_src, 'lxml')
    title_block = BeautifulSoup(str(problem_soup.find('div', class_ = 'title-block')), 'lxml')
    problem_name = str(title_block.h1.text)
    
    problem_file_name = problem_name.replace(' ', '_')
    problem_file_name = problem_file_name.lower()
    problem_file_name += ".cpp"

    problem_path = os.path.join(path, problem_name)
    os.mkdir(problem_path)
    logging.info(f"Created directory for problem {problem_name}")


    readme_path = os.path.join(problem_path, 'README.md')
    f = open(readme_path, 'x')
    f.close()
    logging.info(f"README file created for problem {problem_name}")

    problem_file_path = os.path.join(problem_path, problem_file_name)
    f = open(problem_file_path, 'x')
    f.close()
    logging.info(f"Source File Created for problem {problem_name}")
    
    write_to_readme(readme_path, problem_soup)


def FetchDirectory():
    if(len(sys.argv) < 2):
        logging.info("Invalid Arguments Passed")
        PrintCorrectUsage()
        return

    algo_name = str(sys.argv[2])
    dir_name = algo_name
    path = os.getcwd()
    if not os.path.exists(os.path.join(path, dir_name)):
        os.mkdir(os.path.join(path, dir_name))
        logging.info(f"{dir_name} directory created, at {path} ...")
    else:
        logging.info(f"{dir_name} directory already exists")


    cses_source = requests.get('https://cses.fi/problemset/list/').text
    soup = BeautifulSoup(cses_source, 'lxml')
    
    found = False
    start = False
    for element in soup.find('div', class_ = 'content'):
        if(element.text == str(algo_name)):
            start = True
        if start:
            if element.name == "ul":
                soup2 = BeautifulSoup(str(element), 'lxml')
            if element.name == "h2":
                if found:
                    break
                found = True

    if start:
        path = os.path.join(path, algo_name)
        if not os.path.exists(path):
            os.mkdir(path)
            logging.info("Found, creating directory")
    else:
        logging.info("Not Found")
    

    tasks = []
    for element in soup2.find_all('a'):
        link = str("https://cses.fi" + element['href'])
        tasks.append(link)
    
    problem_count = 1
    for link in tasks:
        problem_src = requests.get(link).text
        problem_soup = BeautifulSoup(problem_src, 'lxml')
        title_block = BeautifulSoup(str(problem_soup.find('div', class_ = 'title-block')), 'lxml')
        problem_name = str(title_block.h1.text)
        
        problem_file_name = problem_name.replace(' ', '_')
        problem_file_name = problem_file_name.lower()
        problem_file_name += ".cpp"

        problem_count_str = str(problem_count)
        if problem_count <= 9:
            problem_count_str = '0' + problem_count_str
        problem_name = problem_count_str + ". " + problem_name
        problem_count += 1

        problem_path = os.path.join(path, problem_name)
        os.mkdir(problem_path)
        logging.info(f"Created directory for problem {problem_name}")


        readme_path = os.path.join(problem_path, 'README.md')
        f = open(readme_path, 'x')
        f.close()
        logging.info(f"README file created for problem {problem_name}")

        problem_file_path = os.path.join(problem_path, problem_file_name)
        f = open(problem_file_path, 'x')
        f.close()
        logging.info(f"Source File Created for problem {problem_name}")
        
        write_to_readme(readme_path, problem_soup)

def fix_file(path):
    res = []
    with open(path, 'r') as current:
        lines = current.readlines()
        start = False
        if not lines:
            logging.info("FILE IS EMPTY")
        else:
            for line in lines:
                line = line.strip()
                if re.search('[*] ', line):
                    line = "\n" + line + " "
                if line.find('\\_') != -1:
                    line = line.replace("\\_", "_")
                if line and line[0] == '`' and line[-1] == '`':
                    pass
                elif line and line[0] == '`':
                    line = line.replace('`', '```\n')
                    start = True
                elif line and line[-1] == '`':
                    line = line.replace('`', "\n```")
                    start = False
                if start:
                    if line:
                        line = line + '\n'
                        res.append(line)
                else:
                    if not line:
                        res.append('\n')
                    else:
                        res.append(line)
        current.close()
    
    with open(path, 'w') as current:
        current.writelines(res)
        current.close()

def write_to_readme(path, problem_soup):
    sourceFile = open(path, 'w+')
    html = problem_soup.prettify()
    h = markdownify.markdownify(html, heading_style = 'ATX')

    title_block = BeautifulSoup(str(problem_soup.find('div', class_ = 'title-block')), 'lxml')
    print("#", title_block.h1.text, file=sourceFile)
    content = BeautifulSoup(str(problem_soup.find('div', class_ = 'content')), 'lxml')

    try:
        content.script.decompose()
    except:
        pass
    try:
        content.title.decompose()
    except:
        pass

    print(markdownify.markdownify(content.prettify(), heading_style = 'ATX'), file=sourceFile)
    sourceFile.close()
    fix_file(path)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    
    directory_flag = False
    if str(sys.argv[1] == '-d' or sys.argv[1] == '--directory'):
        FetchDirectory()
    else:
        FetchProblem()