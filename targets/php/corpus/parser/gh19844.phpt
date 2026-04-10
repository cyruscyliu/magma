<?php

class Test {
    public $context;
    private static $nested = false;

    function stream_open() {
        return true;
    }

    function stream_read() {
        return '.';
    }
    function stream_set_option() {}
    function stream_stat() {}

    function stream_eof() {
        if (!Test::$nested) {
            Test::$nested = true;
            include 'Test://';
        }
        @trigger_error('Bail', E_USER_ERROR);
    }

    function stream_close() {
        @trigger_error('Bail', E_USER_ERROR);
    }
}

stream_wrapper_register('Test', Test::class);
include 'Test://';

?>