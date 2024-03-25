import unittest



import sys
sys.path.append('../json_parser')

from json_parser.JSONParser import parseObject, parseArray, findEnd
class TestJSONParser(unittest.TestCase):
    def test_findEnd(self):
        testInput = '[]'
        self.assertEqual(findEnd(testInput, '['), 1)
        
        testInput = '[[]]'
        self.assertEqual(findEnd(testInput, '['), 3)

        testInput = '[{[abc]}]'
        self.assertEqual(findEnd(testInput, '['), len(testInput)-1)

        testInput = '{ abc [] {} } []'
        self.assertEqual(findEnd(testInput, '{'), 12)

    def test_parseObject(self):
        # Test case 1: Simple JSON object
        json_input = '{"key": "value"}'
        expected_output = {"key": "value"}
        self.assertEqual(parseObject(json_input), expected_output)
        
        # Test case 2: Nested JSON object at end
        json_input = '{"key": "value", "key2": ''a'', "key3": 5, "key4" : ''false'', "key5" : null }'
        expected_output = {"key": "value", "key2" : 'a', "key3": 5, "key4": False, "key5": None}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 3: Nested JSON object at end
        json_input = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}}'
        expected_output = {"key1": "value1", "key2": {"nestedKey": "nestedValue"}}
        self.assertEqual(parseObject(json_input), expected_output)
        
        # Test case 4: Nested JSON object in the middle
        json_input = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}, "key3" : "value3"}'
        expected_output = {"key1": "value1", "key2": {"nestedKey": "nestedValue"}, "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)

         # Test case 5: Nested JSON object in the middle
        json_input = '{"key2": {"nestedKey": "nestedValue"}, "key3" : "value3"}'
        expected_output = {"key2": {"nestedKey": "nestedValue"}, "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 6: Double nested object
        json_input = '{"key": {"nestedKey": {"nestedNestedKey" : "nestedNestedValue"}}, "key3" : "value3"}'
        expected_output = {"key": {"nestedKey": {"nestedNestedKey" : "nestedNestedValue"}}, "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 7: JSON object with array at end
        json_input = '{"key1": "value1", "key2": ["item1", "item2"]}'
        expected_output = {"key1": "value1", "key2": ["item1", "item2"]}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 8: JSON object with array in middle
        json_input = '{"key1": "value1", "key2": ["item1", "item2"], "key3" : "value3"}'
        expected_output = {"key1": "value1", "key2": ["item1", "item2"], "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 9: JSON object with array in beginning
        json_input = '{"key1": ["item1", "item2"], "key2": "value2" , "key3" : "value3"}'
        expected_output = {"key1": ["item1", "item2"], "key2": "value2", "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)
        
        # Test case 10: JSON object with double nested array
        json_input = '{"key1": "value1", "key2": ["item1", "item2", ["nestedItem1", "nestedItem2"]]}'   
        expected_output = {"key1": "value1", "key2": ["item1", "item2", ["nestedItem1", "nestedItem2"]]}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 10: JSON object with double nested array in the beginning
        json_input = '{"key1": ["item1", "item2", ["nestedItem1", "nestedItem2"]], "key2": ["value2"] }'   
        expected_output = {"key1": ["item1", "item2", ["nestedItem1", "nestedItem2"]], "key2": ["value2"]}
        self.assertEqual(parseObject(json_input), expected_output)
        
        # Test case 11: JSON object with array of objects at end
        json_input = '{"key1": "value1", "key2": [{"nestedKey1": "nestedValue1"}, {"nestedKey2": "nestedValue2"}]}'
        expected_output = {"key1": "value1", "key2": [{"nestedKey1": "nestedValue1"}, {"nestedKey2": "nestedValue2"}]}
        self.assertEqual(parseObject(json_input), expected_output)

        # Test case 12: JSON object with array of objects in the middle
        json_input = '{"key1": "value1", "key2": [{"nestedKey1": "nestedValue1"}, {"nestedKey2": "nestedValue2"}], "key3" : "value3"}'
        expected_output = {"key1": "value1", "key2": [{"nestedKey1": "nestedValue1"}, {"nestedKey2": "nestedValue2"}], "key3" : "value3"}
        self.assertEqual(parseObject(json_input), expected_output)

        


    def test_parseArray(self):
        
        inputArray = '[1, 2, 3, 4]'
        expectedOutput = [1,2,3, 4]
        self.assertEqual(parseArray(inputArray), expectedOutput)

        inputArray = "[[1,2,3,4]]"
        expectedOutput = [[1,2,3, 4]]
        self.assertEqual(parseArray(inputArray), expectedOutput)

        inputArray = "[[[1,2,3,4]]]"
        expectedOutput = [[[1,2,3, 4]]]
        self.assertEqual(parseArray(inputArray), expectedOutput)
        
        inputArray = "[1,[2,3],4,5]"
        expectedOutput = [1,[2,3], 4,5]
        self.assertEqual(parseArray(inputArray), expectedOutput)

        inputArray = "[1,[2,[3]],4,5]"
        expectedOutput = [1,[2,[3]], 4,5]
        self.assertEqual(parseArray(inputArray), expectedOutput)

        inputArray = "[1,[2,[3]],4,[5]]"
        expectedOutput = [1,[2,[3]], 4,[5]]
        self.assertEqual(parseArray(inputArray), expectedOutput)
        



if __name__ == '__main__':
    unittest.main()