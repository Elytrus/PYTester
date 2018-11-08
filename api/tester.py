import configparser
import os
import collections
import time
import subprocess as sub
import event.dispatcher as dispatcher
import event.event_types as event_types
import api.types as types
from threading import Thread, Timer

CFG_FLAGS_SECT = 'Flags'
CFG_SETTINGS_SECT = 'Settings'

CFG_TIME_LIMIT_KEY = 'TimeLimit'
CFG_CASE_COUNT_KEY = 'CaseCount'
CFG_DIRECTORY_KEY = 'Directory'
CFG_BASE_NAME_KEY = 'BaseName'
CFG_PROGRAM_NAME_KEY = 'ProgramName'

FLAG_CHECK_OUTPUT_KEY = 'checkoutput'
FLAG_CHECK_TIME_KEY = 'checktime'


class Tester:
    def __init__(self):
        self.dispatcher = dispatcher.Dispatcher()

    def register_handler(self, event_type, handle):
        """
        Registers an event handler

        :param event_type: The type of event the handler should handle
        :type event_type: class
        :param handle: The handler
        :type handle: function
        :return: Nothing
        :rtype: NoneType
        """

        if event_type not in event_types.VALID_EVENT_TYPES:
            raise ValueError('Invalid event type!')

        self.dispatcher.register(event_type, handle)

    def test_async(self, config_file):
        """
        Tests the specified program asynchronously, function is otherwise identical to `test_sync`

        :param config_file: The config file
        :type config_file: file
        :return:
        """

        thread = Thread(target=self.test_sync, args=(config_file,))
        thread.start()

    def test_sync(self, config_file):
        """
        Preforms a test based on what is specified in the file `config_file` synchronously

        == A valid file for `config_file` should look something like this: ==

        [Settings]
        ProgramName = echo.py # Program file name
        BaseName = echo # Test case base_name
        Directory = . # Directory to operate in
        CaseCount = 20 # Amount of test cases
        TimeLimit = 2.0 # Time Limit in Seconds

        [Flags]
        CheckTime = True
        CheckOutput = True

        == Valid Flags for Config Section Flags ==

        CheckTime - Check if program takes more than `time_limit` seconds to run (type: bool)
        CheckOutput - Checks the program output with test case output (type: bool)

        :param config_file: A file object denoting the specifications of the program and the cases
        :type config_file: file
        :return: Nothing
        :rtype: NoneType
        """

        # Config Reading

        config = configparser.ConfigParser()
        config.read_file(config_file)

        program_name = config.get(CFG_SETTINGS_SECT, CFG_PROGRAM_NAME_KEY, fallback=None)
        base_name = config.get(CFG_SETTINGS_SECT, CFG_BASE_NAME_KEY, fallback=None)
        directory = config.get(CFG_SETTINGS_SECT, CFG_DIRECTORY_KEY, fallback='.')
        case_count = config.getint(CFG_SETTINGS_SECT, CFG_CASE_COUNT_KEY, fallback=1)
        time_limit = config.getfloat(CFG_SETTINGS_SECT, CFG_TIME_LIMIT_KEY, fallback=-1.0)

        if not program_name:
            raise ValueError('Required field %s.%s was not specified in the config file!' %
                             (CFG_SETTINGS_SECT, CFG_PROGRAM_NAME_KEY))

        if not base_name:
            raise ValueError('Required field %s.%s was not specified in the config file!' %
                             (CFG_SETTINGS_SECT, CFG_BASE_NAME_KEY))

        if not config.has_section(CFG_FLAGS_SECT):
            raise ValueError('Required section %s was not specified in the config file!' %
                             CFG_FLAGS_SECT)

        # Running private test function

        self._test('%s\\%s' % (directory, program_name),
                   case_count,
                   parse_case_files(base_name, case_count, directory),
                   time_limit,
                   collections.defaultdict(bool, config[CFG_FLAGS_SECT]))

    @staticmethod
    def _decode_output(out_bytes):
        if out_bytes:
            return str(out_bytes, 'utf-8')
        return ''

    def _test(self, file_name, case_count, cases, time_limit, flags):
        """
        Private testing function

        :param file_name:
        :type file_name: str
        :param case_count:
        :type case_count: int
        :param cases:
        :type cases: iter
        :param time_limit:
        :type time_limit: int
        :param flags:
        :type flags: dict
        :return: Nothing
        :rtype: NoneType
        """

        self.dispatcher.dispatch(event_types.BeginEvent(file_name, case_count, time_limit, flags))

        curr_case = 1
        correct_count = 0

        for case in cases:
            # Opening Required subprocess

            process = sub.Popen(['py', file_name], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)

            tle = False
            curr_time = time.time()

            # Setting up timer and passing input

            def kill_process():
                nonlocal tle, result

                process.kill()
                tle = True
                result = ('', '')

            if flags[FLAG_CHECK_TIME_KEY] and time_limit != -1.0:
                try:
                    timer = Timer(time_limit + 0.05, kill_process)
                    timer.start()
                    result = process.communicate(bytes(case.inp, 'utf-8'))
                finally:
                    timer.cancel()
            else:
                result = process.communicate(bytes(case.inp, 'utf-8'))

            # Parsing output

            out, err = map(Tester._decode_output, result)
            out = out.strip().replace('\r', '')

            # Setting case code

            if err:
                code = 'IR'
            elif tle:
                code = 'TLE'
            elif flags[FLAG_CHECK_OUTPUT_KEY]:
                if out != case.out:
                    code = 'WA'
                else:
                    code = 'AC'
                    correct_count += 1
            else:
                code = 'U'

            self.dispatcher.dispatch(
                event_types.CaseTestedEvent(file_name,
                                            types.Result(
                                                curr_case,
                                                case,
                                                out,
                                                err,
                                                time.time() - curr_time,
                                                code
                                            ),
                                            flags))

            curr_case += 1  # Increment case id

        # Testing is complete

        self.dispatcher.dispatch(event_types.FinishEvent(file_name, correct_count, case_count, flags))


