import json
import io
from bs4 import BeautifulSoup
import time

def extract_locators(soup: BeautifulSoup, progress_bar) -> dict:
    """Extract different types of locators from the webpage."""
    locators = {
        'ID': [],
        'Name': [],
        'Data-testid': [],
        'CSS': [],
        'XPath': []
    }
    
    # Extract IDs
    progress_bar.progress(0.2)
    elements = soup.find_all(id=True)
    for element in elements:
        locators['ID'].append({
            'locator': element.get('id'),
            'element': str(element.name)
        })

    # Extract Names
    progress_bar.progress(0.4)
    elements = soup.find_all(attrs={"name": True})
    for element in elements:
        locators['Name'].append({
            'locator': element.get('name'),
            'element': str(element.name)
        })

    # Extract Data-testids
    progress_bar.progress(0.6)
    elements = soup.find_all(attrs={"data-testid": True})
    for element in elements:
        locators['Data-testid'].append({
            'locator': element.get('data-testid'),
            'element': str(element.name)
        })

    # Generate CSS Selectors
    progress_bar.progress(0.8)
    for element in soup.find_all(class_=True):
        css_selector = f"{element.name}.{element['class'][0]}"
        locators['CSS'].append({
            'locator': css_selector,
            'element': str(element.name)
        })

    # Generate XPath
    progress_bar.progress(0.9)
    for i, element in enumerate(soup.find_all()):
        xpath = generate_xpath(element)
        if xpath:
            locators['XPath'].append({
                'locator': xpath,
                'element': str(element.name)
            })

    progress_bar.progress(1.0)
    time.sleep(0.5)  # Allow users to see completion
    progress_bar.empty()
    
    return locators

def generate_xpath(element) -> str:
    """Generate XPath for a given element."""
    components = []
    child = element
    
    for parent in element.parents:
        if parent.name == '[document]':
            break
        
        siblings = parent.find_all(child.name, recursive=False)
        if len(siblings) > 1:
            index = siblings.index(child) + 1
            components.insert(0, f'{child.name}[{index}]')
        else:
            components.insert(0, child.name)
            
        child = parent
    
    return '//' + '/'.join(components)

def save_to_json(data: dict) -> str:
    """Convert locators to JSON string."""
    return json.dumps(data, indent=2)

def save_to_csv(df) -> str:
    """Convert DataFrame to CSV string."""
    return df.to_csv(index=False).encode('utf-8')
