import tester.run as run


def generate(base_name, input_generator_file, output_generator_file, case_cnt=1, input_argv=[]):
    """
    Data generation function that creates randomly generated data

    :param base_name: The base name of the data that is to be generated
    :param input_generator_file: The file name of the input generator
    :param output_generator_file: The file name of the output generator
    :param case_cnt: The amount of cases to generate
    :param input_argv: A list of lists specifying the system arguments to pass into the input generator for each case
    :return: Nothing, the function automatically writes the generated data to files
    """

    # Compile generators if needed

    new_input_generator_file = run.pre_exec_file(input_generator_file)

    if new_input_generator_file:
        input_generator_file = new_input_generator_file

    new_output_generator_file = run.pre_exec_file(output_generator_file)

    if new_output_generator_file:
        output_generator_file = new_output_generator_file

    # Creating cases

    input_argv_len = len(input_argv)
    for i in range(1, case_cnt + 1):
        cargv = []

        # Converting system arguments so lists of strings

        if i <= input_argv_len:
            if isinstance(input_argv[i - 1], list):
                cargv = [str(arg) for arg in input_argv[i - 1]]
            else:
                cargv = [str(input_argv[i - 1])]

        case_in, err_in, _, _ = run.exec_file(input_generator_file, '', argv=cargv)
        case_out, err_out, _, _ = run.exec_file(output_generator_file, case_in)

        curr_base_name = '%s_%d' % (base_name, i)

        with open(curr_base_name + '.in', 'w') as f:
            f.write(case_in)

        with open(curr_base_name + '.out', 'w') as f:
            f.write(case_out)

        # Debug Output

        if err_in:
            print('An error occurred while generating input for case %d:\n%s' % (i, err_in))
            print()

        if err_out:
            print('An error occurred while generating output for case %d:\n%s' % (i, err_out))
            print()

        print('Generated case %d' % i)

    # Cleanup files

    run.post_exec_file(input_generator_file)
    run.post_exec_file(output_generator_file)
