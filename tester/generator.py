import tester.run as run

def generate(base_name, input_generator_file, output_generator_file, case_cnt=1, input_argv=[]):
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

            if i <= input_argv_len:
                cargv = [str(arg) for arg in input_argv[i - 1]]

            case_in, _, _, _ = run.exec_file(input_generator_file, '', argv=cargv)
            case_out, _, _, _ = run.exec_file(output_generator_file, case_in)

            curr_base_name = '%s_%d' % (base_name, i)

            with open(curr_base_name + '.in', 'w') as f:
                f.write(case_in)

            with open(curr_base_name + '.out', 'w') as f:
                f.write(case_out)

        # Cleanup files

        run.post_exec_file(input_generator_file)
        run.post_exec_file(output_generator_file)