from shopeepy_wrapped.config.core import Element
from shopeepy_wrapped.string_manipulation.href_manipulation import append_site_prefix
from shopeepy_wrapped.string_manipulation.xpath_manipulation import xpath_generator


def test_append_site_prefix() -> None:
    # Given
    incomplete_href = "/test/link"

    # When
    complete_href = append_site_prefix(incomplete_href)

    # Then
    assert isinstance(complete_href, str)
    assert complete_href == "https://shopee.ph/test/link"
    assert complete_href is not None


def test_xpath_generator_happy() -> None:
    # Given
    element_tag = "div"
    attribute = "class"
    attribute_value_single_value = ["test_val"]
    attribute_value_multi_value = ["test_val1", "test_val2"]

    test_element_single = Element(element_tag=element_tag, attribute=attribute,
                                  attribute_value=attribute_value_single_value)
    test_element_multi = Element(element_tag=element_tag, attribute=attribute,
                                 attribute_value=attribute_value_multi_value)

    # When
    xpath_single_value = xpath_generator(test_element_single)
    xpath_multi_value = xpath_generator(test_element_multi)

    # Then
    assert isinstance(xpath_single_value, str)
    assert xpath_single_value == "//div[@class = 'test_val']"

    assert isinstance(xpath_multi_value, str)
    assert xpath_multi_value == "//div[@class = 'test_val1' or 'test_val2']"
