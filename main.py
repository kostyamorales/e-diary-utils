from datacenter.models import Mark, Chastisement, Schoolkid, Commendation, Lesson
from random import choice
from sys import exit


def get_kid(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем')
        exit()
    except Schoolkid.DoesNotExist:
        print('Ученика с таким именем не существует')
        exit()
    return child


def fix_marks(schoolkid):
    kid = get_kid(schoolkid)
    bad_marks = Mark.objects.filter(schoolkid=kid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def delete_chastisements(schoolkid):
    kid = get_kid(schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid=kid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    kid = get_kid(schoolkid)
    lessons = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).order_by('-date')
    try:
        lesson = choice(lessons)
        praises = ['Молодец!', 'Отлично!', 'Хорошо!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!']
        Commendation.objects.create(text=choice(praises), schoolkid=kid,
                                    teacher=lesson.teacher, subject=lesson.subject,
                                    created=lesson.date)
    except IndexError:
        print('Название предмета введено не верно')
