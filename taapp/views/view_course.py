from . import setup
from .cmd_interface import CmdInterface
from .file_io import FileIO
from ..models import Course


class ViewCourse(CmdInterface):
    def action(self, command_input):
        # Checks that there is user currently logged in
        if setup.current_user is None:
            return "Failed. No user currently logged in"

        # Shouldnt need to check the permission: should be accessible to everyone

        # Verify legal parameters
        command_items = command_input.split()
        valid_params = self.validateInputParameters(command_items)
        if not valid_params:
            return "Failed. Invalid parameters"

        # Check for course existence
        file = FileIO()
        course_item = file.readData(command_items[1], "Course")
        if course_item is None:
            return "Failed. Course does not exists"

        # Print out course information

        ret_str = "Course ID: " + course_item.courseID + '<br>' + "Name: " + course_item.courseName + '<br>' + "# of Lectures: " \
                  + str(course_item.lectureSectionCount) + '<br>' + "# of Labs: " + str(course_item.labSectionCount)
        return ret_str


    def validateInputParameters(self, parameters):
        # Need to check that the courseID is a 5 digit positive integer (> 99999)
        if len(parameters) != 2:
            return False

        return True