def to_cases(inputs, outputs=None):
    """
    Converts list of inputs and/or outputs into a list of cases

    :param inputs: Inputs for the test cases
    :type inputs: list
    :param outputs: (Optional) Outputs for test cases
    :type outputs: list

    :return: A list of cases made from the inputted inputs and outputs
    :rtype: list
    """

    if outputs:
        return [types.Case(inp, out) for inp, out in zip(inputs, outputs)]
    return [types.Case(inp, None) for inp in inputs]


def parse_case_files(base_name, case_cnt=1, directory=os.getcwd()):
    """
    Parses the case files for the given base_name within the given directory

    Test Data File Format:

     -- Inputs:
    <base_name>_<case #>.in

     -- Outputs:
    <base_name>_<case #>.out

     -- Example:
    <base_name> -> echo

    echo_1.in
    echo_1.in
    echo_2.in
    echo_2.out
    echo_3.out
    echo_3.out
    ...

    :param base_name: The base name for the test cases (as shown earlier)
    :type base_name: str
    :param case_cnt: Amount of cases (defaults to 1)
    :type case_cnt: int
    :param directory: The directory to search in. defaults to os.getcwd()
    :type directory: str

    :return: A list of cases for the corresponding test files
    :rtype: list
    """

    inputs = []
    outputs = []

    for i in range(1, case_cnt + 1):
        curr_base_name = '%s_%d' % (base_name, i)

        with open('%s\\%s.in' % (directory, curr_base_name), 'r') as f:
            inputs.append(f.read().strip())

        with open('%s\\%s.out' % (directory, curr_base_name), 'r') as f:
            outputs.append(f.read().strip())

    return to_cases(inputs, outputs)
