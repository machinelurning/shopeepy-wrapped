from shopeepy_wrapped.config.core import Element


def xpath_attr_val_generator(config: Element) -> str:
    attr_str = f'@{config["attribute"]} = '

    num_attr_vals = len(config["attribute_value"])

    if num_attr_vals == 1:
        attr_str = attr_str + f"'{config['attribute_value'][0]}'"
        return "[" + attr_str + "]"

    for i in range(num_attr_vals):
        if i == num_attr_vals:
            attr_str = attr_str + f"'{config['attribute_value'][i]}'"
        else:
            attr_str = attr_str + f"'{config['attribute_value'][i]}' or "
    return "[" + attr_str[:-4] + "]"


def xpath_generator(config: Element) -> str:
    attr_str = xpath_attr_val_generator(config=config)
    element_tag = f"//{config['element_tag']}"

    return element_tag + attr_str
