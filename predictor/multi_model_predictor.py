from pomegranate import HiddenMarkovModel

with open('../model_generator/partial_model_coding_to_donor_model0.json') as coding_to_donor_model_file0:
    coding_to_donor_model_json0 = coding_to_donor_model_file0.read()

with open('../model_generator/partial_model_coding_to_donor_model1.json') as coding_to_donor_model_file1:
    coding_to_donor_model_json1 = coding_to_donor_model_file1.read()

with open('../model_generator/partial_model_coding_to_donor_model2.json') as coding_to_donor_model_file2:
    coding_to_donor_model_json2 = coding_to_donor_model_file2.read()

with open('../model_generator/partial_model_intron_acceptor_model.json') as intron_acceptor_model_file:
    intron_acceptor_model_json = intron_acceptor_model_file.read()

with open('../model_generator/partial_model_start_model.json') as start_model_file:
    start_model_json = start_model_file.read()

with open('../model_generator/partial_model_coding_to_stop_model0.json') as coding_to_stop_model_file0:
    coding_to_stop_model_json0 = coding_to_stop_model_file0.read()

with open('../model_generator/partial_model_coding_to_stop_model1.json') as coding_to_stop_model_file1:
    coding_to_stop_model_json1 = coding_to_stop_model_file1.read()

with open('../model_generator/partial_model_coding_to_stop_model2.json') as coding_to_stop_model_file2:
    coding_to_stop_model_json2 = coding_to_stop_model_file2.read()


start_model = HiddenMarkovModel.from_json(start_model_json)

coding_to_donor_model0 = HiddenMarkovModel.from_json(coding_to_donor_model_json0)
coding_to_donor_model1 = HiddenMarkovModel.from_json(coding_to_donor_model_json1)
coding_to_donor_model2 = HiddenMarkovModel.from_json(coding_to_donor_model_json2)

intron_acceptor_model = HiddenMarkovModel.from_json(intron_acceptor_model_json)

coding_to_stop_model0 = HiddenMarkovModel.from_json(coding_to_stop_model_json0)
coding_to_stop_model1 = HiddenMarkovModel.from_json(coding_to_stop_model_json1)
coding_to_stop_model2 = HiddenMarkovModel.from_json(coding_to_stop_model_json2)


def get_path_names(seq, model):
    logp, path = model.viterbi(seq)
    return [x[1].name for x in path]


def search_start(seq, start_model):
    print(len(seq))
    step = 25
    site = 0
    max = -1000000000
    for x in range(0, len(seq), step):
        if x + 100 <= len(seq):
            logp, path = start_model.viterbi(seq[x:x + 100])
            best_path = [x[1].name for x in path]
            print( x/step, logp, best_path)
            if logp > max and 'start zone8' in best_path:
                max = logp
                site = x / step
    print('max', max, 'site', site)


def exon_predict(seq, coding_start, coding_state, exon_len):
    max_known_exon = exon_len
    seq_after_start = seq[coding_start: coding_start + max_known_exon]
    logp = None
    path = None
    logp2 = None
    path2 = None

    if coding_state == 0:
        logp, path = coding_to_donor_model0.viterbi(seq_after_start)
        logp2, path2 = coding_to_stop_model0.viterbi(seq_after_start)

    elif coding_state == 1:
        logp, path = coding_to_donor_model1.viterbi(seq_after_start)
        logp2, path2 = coding_to_stop_model1.viterbi(seq_after_start)

    elif coding_state == 2:
        logp, path = coding_to_donor_model2.viterbi(seq_after_start)
        logp2, path2 = coding_to_stop_model2.viterbi(seq_after_start)

    stop_path = None
    if path2:
        stop_path = [x[1].name for x in path2][1:-1]
    #print(logp, logp2)

    if path:
        exon_path = [x[1].name for x in path]
        exon_path = exon_path[1:-1]

        donor0 = exon_path.index('donor00')
        last_coding_state = exon_path[donor0 - 1]

        intron_start = exon_path.index('donor04')

        #print(len(exon_path), len(seq_after_start), exon_path[intron_start], seq_after_start[intron_start])
        #print('ex', seq_after_start[:intron_start])
        return last_coding_state, intron_start, exon_path[:intron_start], stop_path


def intron_predict(seq, intron_start, intron_len):

    seq_after_gt = seq[intron_start:intron_len]
    if len(seq_after_gt) > 22:
        logp, path_intron = intron_acceptor_model.viterbi(seq_after_gt)

        intron_path = [x[1].name for x in path_intron]
        intron_end = intron_path.index('acceptor015')
        #print('i', seq_after_gt[:intron_end])
        return intron_end, intron_path[1:intron_end + 1]


def predict(seq, exon_len, intron_len):

    logp, path = start_model.viterbi(seq)
    start_path = [x[1].name for x in path]
    start_path = start_path[1:]
    longest_prediction = []
    possible_predictions = []
    try:
        atg_index = start_path.index('start zone8')
        coding_start = atg_index + 3
        from_start_to_atg = seq[:atg_index + 3]

        # print(len(from_start_to_atg), len(start_path[:atg_index + 3])) check for equal len
        # print(len(from_start_to_atg), len(start_path[:atg_index + 3]))
        # print(from_start_to_atg)
        longest_prediction += start_path[:atg_index + 3]
        # print(longest_prediction)
        coding_state = 0
        while coding_start < len(seq):

            rex = exon_predict(seq, coding_start, coding_state, exon_len)

            if rex:
                last_coding_state, intron_start_in_this_path, exon_path, stop_path = rex

                rei = intron_predict(seq, coding_start + intron_start_in_this_path, intron_len)
                #print('exon_path', len(exon_path), exon_path)
                #print(stop_path)

                if stop_path:
                    #print('stop_path', len(stop_path))
                    local_end = longest_prediction + stop_path
                    possible_predictions.append(local_end.copy())
                    #print('local end', len(local_end), local_end)
                longest_prediction += exon_path


                if last_coding_state == 'coding state 2':
                    coding_state = 1

                if last_coding_state == 'coding state 1':
                    coding_state = 0

                if last_coding_state == 'coding state 0':
                    coding_state = 2

                if rei:
                    intron_end, intron_path = rei
                    #print('intron p', len(intron_path), intron_path)
                    longest_prediction += intron_path
                    # print('happens', longest_prediction)
                    coding_start = coding_start + intron_start_in_this_path + intron_end # After AG
                else:
                    break
            else:
                break
        back_to_start = start_path[:atg_index+1]
    except ValueError as e:
        print(e)

    return possible_predictions
