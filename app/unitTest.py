import unittest
import mypythonsite
from mypythonsite import app

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_parse(self):
        info = mypythonsite.parse()
        self.assertIsNotNone(info, "parse() должна возвращать значение")
        self.assertIsInstance(info, list, "возвращаемое значение parse() должно быть списком")

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        mypythonsite.name.pop() #убираем добавляемую вручную валюту
        self.assertIsNotNone(mypythonsite.name, "Переменная отвечающая за формирование списка валют пустая")
        dropdown_list_1 = response.data.decode('utf-8')
        self.assertRegex(dropdown_list_1, r'<option>.+</option>',
                         "Первый dropdown список должен содержать хотя бы один элемент")

    def test_form(self):
        self.app.get('/')
        response = self.app.post('/', data={'num_1': '10', 'droplist1': '(840|USD) Доллар США', 'droplist2': '(978|EUR) Евро'})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(mypythonsite.result, 9.4, None, 'Вывод функции неправильный либо курс валют изменился', 0.1)

if __name__ == '__main__':
    unittest.main()
