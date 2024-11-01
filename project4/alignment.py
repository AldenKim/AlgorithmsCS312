def align(seq1: str, seq2: str, match_award=-3, indel_penalty=5,
        sub_penalty=1, banded_width=-1,gap='-') -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """
    left_size = len(seq1)
    top_size = len(seq2)

    matrix = {(0, 0): 0}

    if banded_width == -1:
        for i in range(1, left_size+1):
            matrix[(i, 0)] = i * indel_penalty
        for j in range(1, top_size+1):
            matrix[(0, j)] = j * indel_penalty

        for i in range(1, left_size + 1):
            for j in range(1, top_size + 1):
                adder(matrix, seq1, seq2, i , j)
    else:
        for i in range(1, banded_width + 1):
            matrix[(i, 0)] = i * indel_penalty
        for j in range(1, banded_width+1):
            matrix[(0, j)] = j * indel_penalty

        for i in range(1, left_size + 1):
            for j in range(max(1, i - banded_width), min(top_size+1, i + banded_width + 1)):
                adder(matrix, seq1, seq2, i , j)

    alignment_cost = matrix[(left_size, top_size)]

    alignment_1 = ""
    alignment_2 = ""
    i = left_size
    j = top_size

    while i > 0 or j > 0:
        current_score = matrix.get((i, j), float('inf'))

        if i > 0 and j > 0 and current_score == matrix[(i-1,j-1)] + (match_award if seq1[i-1] == seq2[j-1] else sub_penalty):
            alignment_1 = seq1[i - 1] + alignment_1
            alignment_2 = seq2[j - 1] + alignment_2
            i -= 1
            j -= 1
        elif j > 0 and current_score == matrix[(i, j-1)] + indel_penalty:
            alignment_1 = gap + alignment_1
            alignment_2 = seq2[j - 1] + alignment_2
            j -= 1
        elif i > 0 and current_score == matrix[(i-1, j)] + indel_penalty:
            alignment_1 = seq1[i - 1] + alignment_1
            alignment_2 = gap + alignment_2
            i -= 1

    return alignment_cost, alignment_1, alignment_2

def adder(matrix, seq1: str, seq2: str,i, j, match_award=-3, indel_penalty=5,
        sub_penalty=1):
    if seq1[i - 1] == seq2[j - 1]:
        match = matrix.get((i-1, j-1), float('inf')) + match_award
    else:
        match = matrix.get((i-1, j-1), float('inf')) + sub_penalty

    above = matrix.get((i-1, j), float('inf')) + indel_penalty
    left = matrix.get((i, j-1), float('inf')) + indel_penalty

    matrix[(i, j)] = min(match, above, left)




