from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Course
from ..models import Section


class CreateCourse(CmdInterface):
    def action(self, command_input):

        # Checks that there is user currently logged in
        if setup.current_user is None:
            return "Failed. No user currently logged in"

        # Checks that current user has permission to use command
        user_permissions = setup.current_user.permissions
        if user_permissions[0] == '0' and user_permissions[1] == '0':
            return "Failed. Restricted action"

        # Verify legal parameters
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)
        if not valid_params:
            return "Failed. Invalid parameters"

        file = FileIO()
        course_existence = file.readData(command_items[1], "Course")
        if course_existence is not None:
            return "Failed. Course already exists"

        # Save name of course to variable
        course_name = ""
        for word in command_items[4:]:
            course_name += word + " "

        ### We need to assign which database field is which input. like courseID=command_items[1]
        new_course = Course.objects.create(courseID=command_items[1], courseName=course_name, lectureSectionCount=int(command_items[2]), labSectionCount=int(command_items[3]))
        new_course.save()

        # Creating database lectures
        for i in range(int(command_items[2])):
            # create(sections uniqueID:lecture , section type:1 , parent course uniqueID)
            new_lecture = Section.objects.create(sectionID=((command_items[1]) + "-" + str(i)), sectionType=1, parentCourse=new_course)
            new_lecture.save()

        # Creating database labs
        for j in range(int(command_items[3])):
            new_lab = Section.objects.create(sectionID=((command_items[1]) + "-" + str(j+100)), sectionType=0, parentCourse=new_course)
            new_lab.save()

        return "Course " + course_name + " successfully added"

    def validateInputParameters(self, parameters):
        if len(parameters) < 4:
            return False

        # Need to check that the courseID is a 5 digit positive integer (> 99999)
        if int(parameters[1]) > 99999 or int(parameters[1]) < 0:
            return False

        # Checks validation of input parameters for number of lectures and labs
        if int(parameters[2]) < 1 or int(parameters[3]) < 0:
            return False

        return True
