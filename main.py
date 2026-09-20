import backend, ui, threading

#refreshing items first makes it so the ui takes a bit to show
def main() -> None:
    settings_dict = backend.read_settings()

    product_list = backend.read_item_list()
    
    #settings initialization(might be a better way to do it)
    if settings_dict['refresh_on_startup'] == True:
            refresh_thread = threading.Thread(target = backend.refresh_products, daemon = True)
            refresh_thread.start()

    product_list = backend.read_item_list()

    ui.ui_initialization(product_list, backend.scrape_item_info)


if __name__ == '__main__':
    main()