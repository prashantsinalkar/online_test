from __future__ import unicode_literals
import unittest
import os
import shutil
import tempfile
from textwrap import dedent

# Local Import
from yaksh import grader as gd
from yaksh.grader import Grader
from yaksh.java_code_evaluator import JavaCodeEvaluator
from yaksh.java_stdio_evaluator import JavaStdIOEvaluator
from yaksh.evaluator_tests.test_python_evaluation import EvaluatorBaseTest


class JavaAssertionEvaluationTestCases(EvaluatorBaseTest):
    def setUp(self):
        with open('/tmp/test.txt', 'wb') as f:
            f.write('2'.encode('ascii'))
        tmp_in_dir_path = tempfile.mkdtemp()
        self.test_case_data = [
            {"test_case": "java_files/main_square.java",
            "test_case_type": "standardtestcase",
            "weight": 0.0
            }
        ]
        self.in_dir = tmp_in_dir_path
        self.file_paths = None
        gd.SERVER_TIMEOUT = 9
        self.timeout_msg = ("Code took more than {0} seconds to run. "
            "You probably have an infinite loop in"
            " your code.").format(gd.SERVER_TIMEOUT)


    def tearDown(self):
        gd.SERVER_TIMEOUT = 4
        os.remove('/tmp/test.txt')
        shutil.rmtree(self.in_dir)

    def test_correct_answer(self):
        user_answer = "class Test {\n\tint square_num(int a) {\n\treturn a*a;\n\t}\n}"
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get('success'))

    def test_incorrect_answer(self):
        user_answer = "class Test {\n\tint square_num(int a) {\n\treturn a;\n\t}\n}"
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertFalse(result.get('success'))
        lines_of_error = len(result.get('error')[0].splitlines())
        self.assertFalse(result.get('success'))
        self.assert_correct_output("Incorrect", result.get('error'))
        self.assertTrue(lines_of_error > 1)

    def test_error(self):
        user_answer = "class Test {\n\tint square_num(int a) {\n\treturn a*a"
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertFalse(result.get("success"))
        self.assert_correct_output("Error", result.get("error"))

    def test_infinite_loop(self):
        user_answer = "class Test {\n\tint square_num(int a) {\n\t\twhile(0==0){\n\t\t}\n\t}\n}"
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertFalse(result.get("success"))
        self.assert_correct_output(self.timeout_msg, result.get("error"))

    def test_file_based_assert(self):
        self.file_paths = [("/tmp/test.txt", False)]
        self.test_case_data = [
            {"test_case": "java_files/read_file.java",
            "test_case_type": "standardtestcase",
            "weight": 0.0
            }
        ]
        user_answer = dedent("""
            import java.io.BufferedReader;
            import java.io.FileReader;
            import java.io.IOException;
            class Test{
            String readFile() throws IOException {
            BufferedReader br = new BufferedReader(new FileReader("test.txt"));
            try {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();
                while (line != null) {
                    sb.append(line);
                    line = br.readLine();}
                return sb.toString();
            } finally {
                br.close();
            }}}
            """)
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get("success"))

