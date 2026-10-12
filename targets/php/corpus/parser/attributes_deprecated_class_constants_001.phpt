<?php

class Clazz {
	#[\Deprecated]
	public const TEST = 1;

	#[\Deprecated()]
	public const TEST2 = 2;

	#[\Deprecated("use Clazz::TEST instead")]
	public const TEST3 = 3;

	#[\Deprecated]
	public const TEST4 = 4;

	#[\Deprecated]
	public const TEST5 = 5;
}

var_dump(Clazz::TEST);
var_dump(Clazz::TEST2);
var_dump(Clazz::TEST3);

var_dump(constant('Clazz::TEST4'));
var_dump(defined('Clazz::TEST5'));

?>