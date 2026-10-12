<?php

define('SUFFIX', random_int(1, 2) == 1 ? 'a' : 'b');

class Clazz {
	#[\Deprecated]
	public const CONSTANT = self::class . '-' . SUFFIX;
}

$value = Clazz::CONSTANT;
var_dump($value);
var_dump($value === 'Clazz-' . SUFFIX);

?>