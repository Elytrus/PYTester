import tester.tester as tester
import tester.event.event_types as event_types
from tester.types import TRUNCATE_AMOUNT


def on_finish(event):
    if 'CE' in event.meta:
        print('Compile Error!')

    print('End Results: %d/%d cases correct!' % (event.correct_count, event.total_count))
    print()


def on_case(event):
    print('Result for Case #%d: %s (%.3fs)' % (event.results.case_id, event.results.code, event.results.time))

    if event.results.err:
        print('Error was:\n%s\n' % event.results.err)
    elif event.results.code == 'WA':
        print('Output (truncated):\n%s\n' % event.results.out[:20])


def on_begin(event):
    print('\nTesting file "%s" with %d cases and time limit %.2fs\n' % (event.file_name, event.case_cnt,
                                                                    event.time_limit))


class TextHandler:
    """
    A text based display mechanism for test case results
    """

    def __init__(self, show_time=True, show_score=True, show_correct_output=True, truncate_amount=TRUNCATE_AMOUNT):
        """
        Constructor

        :param show_time: Controls whether the run time is shown
        :param show_score: Controls whether a score is shown in the end
        :param show_correct_output: Controls whether correct output is shown in case of a WA
        :param truncate_amount: How much to truncate output by (if it is being displayed)
        """

        self.tester = tester.Tester()

        self.tester.register_handler(event_types.BeginEvent, on_begin)
        self.tester.register_handler(event_types.CaseTestedEvent, on_case)
        self.tester.register_handler(event_types.FinishEvent, on_finish)

        self.truncate_amount = truncate_amount
        self.show_correct_output = show_correct_output
        self.show_score = show_score
        self.show_time = show_time

    def test(self, file_name, is_async=False):
        """
        Tests the specified file in either a synchronous or asynchronous fashion

        :param file_name: The file name of the file to run the test with
        :param is_async: Whether the test is asynchronous
        :return: Nothing
        """

        if is_async:
            self.tester.test_async(file_name)
        else:
            self.tester.test_sync(file_name)
