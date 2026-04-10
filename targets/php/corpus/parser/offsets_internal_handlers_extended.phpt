<?php

require_once __DIR__ . DIRECTORY_SEPARATOR . 'test_offset_helpers.inc';

class NoImplement extends DimensionHandlersNoArrayAccess {}

class DoImplement extends DimensionHandlersNoArrayAccess implements ArrayAccess {
    public function offsetSet($offset, $value): void {
        var_dump(__METHOD__);
        var_dump($offset);
        var_dump($value);
    }
    public function offsetGet($offset): mixed {
        var_dump(__METHOD__);
        var_dump($offset);
        return "dummy";
    }
    public function offsetUnset($offset): void {
        var_dump(__METHOD__);
        var_dump($offset);
    }
    public function offsetExists($offset): bool {
        var_dump(__METHOD__);
        var_dump($offset);
        return true;
    }
}

$no = new NoImplement();
$do = new DoImplement();

$no['foo'];
exportObject($no);

$do['foo'];
exportObject($do);

?>