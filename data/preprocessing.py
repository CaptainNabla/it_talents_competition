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
