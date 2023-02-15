from typing import Dict, List, Tuple

from shopeepy_wrapped.config.core import Element


def element_id_generator(
    config: Element,
) -> Tuple[str, Dict[str, List[str]]]:
    return config["element_tag"], {config["attribute"]: config["attribute_value"]}
