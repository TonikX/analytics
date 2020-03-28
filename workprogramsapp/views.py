from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views import View
from .models import WorkProgram, OutcomesOfWorkProgram, PrerequisitesOfWorkProgram, EvaluationTool, DisciplineSection, Topic
from .forms import WorkProgramOutcomesPrerequisites, PrerequisitesOfWorkProgramForm, EvaluationToolForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WorkProgramSerializer
from dataprocessing.models import Items

from dataprocessing.models import Items
import itertools
# Create your views here.


class WorkProgramsList(View):


    def get(self, request):

        workprograms = WorkProgram.objects.prefetch_related('outcomes', 'prerequisites')
        workprograms_outcomes = []
        workprograms_prerequisites = []

        for workprogram in workprograms:
            outcomes = [item.name for item in workprogram.outcomes.all()]
            outcomes_levels = OutcomesOfWorkProgram.objects.values_list('masterylevel').filter(workprogram=workprogram.pk)
            outcomes_levels2 = [entry for entry in outcomes_levels]
            outcomes_levels3 = []
            for outcome in outcomes:
                outcomes_levels3.append({'item': outcome, 'item_level': outcomes_levels2[outcomes.index(outcome)][0]})

            prerequisites = [item.name for item in workprogram.prerequisites.all()]
            prerequisites_levels2 = [entry for entry in PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
                workprogram=workprogram.pk)]
            prerequisites_levels3 = []
            for prerequisite in prerequisites:
                prerequisites_levels3.append({'item': prerequisite, 'item_level': prerequisites_levels2[prerequisites.index(prerequisite)][0]})
                workprograms_prerequisites.append({'title': workprogram.title, 'outcomes_levels': outcomes_levels3, })
            workprograms_outcomes.append({'pk': workprogram.pk, 'hoursFirstSemester': workprogram.hoursFirstSemester,
                                          'hoursSecondSemester': workprogram.hoursSecondSemester, 'title': workprogram.title, 'outcomes_levels': outcomes_levels3,
                                          'prerequisites_levels': prerequisites_levels3})

        return render(request, 'workprograms/workprograms.html', {'workprograms': workprograms_outcomes})


# Старая версия редактора рабочей программы
# class WorkProgramsPost(View):
#
#     def get(self, request):
#         form = WorkProgramOutcomesPrerequisites()
#         return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})
#
#     def post(self, request):
#         WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST)
#         if WorkProgramOP.is_valid():
#             WorkProgramOP.save()
#             return redirect('workprograms')
#         return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})

#
# class WorkProgramsList(View):
#
#
#     def get(self, request):
#
#         workprograms = WorkProgram.objects.prefetch_related('outcomes', 'prerequisites')
#         workprograms_outcomes = []
#         workprograms_prerequisites = []
#
#         for workprogram in workprograms:
#             outcomes = [item.name for item in workprogram.outcomes.all()]
#             outcomes_levels = OutcomesOfWorkProgram.objects.values_list('masterylevel').filter(workprogram=workprogram.pk)
#             outcomes_levels2 = [entry for entry in outcomes_levels]
#             outcomes_levels3 = []
#             for outcome in outcomes:
#                 outcomes_levels3.append({'item': outcome, 'item_level': outcomes_levels2[outcomes.index(outcome)][0]})
#
#             prerequisites = [item.name for item in workprogram.prerequisites.all()]
#             prerequisites_levels2 = [entry for entry in PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
#                 workprogram=workprogram.pk)]
#             prerequisites_levels3 = []
#             for prerequisite in prerequisites:
#                 prerequisites_levels3.append({'item': prerequisite, 'item_level': prerequisites_levels2[prerequisites.index(prerequisite)][0]})
#                 workprograms_prerequisites.append({'title': workprogram.title, 'outcomes_levels': outcomes_levels3, })
#             workprograms_outcomes.append({'pk': workprogram.pk, 'hoursFirstSemester': workprogram.hoursFirstSemester,
#                                           'hoursSecondSemester': workprogram.hoursSecondSemester, 'title': workprogram.title, 'outcomes_levels': outcomes_levels3,
#                                           'prerequisites_levels': prerequisites_levels3})
#
#         return render(request, 'workprograms/workprogram.html', {'workprograms': workprograms_outcomes})


