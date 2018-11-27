from ..models import Account
from ..models import Course
from ..models import Section
from ..models import CourseMember
from ..models import SectionMember
from .io_interface import IOInterface
import csv
# Database names can be:
# Account
# Course


class FileIO(IOInterface):

    # Read the file specified by database and search for the row that matches the key
    # Return that row or return None if no row matches
    def readData(self, key, database):
        try:
            current = None
            if database == "Account":
                current = Account.objects.get(pk=key)
            elif database == "Course":
                current = Course.objects.get(pk=key)
            elif database == "Section":
                current = Section.objects.get(pk=key)
            elif database == "CourseMember":
                current = CourseMember.objects.get(pk=key)
            elif database == "SectionMember":
                current = SectionMember.objects.get(pk=key)
            return current
        except (Account.DoesNotExist, Course.DoesNotExist, Section.DoesNotExist, CourseMember.DoesNotExist, SectionMember.DoesNotExist):
            # The primary key does not exist in the database, so return None
            return None

    # Read the file specified by filename to determine if the key is in the file.
    # If the key is found, then the entire line is overwritten with the current information passed in new_info.
    # If no key is found, new information is written to a new row at the bottom of the file.
    def writeData(self, key, filename, new_info):
        data_list = []
        line_number = 0
        with open(filename, newline='') as csv_i:
            data_reader = csv.reader(csv_i)
            data_list.extend(data_reader)
            for row in data_reader:
                if row[0] == key:
                    break
                line_number += 1
        if line_number < len(data_list):
            data_list[line_number] = new_info
        else:
            data_list.append(new_info)
        with open(filename, 'w', newline='') as csv_o:
            data_writer = csv.writer(csv_o)
            data_writer.writerows(data_list)
        """
        else:
            line_to_overwrite = {line_number: new_info}
            with open(filename, 'w', newline='') as csv_o:
                data_writer = csv.writer(csv_o)
                for line, row in enumerate(data_list):
                    print(line, row)
                    data = line_to_overwrite.get(line, row)
                    data_writer.writerow(data)
        """

    def deleteData(self, key, database):
        if database == "Account":
            current = Account.objects.get(pk=key)
            current.delete()
        elif database == "Course":
            current = Course.objects.get(pk=key)
            current.delete()


    def modifyData(self, key, position, newinfo, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
        file = open(filename, 'w')
        for line in lines:
            variableList = line.split(',')
            if variableList[0] != key:
                file.write(line)
            else:
                variableList[position] = newinfo

        file.close()
