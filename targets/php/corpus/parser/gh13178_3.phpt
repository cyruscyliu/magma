<?php

$data = ['foo' => 'foo', 'bar' => 'bar', 'baz' => 'baz'];

foreach ($data as $key => &$value) {
    var_dump($value);
    if ($value === 'baz') {
        unset($data['bar']);
        unset($data['baz']);
        $data['qux'] = 'qux';
        $data['quux'] = 'quux';
    }
}

?>