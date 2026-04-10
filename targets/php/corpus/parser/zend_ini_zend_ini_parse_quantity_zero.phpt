<?php

$tests = [
    '0',
    '0K',
    '0k',
    '0M',
    '0m',
    '0G',
    '0g',
    '-0',
    '-0K',
    '-0k',
    '-0M',
    '-0m',
    '-0G',
    '-0g',
];

foreach ($tests as $setting) {
    printf("# \"%s\"\n", addcslashes($setting, "\0..\37!@\177..\377"));
    var_dump(zend_test_zend_ini_parse_quantity($setting));
    print "\n";
}
?>