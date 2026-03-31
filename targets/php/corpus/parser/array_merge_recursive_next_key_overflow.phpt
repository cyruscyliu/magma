<?php
try {
    array_merge_recursive(
        ['' => [PHP_INT_MAX => null]],
        ['' => [null]],
    );
} catch (Throwable $e) {
    echo $e->getMessage(), "\n";
}

try {
    array_merge_recursive(
        ['foo' => [PHP_INT_MAX => null]],
        ['foo' => str_repeat('a', 2)],
    );
} catch (Throwable $e) {
    echo $e->getMessage(), "\n";
}
?>