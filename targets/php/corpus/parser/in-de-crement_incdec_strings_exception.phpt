<?php

set_error_handler(function($severity, $m) {
    if ($severity == E_DEPRECATED) {
        $m = 'Deprecated: ' . $m;
    }
    if ($severity == E_WARNING) {
        $m = 'Warning: ' . $m;
    }
    throw new Exception($m, $severity);
});

$values = [
    '',
    ' ',
    // Alphanumeric values
    '199A',
    'A199',
    '199Z',
    'Z199',
    // Strings
    'Hello world',
    '🐘'
];
foreach ($values as $value) {
    try {
        $value++;
    } catch (\Exception $e) {
        echo $e->getMessage(), PHP_EOL;
    }
    var_dump($value);
    try {
        $value--;
    } catch (\Exception $e) {
        echo $e->getMessage(), PHP_EOL;
    }
    var_dump($value);
}
?>