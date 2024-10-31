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

    for i in range(1, left_size+1):
        matrix[(i, 0)] = i * indel_penalty
    for j in range(1, top_size+1):
        matrix[(0, j)] = j * indel_penalty

    for i in range(1, left_size + 1):
        for j in range(1, top_size + 1):
            if seq1[i - 1] == seq2[j - 1]:
                match = matrix[(i - 1, j - 1)] + match_award
            else:  # Substitution
                match = matrix[(i - 1, j - 1)] + sub_penalty

            above = matrix[(i - 1, j)] + indel_penalty
            left = matrix[(i, j - 1)] + indel_penalty

            matrix[(i, j)] = min(match, above, left)

    alignment_cost = matrix[(left_size, top_size)]



    return alignment_cost, None, None


