# utils.py

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
        'XPath': [],
        'Links': [],
        'Buttons': [],
        'Class Names': [],
        'Accessibility': []
    }

    # Extract IDs
    progress_bar.progress(0.1)
    elements = soup.find_all(id=True)
    for element in elements:
        locators['ID'].append({
            'locator': element.get('id'),
            'element': str(element.name)
        })

    # Extract Names
    progress_bar.progress(0.2)
    elements = soup.find_all(attrs={"name": True})
    for element in elements:
        locators['Name'].append({
            'locator': element.get('name'),
            'element': str(element.name)
        })

    # Extract Data-testids
    progress_bar.progress(0.3)
    elements = soup.find_all(attrs={"data-testid": True})
    for element in elements:
        locators['Data-testid'].append({
            'locator': element.get('data-testid'),
            'element': str(element.name)
        })

    # Extract Links
    progress_bar.progress(0.4)
    links = soup.find_all('a', href=True)
    for link in links:
        locators['Links'].append({
            'locator': link.get('href'),
            'element': f"a[text='{link.text.strip()[:50]}...']" if len(link.text.strip()) > 50 else f"a[text='{link.text.strip()}']"
        })

    # Extract Buttons
    progress_bar.progress(0.5)
    buttons = soup.find_all(['button', 'input'])
    for button in buttons:
        if button.name == 'input' and button.get('type') in ['submit', 'button', 'reset']:
            locators['Buttons'].append({
                'locator': button.get('value', '') or button.get('name', '') or button.get('id', ''),
                'element': f"input[type='{button.get('type')}']"
            })
        elif button.name == 'button':
            locators['Buttons'].append({
                'locator': button.text.strip() or button.get('id', '') or button.get('name', ''),
                'element': 'button'
            })

    # Extract Class Names
    progress_bar.progress(0.6)
    elements = soup.find_all(class_=True)
    for element in elements:
        for class_name in element.get('class'):
            locators['Class Names'].append({
                'locator': class_name,
                'element': str(element.name)
            })

    # Extract Accessibility Attributes
    progress_bar.progress(0.7)
    accessibility_attrs = ['aria-label', 'aria-describedby', 'aria-labelledby', 'role', 'alt']
    for attr in accessibility_attrs:
        elements = soup.find_all(attrs={attr: True})
        for element in elements:
            locators['Accessibility'].append({
                'locator': f"{attr}='{element.get(attr)}'",
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