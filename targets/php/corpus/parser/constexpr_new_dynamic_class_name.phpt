<?php

class Foo {}
const FOO = 'Foo';
static $x = new (FOO);

var_dump($x);

?>