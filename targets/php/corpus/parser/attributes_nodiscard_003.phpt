<?php

trait T {
	#[\NoDiscard]
	function test(): int {
		return 0;
	}
}

class Clazz {
	use T;
}

$cls = new Clazz();
$cls->test();

?>