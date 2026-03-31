<?php
class FooWrapper {
    public $context;
    public function stream_open($path, $mode, $options, &$opened_path) {
        stream_wrapper_unregister('foo');
        return false;
    }
}
stream_wrapper_register('foo', 'FooWrapper');
var_dump(fopen('foo://bar', 'r'));
?>