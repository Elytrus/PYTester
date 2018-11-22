import tester.tester as tester
import tester.event.event_types as event_types


def on_finish(event):
    if 'CE' in event.meta:
        print('Compile Error!')

    print('End Results: %d/%d cases correct!' % (event.correct_count, event.total_count))
    print()


def on_case(event):
    print('Result for Case #%d: %s (%.3fs)' % (event.results.case_id, event.results.code, event.results.time))

    if event.results.err:
        print('Error was:\n', event.results.err)
    elif event.results.code == 'WA':
        print('Output (truncated):', event.results.out[:20])


def on_begin(event):
    print('Testing file "%s" with %d cases and time limit %.2fs' % (event.file_name, event.case_cnt,
                                                                    event.time_limit))


class TextHandler:
    def __init__(self):
        self.tester = tester.Tester()

        self.tester.register_handler(event_types.BeginEvent, on_begin)
        self.tester.register_handler(event_types.CaseTestedEvent, on_case)
        self.tester.register_handler(event_types.FinishEvent, on_finish)

    def test(self, file_name, is_async=False):
        if is_async:
            self.tester.test_async(file_name)
        else:
            self.tester.test_sync(file_name)