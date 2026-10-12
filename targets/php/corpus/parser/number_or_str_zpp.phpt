<?php

class Foo {}
class ToString {
    public function __toString() {
        return "ToString";
    }
}

var_dump(zend_number_or_string("string"));
var_dump(zend_number_or_string(1));
var_dump(zend_number_or_string(5.5));
var_dump(zend_number_or_string(null));
var_dump(zend_number_or_string(false));
var_dump(zend_number_or_string(true));
var_dump(zend_number_or_string(new ToString()));

try {
    zend_string_or_object([]);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}
try {
    zend_number_or_string(new Foo());
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

var_dump(zend_number_or_string_or_null("string"));
var_dump(zend_number_or_string_or_null(1));
var_dump(zend_number_or_string_or_null(5.5));
var_dump(zend_number_or_string_or_null(null));
var_dump(zend_number_or_string_or_null(false));
var_dump(zend_number_or_string_or_null(true));
var_dump(zend_number_or_string_or_null(new ToString()));

try {
    zend_number_or_string_or_null([]);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}
try {
    zend_number_or_string_or_null(new Foo());
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

?>