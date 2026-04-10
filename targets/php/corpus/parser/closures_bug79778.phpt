<?php
$closure1 = function() {
    static $var = CONST_REF;
};

var_dump($closure1);
print_r($closure1);

try {
    $closure1();
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}

var_dump($closure1);
print_r($closure1);

const CONST_REF = 'foo';
$closure1();
var_dump($closure1);
print_r($closure1);

?>