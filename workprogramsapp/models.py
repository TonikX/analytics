from django.db import models
from dataprocessing.models import Items
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class FieldOfStudyWorkProgram(models.Model):
    '''
    Модель для связи направления и рабочей программы
    '''
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    competence = models.ForeignKey('Competence', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('competence', 'work_program', 'field_of_study')


class WorkProgram(models.Model):
    '''
    Модель для рабочей программы
    '''
    prerequisites = models.ManyToManyField(Items, related_name='WorkProgramPrerequisites',
                                           through='PrerequisitesOfWorkProgram', blank=True, null=True)
    outcomes = models.ManyToManyField(Items, related_name='WorkProgramOutcomes', through='OutcomesOfWorkProgram',)
    title = models.CharField(max_length=1024)
    hoursFirstSemester = models.IntegerField(blank=True, null=True)
    hoursSecondSemester = models.IntegerField(blank=True, null=True)
    goals = models.CharField(max_length=1024)
    result_goals = models.CharField(max_length=1024)
    field_of_studies = models.ManyToManyField('FieldOfStudy', through=FieldOfStudyWorkProgram)

    def __str__(self):
        return self.title


class PrerequisitesOfWorkProgram(models.Model):
    '''
    Модель для пререквизитов рабочей программы
    '''
    # class Meta:
    #     auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE)
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1,
    )


class OutcomesOfWorkProgram(models.Model):
    '''
    Модель для результатов обучения по рабочей программе
    '''
    # class Meta:
    #     auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE)
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1,
    )

#
# class User(AbstractUser):
#     '''
#     Модель для пользователей
#     '''
#     first_name = models.CharField(max_length=1024)
#     last_name = models.CharField(max_length=1024)
#     patronymic = models.CharField(max_length=1024)
#     isu_number = models.CharField(max_length=1024)
#
#     def __str__(self):
#         return self.first_name + ' ' + self.last_name


class FieldOfStudy(models.Model):
    '''
    Модель для направлений
    '''
    PRIMARY_VOCATIONAL_EDUCATION = 'primary_vocational_education'
    SECONADARY_VOCATIONAL_EDUCATION = 'secondary_vocational_education'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    MASTER = 'master'
    QUALIFICATION_CHOICES = (
        (PRIMARY_VOCATIONAL_EDUCATION, 'Primary vocational education'),
        (SECONADARY_VOCATIONAL_EDUCATION, 'Secondary vocational education'),
        (BACHELOR, 'Bachelor'),
        (SPECIALIST, 'Specialist'),
        (MASTER, 'Master')
    )

    INTERNAL = 'internal'
    EXTRAMURAL = 'extramural'
    EDUCATION_FORM_CHOICES = (
        (INTERNAL, 'Internal'),
        (EXTRAMURAL, 'Extramural'),
    )
    number = models.CharField(unique=True, max_length=1024)
    qualification = models.CharField(choices=QUALIFICATION_CHOICES, max_length=1024)
    education_form = models.CharField(choices=EDUCATION_FORM_CHOICES, max_length=1024)

    def __str__(self):
        return self.number


class CompetenceIndicator(models.Model):
    '''
    Модель для связи компетенций и индикаторов
    '''
    competence = models.ForeignKey('Competence', on_delete=models.CASCADE)
    indicator = models.ForeignKey('Indicator', on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('competence', 'indicator', 'field_of_study')


class Competence(models.Model):
    '''
    Модель для компетенций
    '''
    number = models.CharField(unique=True, max_length=1024)
    name = models.CharField(unique=True, max_length=1024)
    field_of_study = models.ManyToManyField('FieldOfStudy')
    work_program = models.ManyToManyField('WorkProgram')
    indicators = models.ManyToManyField('Indicator', through=CompetenceIndicator)

    def __str__(self):
        return self.name


class IndicatorWorkProgram(models.Model):
    '''
    Модель для связи рабочих программ и индикаторов
    '''
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    indicator = models.ForeignKey('Indicator', on_delete=models.CASCADE)
    competence = models.ForeignKey('Competence', on_delete=models.CASCADE)
    knowledge = models.CharField(max_length=1024)
    skills = models.CharField(max_length=1024)
    proficiency = models.CharField(max_length=1024)

    class Meta:
        unique_together = ('competence', 'work_program', 'indicator')


class Indicator(models.Model):
    '''
    Модель для индикаторов
    '''
    number = models.CharField(unique=True, max_length=1024)
    name = models.CharField(max_length=1024)
    work_programs = models.ManyToManyField('WorkProgram', through=IndicatorWorkProgram)

    def __str__(self):
        return self.name


class EvaluationTool(models.Model):
    '''
    Модель для оценочных средств
    '''
    type = models.CharField(max_length=1024)
    name = models.CharField(unique=True, max_length=1024)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class DisciplineSection(models.Model):
    '''
    Модель для разделов дисциплин
    '''
    name = models.CharField(unique=True, max_length=1024)
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    evaluation_tools = models.ManyToManyField('EvaluationTool')

    def __str__(self):
        return self.name


class Topic(models.Model):
    '''
    Модель для темы
    '''
    discipline_section = models.ForeignKey('DisciplineSection', on_delete=models.CASCADE)
    number = models.CharField(unique=True, max_length=1024)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.number


class RouteComposition(models.Model):
    '''
    Модель для состава маршрутов (связь маршрутов и рабочих программ)
    '''
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('route', 'user', 'work_program', 'field_of_study')


class Route(models.Model):
    '''
    Модель для маршрутов
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    work_programs = models.ManyToManyField('WorkProgram', through=RouteComposition)
