from django.shortcuts import render,redirect
from app01 import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets



class ClassForm(Form):
    title = fields.RegexField('全栈\d+')

def class_list(request):
    cls_list = models.Classes.objects.all()
    return render(request,'class_list.html',{'cls_list':cls_list})

def add_class(request):
    if request.method == "GET":
        obj = ClassForm()
        return render(request,'add_class.html',{'obj': obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            # obj.cleaned_data # 字典
            # 数据库创建一条数据
            # print(obj.cleaned_data)
            # models.Classes.objects.create(title=obj.cleaned_data['tt'])

            models.Classes.objects.create(**obj.cleaned_data)
            return redirect('/class_list/')
        return render(request,'add_class.html',{'obj': obj})

def edit_class(request,nid):
    if request.method == "GET":
        row = models.Classes.objects.filter(id=nid).first()
        # 让页面显示初始值
        # obj = ClassForm(data={'title': 'asdfasdfasdfas'})
        obj = ClassForm(initial={'title': row.title})
        return render(request,'edit_class.html',{'nid': nid,'obj':obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            models.Classes.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/class_list/')
        return render(request,'edit_class.html',{'nid': nid,'obj':obj})

class StudentForm(Form):
    name = fields.CharField(
        min_length=2,
        max_length=6,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    email = fields.EmailField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    age = fields.IntegerField(min_value=18,max_value=25,widget=widgets.TextInput(attrs={'class': 'form-control'}))
    cls_id = fields.IntegerField(
        # widget=widgets.Select(choices=[(1,'上海'),(2,'北京')])
        widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'),attrs={'class': 'form-control'})
    )

def student_list(request):

    stu_list = models.Student.objects.all()
    return render(request,'student_list.html',{'stu_list':stu_list})

def add_student(request):
    if request.method == "GET":
        obj = StudentForm()
        return render(request,'add_student.html',{'obj':obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            models.Student.objects.create(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'add_student.html',{'obj':obj})

def edit_student(request,nid):
    if request.method == "GET":
        row = models.Student.objects.filter(id=nid).values('name','email','age','cls_id').first()
        obj = StudentForm(initial=row)
        return render(request,'edit_student.html',{'nid':nid,'obj': obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            models.Student.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'edit_student.html',{'nid':nid,'obj': obj})






def teacher_list(request):
    tea_list = models.Teacher.objects.all()
    return render(request,'teacher_list.html',{'tea_list':tea_list})
from django.forms import models as form_model
class TeacherForm(Form):
    tname = fields.CharField(min_length=2)
    # xx = form_model.ModelMultipleChoiceField(queryset=models.Classes.objects.all())
    # xx = form_model.ModelChoiceField(queryset=models.Classes.objects.all())

    xx = fields.MultipleChoiceField(
        # choices=models.Classes.objects.values_list('id','title'),
        widget=widgets.SelectMultiple
    )
    def __init__(self,*args,**kwargs):
        super(TeacherForm,self).__init__(*args,**kwargs)
        self.fields['xx'].widget.choices = models.Classes.objects.values_list('id','title')

# obj = TeacherForm()
# 1. 找到所有字段
# 2. self.fields = {
#       tname: fields.CharField(min_length=2)
# }

def add_teacher(request):
    if request.method == "GET":
        obj = TeacherForm()
        return render(request,'add_teacher.html',{'obj':obj})
    else:
        obj = TeacherForm(request.POST)
        if obj.is_valid():
            xx = obj.cleaned_data.pop('xx')
            row = models.Teacher.objects.create(**obj.cleaned_data)
            row.c2t.add(*xx) # [1,2]
            return redirect('/teacher_list/')
        return render(request,'add_teacher.html',{'obj':obj})


def edit_teacher(request,nid):
    if request.method == "GET":
        row = models.Teacher.objects.filter(id=nid).first()
        class_ids = row.c2t.values_list('id')
        # print(class_ids)
        # id_list = []
        id_list = list(zip(*class_ids))[0] if list(zip(*class_ids)) else []
        # obj = TeacherForm(initial={'tname':row.tname,'xx':[1,2,3]})
        obj = TeacherForm(initial={'tname':row.tname,'xx':id_list})
        return render(request,'edit_teacher.html',{'obj':obj})
#
# class TestForm(Form):
#     t1 = fields.CharField(
#         widget=widgets.Textarea(attrs={})
#     )
#
#
#     t2 = fields.CharField(
#         widget=widgets.CheckboxInput
#     )
#
#     t3 = fields.MultipleChoiceField(
#         choices=[(1,'篮球'),(2,'足球'),(3,'溜溜球')],
#         widget=widgets.CheckboxSelectMultiple
#     )
#
#     t4 = fields.ChoiceField(
#         choices=[(1,'篮球'),(2,'足球'),(3,'溜溜球')],
#         widget=widgets.RadioSelect
#     )

    # t5 = fields.FileField(
    #     widget=widgets.FileInput
    # )


    # def clean_t1(self):
    #     pass
from django.core.exceptions import ValidationError
class TestForm(Form):
    user = fields.CharField(validators=[])
    pwd = fields.CharField()

    def clean_user(self):
        v = self.cleaned_data['user']
        if models.Student.objects.filter(name=v).count():
            raise ValidationError('用户名已经存在')
        return self.cleaned_data['user']

    def clean_pwd(self):
        return self.cleaned_data['pwd']

    def clean(self):
        # user = self.cleaned_data.get('user')
        # email = self.cleaned_data.get('email')
        # if models.Student.objects.filter(user=user,email=email).count():
        #     raise ValidationError('用户名和邮箱联合已经存在')
        return self.cleaned_data

    # def _post_clean(self):
    #     """
    #     An internal hook for performing additional cleaning after form cleaning
    #     is complete. Used for model validation in model forms.
    #     """
    #     pass
def test(request):
    obj = TestForm(initial={'t3':[2,3]})
    obj.is_valid()
    return render(request,'test.html',{'obj':obj})