from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', type = str, help = 'Enter group')
    parser.add_argument('--date', type = str, help = 'Enter date')
    args = parser.parse_args()
    addr = 'https://ruz.spbstu.ru/'
    page = requests.get(addr + 'search/groups', params={
        'q': '48'
    })
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        page_h = soup.find_all('a', class_ = 'groups-list__link')
        group_code = []
        for item in page_h:
            if item.text == args.group:
                item_url = item.get('href')
                group_code = item_url[-5:-1:1]
                group_code += item_url[-1]
        addr_gr = 'https://ruz.spbstu.ru/faculty/122/groups/' + group_code
        schedule = requests.get(addr_gr, params ={
            'date': args.date
        })
        soup = BeautifulSoup(schedule.text, 'lxml')
        week = soup.find('h3', class_ = 'page__h3')
        print(week.text)
        mn = tsd = wdn = th = fr = st = 0
        schedule_lessons = soup.find_all('li', class_ = 'schedule__day')
        for i in schedule_lessons:
            date = i.find('div', class_='schedule__date')
            print(date.text)
            lessons = i.find_all('li', class_='lesson')
            for j in lessons:
                if 'пн' in date.text:
                    mn += 1
                if 'вт' in date.text:
                    tsd += 1
                if 'ср' in date.text:
                    wdn += 1
                if 'чт' in date.text:
                    th += 1
                if 'пт' in date.text:
                    fr += 1
                if 'сб' in date.text:
                    st += 1
                lesson_name = j.find('div', class_='lesson__subject')
                print(lesson_name.text)
                lesson_type = j.find('div', class_ = 'lesson__type')
                print(lesson_type.text)
                try:
                    teacher = j.find('div', class_='lesson__teachers')
                    print(teacher.text.replace(' ', '', 1))
                except Exception:
                    print('У каждой группы свой преподаватель')
                place = j.find('div', class_='lesson__places')
                print(place.text.replace(', ', ',', 1))
            print('\n')
        x = np.array(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'])
        y = np.array([mn, tsd, wdn, th, fr, st])
        plt.bar(x, y, width=0.5)
        plt.ylabel("Кол-во пар")
        plt.xlabel("День недели")
        plt.title("Диаграмма расписания занятий")
        plt.show()
    else:
        print("Error", page.status_code)