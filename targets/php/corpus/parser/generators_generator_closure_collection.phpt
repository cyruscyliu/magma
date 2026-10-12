<?php

$genFactory = function() {
  yield 1;
  yield 2;
  yield 3;
};

$r = WeakReference::create($genFactory);
$generator = $genFactory();
unset($genFactory);

var_dump($r->get());

foreach ($generator as $value) var_dump($value);

var_dump($r->get());

unset($generator);

var_dump($r->get());

?>