class WorkProgramsPost(View):
    """
    Вторая версия редактора рабочих программ
    """
    def get(self, request):
        form = WorkProgramOutcomesPrerequisites()
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})

    def post(self, request):
        WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST)
        if WorkProgramOP.is_valid():
            WorkProgramOP.save()
            return redirect('workprograms')
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})


class WorkProgramView(View):

    """
    Вторая версия просмотра программ
    """

    def get(self, request, pk):

        thisworkprogram = WorkProgram.objects.filter(pk=pk).prefetch_related('outcomes', 'prerequisites')
        workprograms_outcomes = []
        workprograms_prerequisites = []
        prerequisites_of_workprogram = WorkProgram.objects.all()[0].prerequisites.all()
        # prerequisites_levels = PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
        #     workprogram=pk, item=prerequisites_of_workprogram[0].pk)
        prerequisites_and_levels =[]
        print (prerequisites_of_workprogram)
        prerequisites_levels = []
        prerequisites_levels2 = [entry for entry in prerequisites_levels]
        for prerequisite in prerequisites_of_workprogram:
            prerequisites_levels = PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
                workprogram=pk, item=prerequisite.pk)
            print (prerequisites_levels)
            prerequisites_and_levels.append({'item': prerequisite, 'item_level':  prerequisites_levels[0][0]})
        workprograms_outcomes.append({'pk': thisworkprogram[0].pk, 'hoursFirstSemester': thisworkprogram[0].hoursFirstSemester,
                                      'hoursSecondSemester': thisworkprogram[0].hoursSecondSemester, 'title': thisworkprogram[0].title,
                                      'prerequisites_levels': prerequisites_and_levels})


        #Работа над разделами и темами
        discipline_section_list = DisciplineSection.objects.filter(work_program_id=pk)
        discipline_topics_list =[]
        for discipline_section in discipline_section_list:
            print (discipline_section.pk)
            discipline_topics = Topic.objects.filter(discipline_section_id = discipline_section.pk)
            print (discipline_topics[0].discipline_section)
            print (discipline_section.name)
            print (discipline_section.work_program)
            discipline_topics_list.append(discipline_topics)
        print (discipline_topics_list)




        return render(request, 'workprograms/workprogram.html', {'workprograms': workprograms_outcomes, 'discipline_list': discipline_section_list,
                                                                 'discipline_topics_list': discipline_topics_list,})


class WorkProgramsPostUpdate(View):

    def get(self, request, pk):
        wp_obj = get_object_or_404(WorkProgram, id=pk)
        form = WorkProgramOutcomesPrerequisites(instance=wp_obj)
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})

    def post(self, request, pk):
        wp_obj = get_object_or_404(WorkProgram, id=pk)

        if request.method == "POST":
            WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST, instance=wp_obj)
            if WorkProgramOP.is_valid():
                WorkProgramOP.save()
                return redirect('workprograms')
        else:
            WorkProgramOP = WorkProgramOutcomesPrerequisites(instance=wp_obj)
        return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})


