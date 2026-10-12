<?php

var_dump(zend_test_zend_call_stack_get());

function replace2() {
    return preg_replace_callback('#.#', function () {
        replace2();
    }, 'x');
}
function replace() {
    static $once = false;
    return preg_replace_callback('#.#', function () use (&$once) {
        try {
            replace();
        } finally {
            if (!$once) {
                $once = true;
                replace2();
            }
        }
    }, 'x');
}

try {
    replace();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
    echo 'Previous: ', $e->getPrevious()->getMessage(), "\n";
}

?>