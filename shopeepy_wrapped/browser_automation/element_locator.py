from typing import Dict, Tuple, Union


def element_xpath_generator_by_attribute(
        element_tag: str, attribute: str, attribute_value: str
) -> str:
    return f"//{element_tag}[@{attribute}='{attribute_value}']"


def element_xpath_generator_by_text(
        element_tag: str, attribute: str, attribute_value: str
) -> str:
    return f"//{element_tag}[{attribute}()='{attribute_value}']"


def element_id_generator_tuple(
        element_tag: str, attribute: str, attribute_value: str
) -> Tuple[str, Dict[str, str]]:
    return element_tag, {attribute: attribute_value}


def element_id_generator(
        element_tag: str, attribute: str, attribute_value: str, xpath: bool = False
) -> Union[Tuple[str, Dict[str, str]], str]:
    if element_tag == "text":
        return element_xpath_generator_by_text(element_tag, attribute, attribute_value)
    elif xpath:
        return element_xpath_generator_by_attribute(
            element_tag, attribute, attribute_value
        )
    else:
        return element_id_generator_tuple(element_tag, attribute, attribute_value)
