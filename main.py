import backend, ui

product_list = backend.read_item_list()

ui.ui_initialization(product_list, backend.scrape_item_info)
