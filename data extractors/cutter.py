def cut_starts(file, output, before, after):

    with open(file) as file_handle, open(output, 'w') as output_handle:
        for line in file_handle:
            tokens = line.split()
            for it, token in enumerate(tokens[:1]):
                for i, char in enumerate(token):
                    if char == 'P':
                        if i + after < len(token):
                            output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + '\n')
    #                    else:
    #                        to_take = i + after - len(token) + 1
    #                        append = tokens[it + 1][:to_take]
    #                        output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + append.lower() + '\n')


def cut_ends():
    file = 'new_cutsa.txt'
    output = 'new_stops.exa'
    before = 11
    after = 11

    with open(file) as file_handle, open(output, 'w') as output_handle:
        for line in file_handle:
            tokens = line.split()
            for it, token in enumerate(tokens[-1:]):
                for i, char in enumerate(token):
                    if char == 'P':
                        if i + after < len(token):
                            output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + '\n')




def cut_donors():
    file = 'new_cutsa.txt'
    output = 'new_donor1.exa'
    before = 6
    after = 8

    with open(file) as file_handle, open(output, 'w') as output_handle:
        for line in file_handle:
            tokens = line.split()
            for it, token in enumerate(tokens[1:]):
                for i, char in enumerate(token):
                    if char == 'P':
                        if i + after < len(token):
                            output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + '\n')
    #                    else:
    #                        to_take = i + after - len(token) + 1
    #                        append = tokens[it + 1][:to_take]
    #                        output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + append.lower() + '\n')


def cut_acceptors():
    file = 'new_cutsb.txt'
    output = 'new_acceptor1.exa'
    before = 18
    after = 5

    with open(file) as file_handle, open(output, 'w') as output_handle:
        for line in file_handle:
            tokens = line.split()
            for it, token in enumerate(tokens[:-1]):
                for i, char in enumerate(token):
                    if char == 'P':
                        if i + after < len(token):
                            output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + '\n')
    #                    else:
    #                        to_take = i + after - len(token) + 1
    #                        append = tokens[it + 1][:to_take]
    #                        output_handle.write(token[i - before: i + after + 1].replace('P', '').lower() + append.lower() + '\n')
