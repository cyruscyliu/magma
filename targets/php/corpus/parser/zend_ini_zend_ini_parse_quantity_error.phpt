<?php

// This test checks invalid formats do throw warnings.

$tests = [
    'K',     # No digits
    '1KM',   # Multiple multipliers.
    '1X',    # Unknown multiplier.
    '1.0K',  # Non integral digits.

    '0X',    # Valid prefix with no value
    '0Z',    # Invalid prefix
    '0XK',   # Valid prefix with no value and multiplier

    '++',
    '-+',
    '+ 25',
    '- 25',

    # Null bytes
    " 123\x00K",
    "\x00 123K",
    " \x00123K",
    " 123\x00K",
    " 123K\x00",
    " 123\x00",
];

foreach ($tests as $setting) {
    printf("# \"%s\"\n", addcslashes($setting, "\0..\37!@\177..\377"));
    var_dump(zend_test_zend_ini_parse_quantity($setting));
    print "\n";
}
?>