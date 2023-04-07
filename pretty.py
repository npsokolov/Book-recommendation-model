import re


import httplib2


def cover_check(url):
    if "nophoto" in url:
        return 0
    else:
        return 1

def get_img(url, id, number):

    h = httplib2.Http('.cache')
    response, content = h.request(url)
    out = open("img_to_users\\" + str(id) + "_" + str(number) +".jpg", 'wb')
    out.write(content)
    out.close()

def get_books_info(user_id, book):
    answer_strings = []
    for i, el in enumerate(book):
        img_path = -1
        if (cover_check(el[1])):
            get_img(el[1], user_id, i)
            img_path = "img_to_users\\" + str(user_id) + "_" + str(i) +".jpg"
        answer_string = "Название: " + el[0] + "\nЖанр: " + el[2]

        answer_strings.append([answer_string, img_path])
    return answer_strings
