<?php

require_once __DIR__ . DIRECTORY_SEPARATOR . 'test_offset_helpers.inc';

foreach ($containers as $container) {
    echo zend_test_var_export($container), " container:\n";
    try {
        $container[] = 'value';
        var_dump($container);
    } catch (\Throwable $e) {
        echo $e->getMessage(), "\n";
    }
}

?>