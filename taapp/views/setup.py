from .command import Command
from .login import Login
from .logout import Logout
from .create_account import CreateAccount
from .create_course import CreateCourse
from .delete_account import DeleteAccount
from .delete_course import DeleteCourse
from .view_account import ViewAccount
from .view_users import ViewUsers
from .view_course import ViewCourse
from .view_lecture import ViewLecture
from .view_lab import ViewLab
from .assign_instructor import AssignInstructor
from .assign_TA import AssignTA
from .assign_TA_toLab import AssignTAtoLab
from .edit_account import EditAccount
from .edit_account import ChangePassword
from .edit_account import EditAddress
from .edit_account import EditPhoneNumber
from .edit_account import EditEmail

# Use a global user variable to track who is logged in
current_user = None


def setupCommands():
    # Instantiate the command class and add all commands to it
    cmd = Command()
    login = Login()
    cmd.addCommand("login", login)
    logout = Logout()
    cmd.addCommand("logout", logout)
    createAccount = CreateAccount()
    cmd.addCommand("createAccount", createAccount)
    createCourse = CreateCourse()
    cmd.addCommand("createCourse", createCourse)
    deleteCourse = DeleteCourse()
    cmd.addCommand("deleteCourse", deleteCourse)
    deleteAccount = DeleteAccount()
    cmd.addCommand("deleteAccount", deleteAccount)
    viewAccount = ViewAccount()
    cmd.addCommand("viewAccount", viewAccount)
    viewUsers = ViewUsers()
    cmd.addCommand("viewUsers", viewUsers)
    viewCourse = ViewCourse()
    cmd.addCommand("viewCourse", viewCourse)
    viewLecture = ViewLecture()
    cmd.addCommand("viewLecture", viewLecture)
    viewLab = ViewLab()
    cmd.addCommand("viewLab", viewLab)
    assignInstructor = AssignInstructor()
    cmd.addCommand("assignInstructor", assignInstructor)
    assignTA = AssignTA()
    cmd.addCommand("assignTA", assignTA)
    assignTAtoLab = AssignTAtoLab()
    cmd.addCommand("assignTAtoLab", assignTAtoLab)
    editAccount = EditAccount()
    cmd.addCommand("editAccount", editAccount)
    changePassword = ChangePassword()
    cmd.addCommand("changePassword", changePassword)
    editAddress = EditAddress()
    cmd.addCommand("editAddress", editAddress)
    editPhoneNumber = EditPhoneNumber()
    cmd.addCommand("editPhoneNumber", editPhoneNumber)
    editEmail = EditEmail()
    cmd.addCommand("editEmail", editEmail)

    return cmd
