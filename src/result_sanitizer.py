HIDDEN_COLUMNS = {
    "photo",
    "picture",
    "customer_id",
    "employee_id",
    "supplier_id",
    "category_id",
    "territory_id"
}
def sanitize_results(columns, rows):
    keep_indices = [
        i
        for i, col in enumerate(columns)
        if col not in HIDDEN_COLUMNS
    ]
    sanitized_columns = [
        columns[i]
        for i in keep_indices
    ]
    sanitized_rows = [
        tuple(
            row[i]
            for i in keep_indices
        )
        for row in rows
    ]

    return sanitized_columns, sanitized_rows

def handle_empty_results():
    return (
        "The query returned no results. This may indicate either no matching data or an incorrectly generated query."
    )
