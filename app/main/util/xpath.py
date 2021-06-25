xpath_info = dict(
    removal_buttons="//button[contains(@title, 'Remove')]",
    add_filter_button="".join([
        "//span[contains(text(), 'Add another filter')]",
        "/ancestor::button"
    ]),
    region_checkbox="".join([
        "//span[contains(text(), 'Region')]",
        "/ancestor::label/*[name()='svg']"
    ]),
    close_menu_button="".join([
        "//div[not(contains(@id, 'dropdown'))]",
        "/button[contains(@class, 'close')]"]),
    add_region_checkbox="".join([
        "//span[contains(text(), 'Add')]/span[contains(text(), 'Region')]",
        "/ancestor::div/*[name()='svg']"
    ]),
    choose_region_checkbox="".join([
        "//span[contains(text(), '{}')]",
        "/ancestor::label/*[name()='svg']"
    ]),
    find_stocks_button="".join([
        "//span[contains(text(), 'Find')]/span[contains(text(), 'Stocks')]",
        "/ancestor::button[contains(@class, 'linkActiveColor')]"
    ]),
    matching_stocks_evidence="".join([
        "//span[contains(text(), 'Matching')]",
        "/span[contains(text(), 'Stocks')]"
    ]),
    show_25_rows_link="//span[contains(text(), 'Show')]",
    show_100_rows_link="//span[contains(text(), 'Show 100 rows')]",
    result_metrics_span="".join([
        "//span[contains(text(), 'Matching')]",
        "/following-sibling::span/span[contains(text(), 'results')]"
    ]),
    next_page_link="//span[contains(text(), 'Next')]"
)
