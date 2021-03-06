
def generate_exons(file_from, prefix=''):
    with open(file_from) as in_file, open(prefix + 'exons_start_0.txt', 'w') as ex0,\
                    open(prefix + 'exons_start_1.txt', 'w') as ex1,\
                    open(prefix + 'exons_start_2.txt', 'w') as ex2:
        for line in in_file:
            print(line)
            previous = 2
            tokenized = line.split()
            for i, token in enumerate(tokenized[:-1]):
                index_of_P = token.index('P')
                token_until_P = token[:index_of_P]
                print(previous)
                print(token_until_P)
                remain_current_len = len(token_until_P) % 3
                current_start = (previous + 4) % 3
                current_end = (previous + remain_current_len) % 3
                print(len(token_until_P), len(token_until_P) % 3)
                print('current__start', current_start)
                print('current_end', current_end)
                previous = current_end

                if current_start == 0:
                    ex0.write(token + '\n')
                if current_start == 1:
                    ex1.write(token + '\n')
                if current_start == 2:
                    ex2.write(token + '\n')