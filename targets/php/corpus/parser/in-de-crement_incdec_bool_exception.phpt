<?php

set_error_handler(function($severity, $m) {
    throw new Exception($m, $severity);
});

$values = [false, true];
foreach ($values as $value) {
    try {
        $value++;
    } catch (\Exception $e) {
        echo $e->getMessage(), PHP_EOL;
    }
    try {
        $value--;
    } catch (\Exception $e) {
        echo $e->getMessage(), PHP_EOL;
    }
}
?>