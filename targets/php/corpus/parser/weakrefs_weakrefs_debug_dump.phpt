<?php

$s = new stdClass;
$s->hello = 'world';

$weak = WeakReference::create($s);
var_dump($weak);
unset($s);
var_dump($weak);

?>