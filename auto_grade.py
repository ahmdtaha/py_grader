from csv import DictReader, DictWriter
import sys
import os
from os import listdir
from multiprocessing import Process
from os.path import isfile, join
import zipfile
import shutil
import importlib.util
import multiprocessing as mp

import config


class Grader:
    def __init__(self):
        pass

    def grade_student(self, test_name, current_submission_dir, q):

        # import public_tests as m
        try:
            sys.path.insert(0, current_submission_dir)
            spec = importlib.util.spec_from_file_location(test_name, join(current_submission_dir, test_name + '.py'))
            m = spec.loader.load_module(spec.name)
            # print(spec)

            # importlib.invalidate_caches()
            # importlib.reload(m)

            # import public_tests
            (total, fail, err) = m.run_tests()
            grade = (total - fail - err) * 5
            # sys.path.remove(current_submission_dir)
            shutil.rmtree(current_submission_dir)

            q.put(grade)
        except:
            print('Catching exception ------->')
            print("Unexpected error:", sys.exc_info())
            shutil.rmtree(current_submission_dir)
            q.put(0)

    def grade_submissions(self):
        all_students = list(DictReader(open(config.students_csv_file, 'r')))
        submissions_path =config.students_submission_dir
        base_current_submission_dir = join(submissions_path,'current_submission');
        gt_tests_path = config.test_files_dir
        test_name = config.test_files
        tests_path = ''

        grades_file = open(config.grade_write_file, config.grade_write_file_mode);
        o = DictWriter(grades_file, ["name", "grade"])
        o.writeheader()
        grades_file.flush()

        wrong_submission_files = open(config.wrong_submissions_log_file, config.wrong_submissions_log_file_mode)



        for idx , student in enumerate(all_students):

            current_submission_dir = base_current_submission_dir
            file_name = student['name'].replace(",","").replace(' ', '').strip().lower();
            onlyfiles = [f for f in listdir(submissions_path) if (isfile(join(submissions_path, f)) and f.startswith(file_name))]

            if(len(onlyfiles) != 1 or not onlyfiles[0].endswith('.zip')):
                if(len(onlyfiles) != 1):
                    print(idx,student['name'],' No Submission',file=wrong_submission_files)
                else:
                    print(idx,student['name'],' Wrong Submission',file=wrong_submission_files)
                d = {'name': student['name'], 'grade': 0}
                o.writerow(d)
                grades_file.flush()
                continue;


            zip_ref = zipfile.ZipFile(join(submissions_path,onlyfiles[0]), 'r')
            zip_ref.extractall(current_submission_dir)
            zip_ref.close()



            num_files = len([i for i in os.listdir(current_submission_dir) if os.path.isfile(join(current_submission_dir,i))])
            prefixes = ["project", "Project"]
            if(num_files == 0):
                sub_dir = [i for i in os.listdir(current_submission_dir) if (os.path.isdir(join(current_submission_dir,i)) and i.startswith(tuple(prefixes)) )]
                if(len(sub_dir) == 0):
                    print(idx,student['name'],' Something is wrong with',file=wrong_submission_files)
                    d = {'name': student['name'], 'grade': 0}
                    o.writerow(d)
                    grades_file.flush()
                    continue;

                tests_path = join(current_submission_dir,sub_dir[0])
                for i in os.listdir(tests_path):
                    if(os.path.isfile(join(tests_path,i))):
                        shutil.copyfile(join(tests_path,i), join(current_submission_dir,i))


            for i in os.listdir(gt_tests_path):
                shutil.copyfile(join(gt_tests_path,i), join(current_submission_dir,i))


            q = mp.Queue()
            p = mp.Process(target=grade_student, args=(student['name'],test_name,current_submission_dir,q))
            p.start()
            p.join()
            grade = q.get()
            print(idx, student['name'],'\t',grade)

            d = {'name': student['name'], 'grade': grade}
            o.writerow(d)
            grades_file.flush()
        

if __name__ == '__main__':
    Grader().grade_submissions();
        