class JavaStdIOEvaluationTestCases(EvaluatorBaseTest):
    def setUp(self):
        with open('/tmp/test.txt', 'wb') as f:
            f.write('2'.encode('ascii'))
        tmp_in_dir_path = tempfile.mkdtemp()
        self.in_dir = tmp_in_dir_path
        self.test_case_data = [{'expected_output': '11',
                                'expected_input': '5\n6',
                                'test_case_type': 'stdiobasedtestcase',
                                'weight': 0.0
                            }]
        self.file_paths = None
        gd.SERVER_TIMEOUT = 9
        self.timeout_msg = ("Code took more than {0} seconds to run. "
                            "You probably have an infinite loop in"
                            " your code.").format(gd.SERVER_TIMEOUT)

    def tearDown(self):
        gd.SERVER_TIMEOUT = 4
        os.remove('/tmp/test.txt')
        shutil.rmtree(self.in_dir)

    def test_correct_answer(self):
        user_answer = dedent("""
        import java.util.Scanner;
        class Test
        {public static void main(String[] args){
         Scanner s = new Scanner(System.in);
         int a = s.nextInt();
         int b = s.nextInt();
         System.out.print(a+b);
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get('success'))

    def test_array_input(self):
        self.test_case_data = [{'expected_output': '561',
                                'expected_input': '5\n6\n1',
                                'test_case_type': 'stdiobasedtestcase',
                                'weight': 0.0
                                }]
        user_answer = dedent("""
        import java.util.Scanner;
        class Test
        {public static void main(String[] args){
         Scanner s = new Scanner(System.in);
         int a[] = new int[3];
         for (int i=0;i<3;i++){
         a[i] = s.nextInt();
         System.out.print(a[i]);}
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get('success'))

    def test_incorrect_answer(self):
        user_answer = dedent("""
        import java.util.Scanner;
        class Test
        {public static void main(String[] args){
         Scanner s = new Scanner(System.in);
         int a = s.nextInt();
         int b = s.nextInt();
         System.out.print(a);
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        lines_of_error = len(result.get('error')[0].splitlines())
        self.assertFalse(result.get('success'))
        self.assert_correct_output("Incorrect", result.get('error'))
        self.assertTrue(lines_of_error > 1)

    def test_error(self):
        user_answer = dedent("""
        class Test
        {
         System.out.print("a");
        }""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertFalse(result.get("success"))
        self.assertTrue("Compilation Error" in '\n'.join(result.get("error")))

    def test_infinite_loop(self):
        user_answer = dedent("""
        class Test
        {public static void main(String[] args){
         while(0==0)
         {
         System.out.print("a");}
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertFalse(result.get("success"))
        self.assert_correct_output(self.timeout_msg, result.get("error"))

    def test_only_stdout(self):
        self.test_case_data = [{'expected_output': '11',
                                'expected_input': '',
                                'test_case_type': 'stdiobasedtestcase',
                                'weight': 0.0
                               }]
        user_answer = dedent("""
        class Test
        {public static void main(String[] args){
         int a = 5;
         int b = 6;
         System.out.print(a+b);
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get('success'))

    def test_string_input(self):
        self.test_case_data = [{'expected_output': 'HelloWorld',
                                'expected_input': 'Hello\nWorld',
                                'test_case_type': 'stdiobasedtestcase',
                                'weight': 0.0
                               }]
        user_answer = dedent("""
        import java.util.Scanner;
        class Test
        {public static void main(String[] args){
         Scanner s = new Scanner(System.in);
         String a = s.nextLine();
         String b = s.nextLine();
         System.out.print(a+b);
        }}""")
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get('success'))

    def test_file_based_stdout(self):
        self.file_paths = [("/tmp/test.txt", False)]
        self.test_case_data = [{'expected_output': '2',
                                'expected_input': '',
                                'test_case_type': 'stdiobasedtestcase',
                                'weight': 0.0
                               }]
        user_answer = dedent("""
            import java.io.BufferedReader;
            import java.io.FileReader;
            import java.io.IOException;
            class Test{
            public static void main(String[] args) throws IOException {
            BufferedReader br = new BufferedReader(new FileReader("test.txt"));
            try {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();
                while (line != null) {
                    sb.append(line);
                    line = br.readLine();}
                System.out.print(sb.toString());
            } finally {
                br.close();
            }}}
            """)
        kwargs = {
                  'metadata': {
                    'user_answer': user_answer,
                    'file_paths': self.file_paths,
                    'partial_grading': False,
                    'language': 'java'
                    },
                    'test_case_data': self.test_case_data,
                  }

        grader = Grader(self.in_dir)
        result = grader.evaluate(kwargs)

        self.assertTrue(result.get("success"))


if __name__ == '__main__':
    unittest.main()