# class WorkPrograms(View):
#
#     def get(self, request, pk):
#
#         workprogram = WorkProgram.objects.prefetch_related('outcomes', 'prerequisites').filter(pk=pk)
#         workprogram_outcomes = []
#         workprogram_prerequisites = []
#
#         """данные о резальтатах"""
#         outcomes = [item.name for item in workprogram.outcomes.get(pk=pk)]
#         outcomes_levels = OutcomesOfWorkProgram.objects.values_list('masterylevel').filter(workprogram=workprogram.pk)
#         outcomes_levels2 = [entry for entry in outcomes_levels]
#         outcomes_levels3 = []
#         for outcome in outcomes:
#             outcomes_levels3.append({'item': outcome, 'item_level': outcomes_levels2[outcomes.index(outcome)][0]})
#         """данные о перерквизитах"""
#         prerequisites = [item.name for item in workprogram.prerequisites.all()]
#         prerequisites_levels2 = [entry for entry in PrerequisitesOfWorkProgram.objects.values_list('masterylevel').filter(
#             workprogram=workprogram.pk)]
#         prerequisites_levels3 = []
#         for prerequisite in prerequisites:
#             prerequisites_levels3.append({'item': prerequisite, 'item_level': prerequisites_levels2[prerequisites.index(prerequisite)][0]})
#             workprograms_prerequisites.append({'title': workprogram.title, 'outcomes_levels': outcomes_levels3, })
#         print(workprograms_outcomes)
#         workprograms_outcomes.append({'pk': workprogram.pk, 'hoursFirstSemester': workprogram.hoursFirstSemester,
#                                       'hoursSecondSemester': workprogram.hoursSecondSemester, 'title': workprogram.title, 'outcomes_levels': outcomes_levels3,
#                                       'prerequisites_levels': prerequisites_levels3})
#
#         return render(request, 'workprograms/workprograms.html', {'workprograms': workprograms_outcomes})
#
# # class PrerequisitesOfWorkProgram(View):
#
#     def get(self, request, pk):
#         wp_obj = get_object_or_404(PrerequisitesOfWorkProgram, workprogram=pk)
#         form = PrerequisitesOfWorkProgramForm(instance=wp_obj)
#         return render(request, 'workprograms/workprogram_edit.html', {'form': form})
#
#     def post(self, request):
#         WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST)
#         if WorkProgramOP.is_valid():
#             WorkProgramOP.save()
#             return redirect('workprograms')
#         return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})


class WorkProgramsListApi(APIView):
    """
    Список рабочих программ для апи.
    """
    def get(self, request, format=None):
        WorkPrograms = WorkProgram.objects.all()
        serializer = WorkProgramSerializer(WorkPrograms, many=True)
        return Response(serializer.data)

#
# class WorkProgramsEdit(View):
#
#     def get(self, request):
#         form = WorkProgramOutcomesPrerequisites()
#         return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': form})
#
#     def post(self, request):
#         WorkProgramOP = WorkProgramOutcomesPrerequisites(request.POST)
#         if WorkProgramOP.is_valid():
#             WorkProgramOP.save()
#             return redirect('workprograms')
#         return render(request, 'workprograms/WorkProgramOutcomesPrerequisitesEdit.html', {'form': WorkProgramOP})


# 
#EvaluationTool Views
#

class EvaluationToolList(View):

    def get(self, request):
        evaluation = EvaluationTool.objects.all()
        result = []
        for e in evaluation:
            sections = DisciplineSection.objects.filter(evaluation_tools = e)
            result.append({'pk': e.pk, 'type': e.type,
                                          'name': e.name, 'description': e.description, 'sections': sections})

        return render(request, 'workprograms/evaluation_list.html', {'evaluation': result})


class EvaluationToolPost(View):

    def get(self, request):
        form = EvaluationToolForm()
        return render(request, 'workprograms/EvaluationToolEdit.html', {'form': form})

    def post(self, request):
        evaluation = EvaluationToolForm(request.POST)
        if evaluation.is_valid():
            evaluation.save()
            return redirect('evaluation')
        return render(request, 'workprograms/EvaluationToolEdit.html', {'form': evaluation})

class EvaluationToolPostUpdate(View):

    def get(self, request, pk):
        et_obj = get_object_or_404(EvaluationTool, id=pk)
        form = EvaluationToolForm(instance=et_obj)
        return render(request, 'workprograms/EvaluationToolEdit.html', {'form': form})

    def post(self, request, pk):
        et_obj = get_object_or_404(EvaluationTool, id=pk)

        if request.method == "POST":
            evaluation = EvaluationToolForm(request.POST, instance=et_obj)
            if evaluation.is_valid():
                evaluation.save()
                return redirect('evaluation')
        else:
            evaluation = WorkProgramOutcomesPrerequisites(instance=et_obj)
        return render(request, 'workprograms/EvaluationToolEdit.html', {'form': evaluation})


