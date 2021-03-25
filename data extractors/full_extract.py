from gene_data_extractor import extractor
from exon_stop_for_test_clasisfier import generate_exon_to_end
from exon_for_test_clasisfier import generate_exons
from cutter import cut_starts, cut_donors, cut_acceptors, cut_ends

folder_path = '/run/media/seijasdz/BE96A68C96A6452D/Asi/Data/'

extractor(folder_path)


cut_starts(file='new_ccutsb.txt',
           output='train_start2.exa',
           before=50,
           after=50)

cut_starts(file='new_cutsb.txt',
           output='starts.exa',
           before=10,
           after=9)

cut_ends()
cut_donors()
cut_acceptors()
generate_exons('new_cutsa.txt')
generate_exons('new_ccutsa.txt', 'test_')
generate_exon_to_end('new_cutsa.txt')
generate_exon_to_end('new_ccutsa.txt', 'test_')
