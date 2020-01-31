def compute_elo(elo_challenger, elo_opponent, winner):
    '''Function for computation of ELO score.

    Input:
        * elo_challenger:   Elo score of challenger.
        * elo_opponent:     Elo score of opponent.
        * winner:           String which indicates winner. Allowed values are
                            "challenger", "opponent", "winner".
    Output:
        New ELO score for both players.
    '''
    elo_diff = elo_opponent-elo_challenger
    elo_change_a = 1/(1 + 10 ** (elo_diff/400))
    elo_change_b = 1 - elo_change_a
    k = 10  # TODO: vielleicht noch anpassen????????????

    if winner not in ["challenger", "opponent", "none"]:
        raise ValueError("winner has to be either 'challenger', 'opponent', or 'none'.")

    if winner == "challenger":
        new_elo_challenger = elo_challenger + k * (1 - elo_change_a)
        new_elo_opponent = elo_opponent + k * (0 - elo_change_b)
    elif winner == "opponent":
        new_elo_challenger = elo_challenger + k * (0 - elo_change_a)
        new_elo_opponent = elo_opponent + k * (1 - elo_change_b)
    elif winner == "none":
        new_elo_challenger = elo_challenger + k * (0.5 - elo_change_a)
        new_elo_opponent = elo_opponent + k * (0.5 - elo_change_b)

    return new_elo_challenger, new_elo_opponent


def extract_player_info(row):
    '''Function to extract participants and winner

    Input:
        * row:  Row of data which represents single race.

    Output:
        Challenger, opponent, and winner.
    '''
    challenger = row["challenger"]
    opponent = row["opponent"]
    winner = row["winner"]
    if winner == challenger:
        winner_str = "challenger"
    else:
        winner_str = "opponent"
    # return {"challenger": challenger, "opponent": opponent, "winner": winner}
    return challenger, opponent, winner_str

def date_to_numeric(row):

    excel_months = ["dummy", "Jan", "Feb", "Mrz", "Apr",
                    "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
    numerical_months = ["00", "01", "02", "03", "04",
                        "05", "06", "07", "08", "09", "10", "11", "12"]

    input_values = row.split(".")
    if len(input_values) == 2 and not input_values[1].isdigit():
        index = excel_months.index(input_values[1].strip())
        translated_month = numerical_months[index]
        return input_values[0] + "." + translated_month
    else:
        input_values = row.split()
        if len(input_values) == 2:
            index = excel_months.index(input_values[0])
            translated_month = numerical_months[index]
            return input_values[1] + "." + translated_month
        else:
            return row
