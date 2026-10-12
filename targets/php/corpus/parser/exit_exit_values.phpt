<?php

function zend_test_var_export($value) {
    if ($value === PHP_INT_MIN) {
        return "PHP_INT_MIN";
    }
    if ($value === PHP_INT_MAX) {
        return "PHP_INT_MAX";
    }
    if (is_array($value)) {
        return "[]";
    }
    if (is_resource($value)) {
        return "STDERR";
    }
    if ($value instanceof stdClass) {
        return "new stdClass()";
    }
    return var_export($value, true);
}

$values = [
    null,
    false,
    true,
    0,
    1,
    20,
    10.0,
    15.5,
    "Hello world",
    [],
    STDERR,
    new stdClass(),
];

const FILE_PATH = __DIR__ . '/exit_values_test.php';
const FILE_CONTENT = <<<'TEMPLATE'
<?php
try {
    exit(VALUE);
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}

TEMPLATE;

$php = getenv('TEST_PHP_EXECUTABLE_ESCAPED');
$command = $php . ' --no-php-ini ' . escapeshellarg(FILE_PATH);

foreach ([FILE_CONTENT, str_replace('exit', 'die', FILE_CONTENT)] as $code) {
    foreach ($values as $value) {
        echo 'Using ', zend_test_var_export($value), ' as value:', PHP_EOL;
        $output = [];
        $content = str_replace('VALUE', zend_test_var_export($value), $code);
        file_put_contents(FILE_PATH, $content);
        exec($command, $output, $exit_status);
        echo 'Exit status is: ', $exit_status, PHP_EOL,
             'Output is:', PHP_EOL, join($output), PHP_EOL;
    }

    echo 'As a statement:', PHP_EOL;
    $output = [];
    $content = str_replace('(VALUE)', '', $code);
    exec($command, $output, $exit_status);
    echo 'Exit status is: ', $exit_status, PHP_EOL,
         'Output is:', PHP_EOL, join($output), PHP_EOL;
}

?>