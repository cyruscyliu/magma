<?php

var_dump(zend_test_zend_ini_parse_quantity('0x0x12'));

var_dump(zend_test_zend_ini_parse_quantity('0b+10'));
var_dump(zend_test_zend_ini_parse_quantity('0o+10'));
var_dump(zend_test_zend_ini_parse_quantity('0x+10'));

var_dump(zend_test_zend_ini_parse_quantity('0b 10'));
var_dump(zend_test_zend_ini_parse_quantity('0o 10'));
var_dump(zend_test_zend_ini_parse_quantity('0x 10'));

var_dump(zend_test_zend_ini_parse_quantity('0g10'));
var_dump(zend_test_zend_ini_parse_quantity('0m10'));
var_dump(zend_test_zend_ini_parse_quantity('0k10'));

?>