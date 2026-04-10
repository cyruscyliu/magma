<?php

define('SUFFIX', random_int(1, 2) == 1 ? 'a' : 'b');

#[\Deprecated]
const CONSTANT = 'Prefix-' . SUFFIX;

$value = CONSTANT;
var_dump($value);
var_dump($value === 'Prefix-' . SUFFIX);

?>