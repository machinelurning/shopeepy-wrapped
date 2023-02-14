def element_xpath_generator_by_attribute(element_tag, attribute, attribute_value):
    return f"//{element_tag}[@{attribute}='{attribute_value}']"


def element_xpath_generator_by_text(element_tag, attribute, attribute_value):
    return f"//{element_tag}[{attribute}()='{attribute_value}']"


def element_id_generator_tuple(element_tag, attribute, attribute_value):
    return element_tag, {attribute: attribute_value}


def element_id_generator(element_tag, attribute, attribute_value, xpath=False):
    if element_tag == "text":
        return element_xpath_generator_by_text(element_tag, attribute, attribute_value)
    elif xpath:
        return element_xpath_generator_by_attribute(
            element_tag, attribute, attribute_value
        )
    else:
        return element_id_generator_tuple(element_tag, attribute, attribute_value)
