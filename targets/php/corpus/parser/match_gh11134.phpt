<?php

function testMatch() {
    return match ($unset ?? null) {
        'foo' => 'foo',
        'bar' => 'bar',
        default => 'baz',
    };
}

function testSwitch() {
    switch ($unset ?? null) {
        case 'foo': return 'foo';
        case 'bar': return 'bar';
        default: return 'baz';
    }
}

var_dump(testMatch());
var_dump(testSwitch());

?>