from django import forms

from .models import WorkProgram, OutcomesOfWorkProgram, PrerequisitesOfWorkProgram, EvaluationTool


class WorkProgramOutcomesPrerequisites(forms.ModelForm):
    
    class Meta:
        model = WorkProgram
        fields = ('id', 'title', 'hoursFirstSemester', 'hoursSecondSemester', 'prerequisites', 'outcomes' )
        #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['hoursFirstSemester'].label = "Количество часов в 1 семестре"
        self.fields['hoursSecondSemester'].label = "Количество часов во 2 семестре" 
        self.fields['prerequisites'].label = "Пререквизиты" 
        self.fields['outcomes'].label = "Постреквизиты"   
        self.fields['prerequisites'].widget.attrs.update({'class': 'selectpicker','data-live-search':'true'})    
        self.fields['outcomes'].widget.attrs.update({'class': 'selectpicker','data-live-search':'true'})    

    

class PrerequisitesOfWorkProgramForm(forms.ModelForm):

    class Meta:
        model = WorkProgram
        #fields = ('id', 'prerequisites', 'outcomes', 'title')
        fields = '__all__'
        
        
class EvaluationToolForm(forms.ModelForm):

    class Meta:
        model = EvaluationTool
        fields = '__all__'        
        

