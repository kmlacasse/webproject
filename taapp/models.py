from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    permissions = models.CharField(max_length=4)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    officehours = models.CharField(max_length=100)
    #AS a ta or instructor, you can have a table with section members.
    sections = models.ManyToManyField('Section', through='SectionMember', related_name='sections')
    #As an instructor or TA you can have a table with course members
    courses = models.ManyToManyField('Course', through='CourseMember', related_name='courses')


class Course(models.Model):
    courseID = models.CharField(max_length=20, primary_key=True)
    courseName = models.CharField(max_length=50)
    lectureSectionCount = models.IntegerField()
    labSectionCount = models.IntegerField()

    #To get a list of sections for a course, sectionlist = Section.objects.filter(whichcourse='<unqiuecourse>')
    #Not needed because you can get this from account. instructors = models.ManyToManyField(Account)
    #Not needed because you can get this from account. tas = models.ManyToManyField(Account)


class Section(models.Model):
    sectionID = models.CharField(max_length=20, primary_key=True)
    sectionName = models.CharField(max_length=50)
    #Lab = 0, Lecture = 1
    sectionType = models.IntegerField()

    #formerly named whichcourse
    parentCourse = models.ForeignKey(Course, on_delete=models.CASCADE)


class CourseMember(models.Model):
    #To assign a course to an instructor or ta's list
    #john = Account.objects.create(username='ian')
    #cs351 = Course.objects.create(uniqueID=<somenumber> ...)
    #CourseMember.objects.create(account=john, course=<somenumber>)
    account = models.ForeignKey(Account, related_name='courselist', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, related_name='courselist', on_delete=models.SET_NULL, null=True)


class SectionMember(models.Model):
    #To assign a section to an instructor or ta's list
    #ian = Account.objects.create(username='ian'...)
    #section1 = Section.objects.create(courseid=<uniquecourseid>, sectionid=<uniquesectionid> ...)
    #SectionMember.objects.create(account=ian, section=section1)
    account = models.ForeignKey(Account, related_name='sectionlist', on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, related_name='sectionlist', on_delete=models.SET_NULL, null=True)
