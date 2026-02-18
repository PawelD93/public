import pandas


def add_virtual_column(df, role, new_column):
    empty = pandas.DataFrame([])

    # 1. Check if DataFrame column names are valid
    for col in df.columns:
        if not str(col).replace('_', '').isalpha():
            return empty

    # 2. Check if new_column has a valid name
    if not new_column.replace('_', '').isalpha():
        return empty

    # 3. Check if role contains only allowed characters
    cleaned = role.replace(' ', '').replace('+', '').replace('-', '').replace('*', '').replace('_', '')
    if not cleaned.isalpha():
        return empty

    # 4. Extract column names from the expression and check if they exist in df
    role_copy = role
    for char in '+-*':
        role_copy = role_copy.replace(char, ' ') # Space instead of null in case of "col1+col2" to separate column names
    col_names = role_copy.split()
    for col_name in col_names:
        if col_name not in df.columns:
            return empty

    # 5. Evaluate the expression using df.eval() and add as a new column
    try:
        new_df = df.copy()
        new_df[new_column] = df.eval(role)
        return new_df
    except Exception:
        return empty
