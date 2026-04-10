<?php

function handler($errno, $errstr, $errfile, $errline) {
	echo "$errstr in $errfile on line $errline\n";
	eval('class string {}');
}

set_error_handler('handler');

var_dump(_ZendTestClass::ZEND_TEST_DEPRECATED);
?>