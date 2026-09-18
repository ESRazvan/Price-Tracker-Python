import requests, csv, json, re
from bs4 import BeautifulSoup, Tag

#Altex does not work, request is timed out.

#(response, current_site, error_description)
def request_data(link: str) -> tuple[requests.Response | None, str | None, str | None]: 
    supported_sites = ['emag']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    for site in supported_sites:
        if site in link:
            current_site = site
            break
        else:
            current_site = None

    if not current_site:
        return None, None, 'Unsupported site link provided'

    try:
        raw_data = requests.get(url = link, headers = header, timeout = 30)

        #Raises error
        raw_data.raise_for_status()

        return raw_data, current_site, None
    except requests.exceptions.Timeout:
        return None, current_site, 'Request timed out.'
    except requests.exceptions.HTTPError as e:
        return None, current_site, f'HTTP errror: {e.response.status_code}'
    except requests.exceptions.RequestException as e:
        return None, current_site, f'Network request failed with the following code: {e}'


def parse_extract_data(raw_data: requests.Response, current_site: str) -> dict:
    site_script_tags_patterns = {
        'emag' : ['text/javascript', r'\"products\":(\[.*?\])'], #extract only the text in the products tag
        #'altex' : ['application/ld+json', '(.*)'],
    }

    parsed_data: BeautifulSoup = BeautifulSoup(raw_data.text, 'html.parser')
    script_tag_content: Tag | None = parsed_data.find('script', type = site_script_tags_patterns[current_site][0])

    #group(1) means the first instance found. re.dotall makes the search continue over newline
    raw_match: str = re.search(site_script_tags_patterns[current_site][1], script_tag_content.text, re.DOTALL).group(1)

    #Need all " instead of ' to use json loads and also no , before the }
    clean_match = raw_match.replace("'", '"')
    clean_match = re.sub(r',\s*\}', '}', clean_match)

    #turns json into a list that has 1 dict item in index 0
    item_data: list = json.loads(clean_match)
    item_data: dict = item_data[0]
    return item_data

#name is usually too big, extract until brand name or first 3 words
def extract_name(name: str, brand: str) -> str:
    name = name.strip('"')
    brand = brand.strip('"')

    if brand in name:
        first_char_index = name.find(brand)
        short_name = name[:first_char_index + len(brand)]

    if brand not in name or len(short_name) >= 50:
        word_list = name.split()[:3]
        short_name = ' '.join(word_list)

    return short_name

def store_in_csv(item_data: dict, item_link: str) -> None:
    columns = ['name', 'category', 'brand', 'price', 'status', 'link']
    correct_item_data = {}

    #extract only the necessary key:value pairs in a new dictionary
    for column in columns:
        if column == 'name':
            correct_item_data[column] = extract_name(item_data['name'], item_data['brand'])
        elif column == 'link':
            correct_item_data[column] = item_link
        else:
            correct_item_data[column] = item_data[column]

    with open ('data.csv', 'a', newline = '', encoding = 'utf-8') as data_file:
        csv_writer = csv.writer(data_file)
        if data_file.tell() == 0:
            csv_writer.writerow(columns)
        csv_writer.writerow(correct_item_data.values())

def read_item_list() -> list[dict]:
    with open ('data.csv', 'r', newline = '', encoding = 'utf-8') as data_file:
        csv_reader = csv.DictReader(data_file)
        item_list = list(csv_reader)
    return item_list

#extract only the links from the whole list of dicts that is the item info
def read_item_links() -> list[str]:
    item_list = read_item_list()
    return [item['link'] for item in item_list]

def read_settings() -> dict:
    with open('settings.json', 'r') as f:
        settings_dict = json.loads(f)

def refresh_products() -> None:
    item_link_list = read_item_links()

    #truncate the csv file and write the data again
    with open('data.csv', 'w', newline = '') as csv_file:
        csv_file.seek(0, 0)
        csv_file.truncate(0)

    #scrape the info for every saved link again to refresh the data
    for link in item_link_list:
        scrape_item_info(link)

def scrape_item_info(input_link: str) -> None:

    extracted_raw_data, current_site, error_description = request_data(input_link)

    if not error_description:
        extracted_item_data = parse_extract_data(extracted_raw_data, current_site)
        store_in_csv(extracted_item_data, input_link)
    else:
        print(error_description)
