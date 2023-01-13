from django.test import TestCase


class CompetenceTestCase(TestCase):

    def test_parce_competence(self):
        with open('fixture/competence.csv', 'r') as f:
            lines = f.readlines()
        header = lines[0].rstrip().split(';')
        for line in lines[1:]:
            records = line.split(';')
            employee = records[0]
            project = records[1]
            pm = records[2]
            for skill_index in range(3, len(records)):
                cell = records[skill_index].strip()
                if cell and len(cell) > 0 and cell != '0/0':
                    skill = header[skill_index]
                    cell_param = cell.split('/')
                    freq = cell_param[0]
                    level = cell_param[1]
                    print(f"{employee};{project};{pm};{skill};{freq};{level}")
