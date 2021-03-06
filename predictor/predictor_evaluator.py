import numpy
from converter_to import converter_to
from multi_model_predictor import predict


def get_testable_string(annotated_string):
    l = [x[0] for x in annotated_string.lower().split()]
    a = [x[1] for c, x in enumerate(annotated_string.split()) if c > 1]
    two = converter_to(l, 2)
    seq = numpy.array(two, numpy.unicode_)
    return seq, a,''.join(l)


def evaluate(prediction, annotation):

    # print(ok_start)
    no_coding_names = ['back',
                       'start zone0', 'start zone1', 'start zone2', 'start zone3', 'start zone4', 'start zone5',
                       'start zone6', 'start zone7',
                       'donor04', 'donor05', 'donor06', 'donor07', 'donor08', 'donor09', 'donor010', 'donor011',
                       'in',
                       'acceptor00', 'acceptor01', 'acceptor02', 'acceptor03', 'acceptor04', 'acceptor05', 'acceptor06',
                       'acceptor07', 'acceptor08', 'acceptor09', 'acceptor010', 'acceptor011', 'acceptor012',
                       'acceptor013', 'acceptor014', 'acceptor015'
                       'stop9', 'stop10', 'stop11', 'stop12', 'stop13', 'stop14', 'stop15', 'stop16', 'stop17',
                       'stop18', 'stop19',
                       'post']

    true_negatives = 0
    fake_positives = 0
    true_positives = 0
    fake_negatives = 0

    for i, a in enumerate(annotation):
        if i < len(prediction):
            if a in ['b', 'n', 'f']: # b -> background ; n -> intron; f -> after
                if prediction[i] in no_coding_names:
                    true_negatives += 1
                else:
                    fake_positives += 1
            else:
                if prediction[i] in no_coding_names:
                    fake_negatives += 1
                else:
                    true_positives += 1
        else:
            if a in ['b', 'n', 'f']:  # b -> background ; n -> intron; f -> after
                true_negatives += 1
            else:
                fake_negatives += 1

    return true_positives, true_negatives, fake_positives, fake_negatives


def test_50(exon_len, intron_len, min_len,  max_len):
    lines = set()
    names = set()

    with open('CDS_comp_50_50') as file:

        for line in file:
            t = line.split('-')
            if t[1] not in names and min_len * 3 < len(t[0]) <= max_len * 3:
                names.add(t[1])
                lines.add(t[0])

        sensitivity_acum = 0
        specificity_acum = 0
        true_positives_acum = 0
        true_negatives_acum = 0
        fake_positives_acum = 0
        fake_negatives_acum = 0

        counts = 0

        for line2 in lines:
            parts = line2.split('-')
            annotated = parts[0]
            seq, a, _ = get_testable_string(annotated)

            predictions, longest_pred, longest_with_end = predict(seq, exon_len, intron_len)
            alt = [longest_with_end]
            # print('!', len(seq), len(a))
            for i, pred in enumerate(alt):
                true_positives, true_negatives, fake_positives, fake_negatives = evaluate(pred, a)
                if i == (len(predictions) - 1):

                    sensitivity = true_positives / (true_positives + fake_negatives)
                    specificity = true_positives / (true_positives + fake_positives)
                    # print(sensitivity, specificity )

                    sensitivity_acum += sensitivity
                    specificity_acum += specificity

                    counts += 1

                    true_positives_acum += true_positives
                    true_negatives_acum += true_negatives
                    fake_positives_acum += fake_positives
                    fake_negatives_acum += fake_negatives

        if not counts:
            return 0, 0

        sensitivity_mean = sensitivity_acum / counts
        specificity_mean = specificity_acum / counts

        sensitivity_total = true_positives_acum / (true_positives_acum + fake_negatives_acum)
        specificity_total = true_positives_acum / (true_positives_acum + fake_positives_acum)
        print(counts, true_positives_acum, true_negatives_acum, fake_positives_acum, fake_negatives_acum)
        return sensitivity_total, specificity_total, sensitivity_mean, specificity_mean


if __name__ == '__main__':
    median_len = 7000
    #starts = int(median_len / 2)
    starts = 6000
    minl = 0

    """
    print(test_50(5100, 4800, 0, 5000))
    print(test_50(5100, 6100, 0, 5900))
    """

    combined = -1000000
    best_pair_combined = None
    bests = None

    for exon_len in range(starts, median_len + 200, 100):
        for intron_len in range(starts, median_len + 200, 100):

            sensitivity_total, specificity_total, sens_mean, spec_mean = test_50(exon_len, intron_len, minl, median_len)

            score = sensitivity_total + specificity_total + sens_mean + spec_mean

            if score > combined:
                combined = score
                best_pair_combined = (exon_len, intron_len)
                bests = (sensitivity_total, specificity_total, sens_mean, spec_mean)
                print(sensitivity_total,
                      specificity_total,
                      sens_mean,
                      spec_mean,
                      best_pair_combined,
                      bests,
                      exon_len,
                      intron_len)
