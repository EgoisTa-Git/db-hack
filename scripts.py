import random

import django.core.exceptions

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject
from datacenter.models import Commendation

COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(child, subject_title):
    year_of_study = child.year_of_study
    group_letter = child.group_letter
    subject = Subject.objects.get(
        title=subject_title,
        year_of_study=year_of_study,
    )
    lessons = Lesson.objects.filter(
        year_of_study=year_of_study,
        group_letter=group_letter,
        subject=subject,
    ).order_by('-date')
    lesson = lessons[0]
    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=lesson.date,
        schoolkid=child,
        subject=subject,
        teacher=lesson.teacher,
    )


def become_excellent(
        child_name,
        subject_title='Математика',
        fix_marks_flag=False,
        remove_chastisements_flag=False,
        create_commendation_flag=False,
):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except django.core.exceptions.MultipleObjectsReturned:
        print('Найдено сразу несколько таких учеников. Завершение работы...')
        exit()
    except django.core.exceptions.ObjectDoesNotExist:
        print('Несуществующее имя! Завершение работы...')
        exit()
    if fix_marks_flag:
        fix_marks(child)
    if remove_chastisements_flag:
        remove_chastisements(child)
    if create_commendation_flag:
        try:
            create_commendation(child, subject_title)
        except django.core.exceptions.ObjectDoesNotExist:
            print('Неверно задан предмет! Завершение работы...')
            exit()


if __name__ == '__main__':
    become_excellent(
        child_name='Фролов Иван',
        subject_title='История',
        fix_marks_flag=True,
        remove_chastisements_flag=True,
        create_commendation_flag=True,
    )
