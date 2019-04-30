from django import forms

from apps.engineering.models import Project, ProjectFile, ProjectDesign, ProjectEquipment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner_name', 'owner_email', 'bidding', 'logistics_bidding', 'members', 'commissioned', 'slug')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        exclude = ('project', 'slug')

    def __init__(self, *args, **kwargs):
        super(ProjectFileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProjectDesignForm(forms.ModelForm):
    class Meta:
        model = ProjectDesign
        exclude = ('project', 'slug')

    def __init__(self, *args, **kwargs):
        super(ProjectDesignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProjectEquipmentForm(forms.ModelForm):
    class Meta:
        model = ProjectEquipment
        exclude = ('project', 'slug')

    def __init__(self, *args, **kwargs):
        super(ProjectEquipmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
