import codecs
import os

from app.models import Project, Object, Var, UserKeywordSuite, UserKeyword, Suite, Case, Step


class Builder:
    def __init__(self, id):
        self.id = id
        #self.category = category
        self.root = os.getcwd()
        self.project_dir = 0
        self.build_no = 1
        self.project_name = ""
        self.task_dir = ""
        self.has_case = False

    def build(self):
        self.build_task()

        self.build_variables()

        self.build_suites()

    def build_task(self):

        project = Project.query.filter_by(id=self.id).first()
        if project:
            # self.suite = TestSuite(name=project.name, doc=project.desc)
            self.project_dir = self.root + '/logs/%d' % project.id
            self.project_dir = self.project_dir.replace("\\", "/")
            self.project_name = project.name

            if os.path.exists(self.project_dir) is False:
                os.makedirs(self.project_dir)
            L = []
            dirs = os.listdir(self.project_dir)

            for d in dirs:
                if d.isdigit():
                    L.append(int(d))

            L.sort()

            # 创建当前测试项目build no.
            self.build_no = 1
            if len(L) != 0:
                self.build_no = int(L[-1]) + 1

            task_dir = self.project_dir + "/%d" % self.build_no
            os.makedirs(task_dir)

    def build_variables(self):
        obj_dir = self.project_dir + "/%d" % self.build_no
        obj_dir = obj_dir.replace("\\", "/")
        resource_path = obj_dir + "/resource.txt"
        resource_path = resource_path.replace("\\", "/")
        # resource_file = codecs.open(resource_path, 'w', 'UTF-8')
        resource_file = codecs.open(resource_path, 'w', "utf-8")
        resource_file.write("*** Variables ***\n")
        objects = Object.query.filter_by(project_id=self.id).order_by(Object.id.asc()).all()
        for obj in objects:
            variables = Var.query.filter_by(object_id=obj.id).order_by(Var.id.asc()).all()
            for var in variables:
                resource_file.write("%s    %s\n" % (var.name, var.value))

            resource_file.write("\n\n")

        resource_file.write("*** Keywords ***\n")
        suites = UserKeywordSuite.query.filter_by(project_id=self.id).order_by(UserKeywordSuite.id.asc()).all()
        for suite in suites:
            keywords = UserKeyword.query.filter_by(keyword_suite_id=suite.id).order_by(
                UserKeyword.id.asc()).all()
            for key in keywords:
                resource_file.write("%s\n" % key.keyword)
                params = eval(key.params)
                for p in params:
                    resource_file.write("\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (p["param_1"], p["param_2"], p["param_3"],
                                                                            p["param_4"], p["param_5"], p["param_6"],
                                                                            p["param_7"]))

            resource_file.write("\n\n")

        resource_file.close()

    def build_suites(self):
        suite_dir = self.project_dir + "/%d" % self.build_no
        suite_dir = suite_dir.replace("\\", "/")
        # 截图目录
        images_dir = os.path.normpath(suite_dir + "/images")
        images_dir = images_dir.replace("\\", "/")
        if os.path.exists(images_dir) is False:
            os.makedirs(images_dir)

        case_path = suite_dir + "/testcase.robot"
        case_file = codecs.open(case_path, 'w', "utf-8")
        # case_file = codecs.open(case_path, 'w', 'UTF-8')

        # 写settings
        libs = ('Collections', 'DateTime', 'Screenshot',
                'Dialogs', 'OperatingSystem', 'Process',
                'String', 'Telnet', 'XML')

        case_file.write("*** Settings ***\n")
        for lib in libs:
            case_file.write("Library\t%s\n" % lib)

        project = Project.query.filter_by(id=self.id).first()
        auto_lib = {"web": 'SeleniumLibrary',
                    "app": 'AppiumLibrary',
                    "http": 'RequestsLibrary'}
        if project:
            case_file.write("Library\t%s\n" % auto_lib[project.category])

        case_file.write("\nResource\tresource.txt\n")
        case_file.write("\nSuite Setup  Screenshot.Set Screenshot Directory\t%s\n" % images_dir)
        if project.category == "web":
            case_file.write("\nSuite Teardown  SeleniumLibrary.Close All Browsers\n\n")
        if project.category == "app":
            case_file.write("\nSuite Teardown  AppiumLibrary.Close All Applications\n\n")

        case_file.write("*** Test Cases ***\n\n")
        suites = Suite.query.filter_by(project_id=self.id).order_by(Suite.id.asc()).all()
        for suite in suites:
            cases = Case.query.filter_by(suite_id=suite.id).order_by(Case.id.asc()).all()
            for case in cases:
                case_file.write("%d-%d %s.%s\n" % (suite.id, case.id, suite.name, case.name))
                steps = Step.query.filter_by(case_id=case.id).order_by(Step.id.asc()).all()
                for step in steps:
                    self.has_case = True
                    case_file.write("\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                        step.keyword,
                        step.param_1, step.param_2, step.param_3, step.param_4, step.param_5, step.param_6, step.param_7
                    ))

            case_file.write("\n\n")

        case_file.close()

    def has_test_case(self):

        return self.has_case
